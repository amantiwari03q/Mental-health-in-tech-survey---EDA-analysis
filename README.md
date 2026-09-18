# 🧠 Mental Health in Tech — EDA & Streamlit Dashboard

Exploratory data analysis and an interactive Streamlit dashboard built on the **OSMI Mental Health in Tech Survey** — 1,259 responses from tech-industry employees on mental health attitudes, workplace support, and treatment-seeking behavior.

> 📊 15+ visualizations · 🧹 cleaned & normalized data · 🖥️ interactive multi-tab dashboard · 🚀 ready to deploy

---

## 📁 Project Structure

```
.
├── mental_health_eda.ipynb   # Full EDA notebook (Jupyter)
├── data/
│   └── survey.csv            # Raw dataset
└── app/
    ├── app.py                # Streamlit dashboard
    ├── requirements.txt      # App dependencies
    ├── data/
    │   └── survey.csv        # Dataset bundled with the app
    └── README.md             # App-specific run/deploy instructions
```

## 📊 About the Dataset

The [OSMI Mental Health in Tech Survey](https://osmihelp.org/) measures attitudes towards mental health in the tech workplace. It includes:

- **1,259 rows × 27 columns**
- Demographics: `Age`, `Gender`, `Country`, `state`
- Workplace context: company size, remote work, benefits, wellness programs, anonymity
- Attitudes: comfort discussing mental health with coworkers/supervisors, perceived consequences
- Outcome variable: `treatment` — whether the respondent sought treatment for a mental health condition

The raw data has known quality issues (e.g. `Age` values like `-1726` and `99999999999`, and ~49 free-text spellings of `Gender`) — both are cleaned in the notebook and the app.

## 📓 Notebook: `mental_health_eda.ipynb`

A step-by-step EDA covering:

1. Data loading & structure overview
2. Missing value analysis
3. Data cleaning — Age outlier removal, Gender normalization
4. Univariate analysis — Age, Gender, Country, company size, remote work, treatment, family history, work interference, workplace support indicators
5. Bivariate analysis — Age/Gender/family history/work-interference vs treatment, comfort discussing mental health, mental vs physical health consequence perception
6. Correlation heatmap of encoded categorical variables
7. Key takeaways

Run it with Jupyter:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
jupyter notebook mental_health_eda.ipynb
```

## 🖥️ Dashboard: `app/app.py`

An interactive 5-tab Streamlit dashboard:

| Tab | Contents |
|---|---|
| 📊 Overview | Age distribution, treatment split, gender & country breakdown |
| 👥 Demographics | Age by gender, treatment rate by gender, age by country |
| 🏢 Workplace | Company size, remote work, benefits/wellness/anonymity, comfort with coworkers/supervisor |
| 💊 Treatment Analysis | Work interference vs treatment, family history vs treatment, mental vs physical consequence, correlation heatmap |
| 🗂️ Raw Data | Filtered table with CSV export |

Sidebar filters: **Gender**, **Country**, **Age range**, **Treatment status** — everything updates live.

### Run locally

```bash
cd app
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

### Deploy for free — Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select this repo, and set the main file path to `app/app.py`.
4. Click **Deploy** — you'll get a public `*.streamlit.app` URL in a couple of minutes.

Other options (Docker, Render, Railway, Hugging Face Spaces) are in [`app/README.md`](app/README.md).

## 🔑 Key Takeaways

- Family history of mental illness is the strongest correlate of treatment-seeking.
- Respondents whose mental health "often" interferes with work are far more likely to have sought treatment.
- Comfort discussing mental health is consistently lower than for physical health.
- The sample skews male (~79% after normalization) and is dominated by the US and UK.
- Awareness of company benefits/wellness programs is inconsistent — many respondents answer "Don't know."

## 🛠️ Tech Stack

`Python` · `pandas` · `numpy` · `matplotlib` / `seaborn` (notebook) · `Streamlit` + `Plotly` (dashboard) · `scikit-learn` (encoding for correlation analysis)

## 📄 License

Add a license of your choice (e.g. MIT) if you plan to make this repo public.
