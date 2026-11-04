"""
Data Preprocessing and Feature Engineering Module
FootLens Analytics - Player Injuries and Team Performance Dashboard
Course: Mathematics for AI-II (Summative Assessment)
"""

import pandas as pd
import numpy as np
import re


def clean_rating(val):
    """
    Cleans player rating entries.
    Handles 'N.A.', substitute annotations like '6(S)', typos like '5..8',
    and unrated entries (returns NaN).
    """
    if pd.isna(val) or val == 'N.A.':
        return np.nan
    val_str = str(val).strip()
    # Remove substitute indicator like '(S)'
    val_str = re.sub(r'\(.*?\)', '', val_str).strip()
    # Handle accidental double decimal points e.g. '5..8' -> '5.8'
    if '..' in val_str:
        val_str = val_str.replace('..', '.')
    try:
        f = float(val_str)
        # Ratings in European football analytics are scored on 1-10 scale
        return f if f > 0 else np.nan
    except ValueError:
        return np.nan


def clean_gd(val):
    """
    Cleans Goal Difference (GD) entries.
    Converts valid integer/float strings to float; 'N.A.' to NaN.
    """
    if pd.isna(val) or val == 'N.A.':
        return np.nan
    try:
        return float(val)
    except ValueError:
        return np.nan


def result_to_points(res):
    """
    Converts match result ('win', 'draw', 'lose') into league table points.
    Win = 3 points, Draw = 1 point, Loss = 0 points.
    """
    if pd.isna(res) or res == 'N.A.':
        return np.nan
    res = str(res).lower().strip()
    if res == 'win':
        return 3.0
    elif res == 'draw':
        return 1.0
    elif res in ['lose', 'loss']:
        return 0.0
    return np.nan


def clean_date(date_str):
    """
    Parses and standardizes date strings into pandas datetime objects.
    Corrects historical typographical quirks like '0202' -> '2021',
    missing comma spacing e.g. 'Oct 15,2022', and ongoing status 'Present'.
    """
    if pd.isna(date_str) or date_str == 'N.A.' or str(date_str).strip() == '':
        return pd.NaT
    date_str = str(date_str).strip()
    if date_str.lower() == 'present':
        return pd.NaT  # Active/ongoing injury at the conclusion of tracking
    # Fix dataset typo: 'Mar 7, 0202' -> 'Mar 7, 2021'
    if '0202' in date_str:
        date_str = date_str.replace('0202', '2021')
    # Ensure space after comma in dates like 'Oct 15,2022'
    date_str = re.sub(r',(\d{4})', r', \1', date_str)
    return pd.to_datetime(date_str, format='mixed', errors='coerce')


def categorize_injury(injury):
    """
    Groups raw injury descriptions into standardized sports medicine clinical categories.
    """
    if pd.isna(injury):
        return 'Other / Unknown'
    inj = str(injury).lower().strip()
    if 'hamstring' in inj:
        return 'Hamstring'
    elif 'knee' in inj or 'cruciate' in inj or 'meniscus' in inj:
        return 'Knee / Ligament'
    elif 'ankle' in inj:
        return 'Ankle'
    elif 'calf' in inj or 'shin' in inj or 'achilles' in inj:
        return 'Calf / Lower Leg'
    elif 'groin' in inj or 'pubic' in inj or 'adductor' in inj or 'pelvic' in inj:
        return 'Groin / Pelvis'
    elif 'thigh' in inj or 'quad' in inj:
        return 'Thigh / Quad'
    elif 'foot' in inj or 'toe' in inj or 'metatarsal' in inj:
        return 'Foot / Toe'
    elif 'back' in inj or 'ack injury' in inj:
        return 'Back / Spine'
    elif any(k in inj for k in ['shoulder', 'arm', 'elbow', 'hand', 'collarbone', 'rib']):
        return 'Upper Body'
    elif any(k in inj for k in ['head', 'concussion', 'facial', 'nose', 'cheekbone']):
        return 'Head / Concussion'
    elif any(k in inj for k in ['ill', 'virus', 'coronavirus', 'cold', 'fever', 'malaria', 'tonsillitis', 'infection', 'shingles', 'bronchitis']):
        return 'Illness / Infection'
    elif 'muscle' in inj or 'strain' in inj or 'fatigue' in inj:
        return 'Muscle Strain / Fatigue'
    else:
        return 'Other / Unknown'


def categorize_position(pos):
    """
    Normalizes specific football positions into standard squad units.
    """
    if pd.isna(pos):
        return 'Other'
    pos = str(pos).lower().strip()
    if 'goalkeeper' in pos:
        return 'Goalkeeper'
    elif 'back' in pos:
        return 'Defender'
    elif 'midfielder' in pos:
        return 'Midfielder'
    elif 'winger' in pos or 'forward' in pos:
        return 'Forward'
    return 'Other'


def load_and_preprocess_data(csv_path='player_injuries_impact.csv'):
    """
    Loads raw CSV and executes the complete cleaning and feature engineering pipeline.
    Returns cleaned pandas DataFrame with standardized names and engineered metrics.
    """
    # Load with latin-1 encoding to preserve international player names with diacritics
    df = pd.read_csv(csv_path, encoding='latin-1')

    # 1. Clean string fields
    df['Name'] = df['Name'].astype(str).str.strip()
    df['Team Name'] = df['Team Name'].astype(str).str.strip()
    df['Position'] = df['Position'].astype(str).str.strip()
    df['Injury'] = df['Injury'].astype(str).str.strip()
    df['Season'] = df['Season'].astype(str).str.strip()

    # 2. Date conversion and handling of known dataset anomalies
    df['Injury_Date'] = df['Date of Injury'].apply(clean_date)
    df['Return_Date'] = df['Date of return'].apply(clean_date)

    # Correct inverted return years in original dataset:
    # Row: Tanguy Ndombele injured 2020-01-01, typo returned 2019-01-21 -> 2020-01-21
    mask_ndombele = (df['Name'] == 'Tanguy Ndombele') & (df['Injury_Date'] == '2020-01-01')
    df.loc[mask_ndombele, 'Return_Date'] = pd.Timestamp('2020-01-21')

    # Row: Matej Vydra injured 2020-12-18, typo returned 2020-01-11 -> 2021-01-11
    mask_vydra = (df['Name'] == 'Matej Vydra') & (df['Injury_Date'] == '2020-12-18')
    df.loc[mask_vydra, 'Return_Date'] = pd.Timestamp('2021-01-11')

    # Calculate injury severity / recovery duration (days lost)
    df['Recovery_Days'] = (df['Return_Date'] - df['Injury_Date']).dt.days

    # 3. Categorize positions and injuries
    df['Injury_Category'] = df['Injury'].apply(categorize_injury)
    df['Position_Group'] = df['Position'].apply(categorize_position)

    # 4. Temporal attributes
    df['Injury_Year'] = df['Injury_Date'].dt.year
    df['Injury_Month'] = df['Injury_Date'].dt.strftime('%B')
    df['Injury_Month_Num'] = df['Injury_Date'].dt.month

    # 5. Clean individual player ratings
    before_rating_cols = [
        'Match1_before_injury_Player_rating',
        'Match2_before_injury_Player_rating',
        'Match3_before_injury_Player_rating'
    ]
    after_rating_cols = [
        'Match1_after_injury_Player_rating',
        'Match2_after_injury_Player_rating',
        'Match3_after_injury_Player_rating'
    ]

    for c in before_rating_cols + after_rating_cols:
        df[c + '_clean'] = df[c].apply(clean_rating)

    # Calculate player's average rating before and after injury
    df['Pre_Injury_Avg_Rating'] = df[[c + '_clean' for c in before_rating_cols]].mean(axis=1)
    df['Post_Injury_Avg_Rating'] = df[[c + '_clean' for c in after_rating_cols]].mean(axis=1)
    df['Rating_Improvement'] = df['Post_Injury_Avg_Rating'] - df['Pre_Injury_Avg_Rating']

    # 6. Clean match results and convert to Points Per Match (PPM)
    before_res_cols = ['Match1_before_injury_Result', 'Match2_before_injury_Result', 'Match3_before_injury_Result']
    missed_res_cols = ['Match1_missed_match_Result', 'Match2_missed_match_Result', 'Match3_missed_match_Result']
    after_res_cols = ['Match1_after_injury_Result', 'Match2_after_injury_Result', 'Match3_after_injury_Result']

    for c in before_res_cols + missed_res_cols + after_res_cols:
        df[c + '_pts'] = df[c].apply(result_to_points)

    df['Pre_Injury_Team_PPM'] = df[[c + '_pts' for c in before_res_cols]].mean(axis=1)
    df['During_Absence_Team_PPM'] = df[[c + '_pts' for c in missed_res_cols]].mean(axis=1)
    df['Post_Injury_Team_PPM'] = df[[c + '_pts' for c in after_res_cols]].mean(axis=1)

    # 7. Clean Goal Difference (GD)
    before_gd_cols = ['Match1_before_injury_GD', 'Match2_before_injury_GD', 'Match3_before_injury_GD']
    missed_gd_cols = ['Match1_missed_match_GD', 'Match2_missed_match_GD', 'Match3_missed_match_GD']
    after_gd_cols = ['Match1_after_injury_GD', 'Match2_after_injury_GD', 'Match3_after_injury_GD']

    for c in before_gd_cols + missed_gd_cols + after_gd_cols:
        df[c + '_clean'] = df[c].apply(clean_gd)

    df['Pre_Injury_Team_Avg_GD'] = df[[c + '_clean' for c in before_gd_cols]].mean(axis=1)
    df['During_Absence_Team_Avg_GD'] = df[[c + '_clean' for c in missed_gd_cols]].mean(axis=1)
    df['Post_Injury_Team_Avg_GD'] = df[[c + '_clean' for c in after_gd_cols]].mean(axis=1)

    # 8. Team Performance Drop Index
    # Primary sports analytics drop metric: Drop in Points Per Match (PPM Before - PPM During)
    # Goal difference drop: Average GD Before - Average GD During
    df['Team_PPM_Drop'] = df['Pre_Injury_Team_PPM'] - df['During_Absence_Team_PPM']
    df['Team_GD_Drop'] = df['Pre_Injury_Team_Avg_GD'] - df['During_Absence_Team_Avg_GD']
    
    # Standard Performance Drop Index:
    # A positive drop index means team performed WORSE during player absence.
    # We define the primary Performance Drop Index as Team_PPM_Drop
    df['Performance_Drop_Index'] = df['Team_PPM_Drop'].round(3)

    # Clean display column names
    df['Player_Name'] = df['Name']
    df['Club'] = df['Team Name']

    return df


if __name__ == '__main__':
    clean_df = load_and_preprocess_data()
    print("Preprocessed DataFrame successfully! Shape:", clean_df.shape)
    print("Columns sample:", clean_df[['Player_Name', 'Club', 'Injury_Category', 'Performance_Drop_Index', 'Rating_Improvement']].head())
