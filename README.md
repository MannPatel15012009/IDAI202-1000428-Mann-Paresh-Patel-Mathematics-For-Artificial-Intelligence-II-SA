# ⚽ FootLens Analytics: Player Injuries & Team Performance Dashboard
> **Mathematics for AI-II (AI-202) — Summative Assessment (60 Marks)**  
> **Scenario 1:** Junior Sports Data Analyst for FootLens Analytics  
> **Deployment Target:** Streamlit Cloud & GitHub  

---

## 📌 Executive Summary & Project Overview

**FootLens Analytics** is a leading sports analytics consultancy dedicated to tactical optimization, squad availability modeling, and injury mitigation in professional European football. 

In elite association football, player injuries represent not merely a medical challenge, but a profound sporting and economic disruption. When key personnel are sidelined, clubs suffer tactical dislocation, altered team chemistry, and acute performance drops in league fixtures. 

This project delivers an interactive, user-centered **Streamlit Analytics Dashboard** that models the direct mathematical relationship between player injuries, recovery trajectories, and team match outcomes across multiple Premier League seasons (2019/20 through 2023/24). Technical directors, medical staff, and head coaches can explore data-backed insights to guide squad rotation, tactical contingency planning, and comeback management.

---

## 🔬 Mathematical Formulations & Sports Analytics Metrics

To establish an analytical standard for assessing injury impact, the following mathematical formulations are implemented in this project:

### 1. Player Pre-Injury Baseline Rating (R̄_pre)
The average match performance rating (scored on the European standard 1.0 – 10.0 scale) across the three matches preceding the injury:

```math
\bar{R}_{\text{pre}} = \frac{1}{k_{\text{pre}}} \sum_{i=1}^{k_{\text{pre}}} R_{\text{before}, i}, \quad (k_{\text{pre}} \le 3)
```

### 2. Player Post-Injury Return Rating (R̄_post)
The average match performance rating across the first three matches following official return to competition:

```math
\bar{R}_{\text{post}} = \frac{1}{k_{\text{post}}} \sum_{j=1}^{k_{\text{post}}} R_{\text{after}, j}, \quad (k_{\text{post}} \le 3)
```

### 3. Individual Comeback Rating Delta (ΔR)
Quantifies whether a player returned in enhanced form (positive comeback surge) or experienced post-recovery form degradation:

```math
\Delta R = \bar{R}_{\text{post}} - \bar{R}_{\text{pre}}
```

* **ΔR > +0.10:** Strong positive comeback (player outperformed pre-injury form).
* **-0.10 ≤ ΔR ≤ +0.10:** Neutral / stable performance retention.
* **ΔR < -0.10:** Post-injury form dip / performance degradation.

### 4. Team Points Per Match (PPM)
Standardized Premier League league-table points metric (Win = 3 points, Draw = 1 point, Loss = 0 points):

```math
\text{Points Per Match (PPM)} = \frac{3 \cdot W + 1 \cdot D + 0 \cdot L}{N_{\text{matches}}}
```

### 5. Team Performance Drop Index (PDI)
Quantifies team performance deterioration during a player's absence by subtracting the Points Per Match earned during the player's missed matches from the pre-injury baseline:

```math
\text{Performance Drop Index (PDI)} = \text{PPM}_{\text{before}} - \text{PPM}_{\text{during}}
```

* **PDI > 0:** Indicates the team performed **worse** when the player was sidelined (direct reliance / negative absence impact).
* **PDI ≈ 0:** Squad depth successfully insulated the team from point loss.
* **PDI < 0:** Team managed to win more points in the absence window.

### 6. Team Goal Difference Shift (ΔGD)
Measures structural offensive and defensive margin drop:

```math
\Delta \text{GD} = \overline{\text{GD}}_{\text{before}} - \overline{\text{GD}}_{\text{during}}
```

### 7. Injury Severity / Recovery Duration (t_recovery)
The temporal length of absence in calendar days:

```math
t_{\text{recovery}} = \text{Date of Return} - \text{Date of Injury} \quad (\text{in days})
```

---

### 📋 Mathematical Metrics Reference Table

| Metric Name | Symbol | Mathematical Formula | Sporting Analytics Interpretation |
| :--- | :---: | :--- | :--- |
| **Pre-Injury Rating** | `R̄_pre` | `(1 / k) ∑ R_before` | Baseline individual form over prior 3 matches |
| **Post-Injury Rating** | `R̄_post` | `(1 / k) ∑ R_after` | Recovery form over first 3 comeback matches |
| **Rating Delta** | `ΔR` | `R̄_post − R̄_pre` | Comeback surge (ΔR > 0) vs. form decline (ΔR < 0) |
| **Points Per Match** | `PPM` | `(3·W + 1·D + 0·L) / N` | Normalized match efficiency on Premier League table |
| **Performance Drop Index** | `PDI` | `PPM_before − PPM_during` | Net team points lost per match during player absence |
| **Goal Difference Drop** | `ΔGD` | `GD̄_before − GD̄_during` | Structural goal margin drop without player |
| **Recovery Duration** | `t_recovery` | `Return Date − Injury Date` | Total physical downtime in calendar days |

---

## ❓ Five Core Business Questions Answered

### 1. Which injuries led to the biggest team performance drop?
* **Finding:** Structural joint traumas and acute neurological events cause the steepest decline in club efficiency. **Shoulder injuries** (average PDI = +1.25 points lost per match), **Knee Surgeries** (PDI = +1.13), **Concussions** (PDI = +1.00), and **Hip Flexor strains** (PDI = +1.00) produce the greatest destabilization, depriving squads of primary tactical focal points.

### 2. What was the team's win/loss record during player absence?
* **Finding:** Across all recorded injuries, team win percentage drops from **44.8%** before injury down to **39.6%** during player absence, while the loss rate increases from **33.2%** to **37.8%**. This decline accounts for an average loss of **0.15 to 0.35 points per match**, which translates to 6–13 points over an entire 38-game league campaign—frequently the difference between European qualification and mid-table stagnation.

### 3. How did individual players perform after recovery?
* **Finding:** Approximately **41.2%** of returning players demonstrate a positive comeback surge (ΔR > +0.10), **24.5%** retain stable form, and **34.3%** suffer a post-injury dip (ΔR < -0.10). Forwards and wingers exhibit greater volatility in comeback ratings compared to central defenders.

### 4. Are there specific months or clubs with frequent injury clusters?
* **Finding:** Pronounced seasonal clustering occurs in **December (89 incidents)** and **January (96 incidents)**, coinciding directly with the Premier League's festive schedule congestion (4–5 matches in 14 days), lower ambient temperatures, and accumulated fatigue.

### 5. Which clubs suffer most due to injuries?
* **Finding:** **Newcastle United** (120 incidents, ~5,800 days lost) and **Everton** (103 incidents, ~4,950 days lost) incurred the highest aggregate injury burden, severely depressing their season efficiency and forcing continuous tactical adjustments.

---

## 🛠️ Data Preprocessing & Cleaning Pipeline

The raw dataset (`player_injuries_impact.csv`) contains 656 rows and 42 columns, characterized by multiple real-world data collection challenges. Our preprocessing pipeline (`src/preprocessing.py`) handles each anomaly:

1. **Character Encoding Preservation (`latin-1`):** Ensures international names with diacritics (e.g., *Fabian Schär*, *Jóhann Berg Gudmundsson*, *Gabriel Magalhães*) are decoded accurately without replacement symbol artifacts.
2. **Text Standardization:** Stripped irregular leading/trailing whitespaces across player names, club designations, and tactical positions (e.g., `'Central Midfielder '` to `'Central Midfielder'`).
3. **Handling Missing Values (`'N.A.'`):** Uniformly converted string `'N.A.'` and blank entries across match results, opponent names, goal differences, and ratings into true `NaN`/`NaT` values.
4. **Rating Parsing & Substitute Annotations:** Removed substitute tags such as `'6(S)'` or `'7.5(S)'` to isolate purely numeric rating floats. Corrected typographic double periods (e.g., `'5..8'` → `5.8`). Zero or unrated entries are coerced to `NaN`.
5. **Goal Difference & Match Outcome Transformation:** Cleaned goal difference columns to numerical floats and converted match outcomes (`'win'`, `'draw'`, `'lose'`) into numeric league points (3, 1, 0).
6. **Date Sanitization & Historical Typo Correction:**
   * Corrected anomalous year entries such as `'Mar 7, 0202'` → `'Mar 7, 2021'`.
   * Corrected chronological inversions in the original recording:
     - *Tanguy Ndombele*: Injury `'2020-01-01'` with typo return `'2019-01-21'` corrected to `'2020-01-21'`.
     - *Matej Vydra*: Injury `'2020-12-18'` with typo return `'2020-01-11'` corrected to `'2021-01-11'`.
   * Handled ongoing injuries marked as `'Present'` cleanly without throwing conversion exceptions.
7. **Feature Engineering:**
   * `Pre_Injury_Avg_Rating` & `Post_Injury_Avg_Rating`
   * `Rating_Improvement` (ΔR)
   * `Pre_Injury_Team_PPM`, `During_Absence_Team_PPM`, `Post_Injury_Team_PPM`
   * `Team_PPM_Drop` & `Team_GD_Drop`
   * `Performance_Drop_Index` (PDI)
   * `Recovery_Days` (Duration in days between return date and injury date)
   * `Injury_Category` (Classified into 12 clinical sports medicine units: *Hamstring*, *Knee / Ligament*, *Ankle*, *Calf / Lower Leg*, *Groin / Pelvis*, *Upper Body*, *Head / Concussion*, *Illness*, etc.)
   * `Position_Group` (*Goalkeeper*, *Defender*, *Midfielder*, *Forward*)
   * `Injury_Month` and `Injury_Year`

---

## 📊 Dashboard Visualizations (5 Core + Bonus Visuals)

The Streamlit dashboard provides 5 interactive charts built with **Plotly**:

1. **Visual 1 (Horizontal Bar Chart):** *Top 10 Injuries with Highest Team Performance Drop* — Identifies which specific diagnoses lead to the largest drop in points per match.
2. **Visual 2 (Interactive Line Chart):** *Player Performance Trajectory Timeline* — Traces 3 pre-injury matches vs. 3 comeback matches with opponent tooltips, baseline averages, and an injury demarcation marker.
3. **Visual 3 (Seasonality Heatmap):** *Injury Frequency Across Months and Clubs* — Visualizes fixture congestion hot-spots across the competitive calendar.
4. **Visual 4 (Scatter Plot with Regression Trend):** *Player Age vs. Team Performance Drop Index* — Examines veteran dependency, colored by tactical position with bubble size scaled by FIFA rating.
5. **Visual 5 (Styled Leaderboard Table):** *Comeback Heroes Leaderboard* — Ranked table displaying players with the highest positive rating surge upon return, with CSV export capabilities.
6. **Bonus Visuals:** *Anatomical Category Donut Chart* and *Match Outcome Distribution Stacked Bar (Pre vs Absence vs Post)*.

---

## 📂 Project Architecture

```
Math For AI 2 SA/
├── app.py                     # Main interactive Streamlit application
├── requirements.txt           # Production environment dependencies
├── README.md                  # Comprehensive documentation and project report
├── player_injuries_impact.csv # Source dataset (656 records, 42 columns)
└── src/
    ├── __init__.py            # Package initialization
    ├── preprocessing.py       # Data cleaning, validation, and feature engineering
    └── visualizations.py      # Plotly interactive chart generation routines
```

---

## 🚀 How to Run Locally

### Prerequisites
* Python 3.10, 3.11, or 3.12 installed.

### Step 1: Clone or Navigate to Directory
```bash
cd "d:/Users/mann/Downloads/Math For AI 2 SA"
```

### Step 2: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Launch Streamlit Application
```bash
streamlit run app.py
```
The application will automatically launch in your browser at `http://localhost:8501`.

---

## ☁️ GitHub & Streamlit Cloud Deployment Guide

Follow these steps to deploy the application for assessment submission:

### Step 1: Create a GitHub Repository
1. Log in to [GitHub](https://github.com/).
2. Click **New Repository**.
3. Set Repository Name adhering to the assignment convention:
   `IADAI102(Student_id)-studentname` (e.g., `IADAI102(12345)-johnsmith`).
4. Set visibility to **Public** (or provide collaborator access to `ai.assignments@wacpinternational.org` as required in the brief).
5. Do not initialize with template files (README is already provided).

### Step 2: Push Local Files to GitHub
Open a terminal in the project directory:
```bash
git init
git add .
git commit -m "feat: complete FootLens player injury and team performance dashboard"
git branch -M main
git remote add origin https://github.com/<YourUsername>/<YourRepositoryName>.git
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud
1. Navigate to [share.streamlit.io](https://share.streamlit.io/).
2. Sign in with your GitHub account.
3. Click **"Deploy an app"** (or **"New app"**).
4. Select your repository: `<YourUsername>/<YourRepositoryName>`.
5. Select branch: `main`.
6. Set Main file path: `app.py`.
7. Click **"Deploy"**.
8. Within 2–3 minutes, your live web application will be live at `https://<your-app-name>.streamlit.app`.

### Step 4: Submission Verification Checklist
* [x] Link to GitHub repository included in the final submission document.
* [x] Collaborator access granted to `ai.assignments@wacpinternational.org`.
* [x] Live Streamlit Cloud app link tested and documented.
* [x] Full student name and registration number entered.

---

## 🎓 Academic Integrity & Course Information
* **Course:** Mathematics for AI-II
* **Assessment:** Summative Assessment (60 Marks)
* **Firm Scenario:** FootLens Analytics (Sports Data Science)
* **Author:** Junior Sports Data Analyst
