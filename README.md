# 📈 Sales Forecasting Dashboard

An interactive Streamlit dashboard for sales forecasting and business analytics using the Superstore dataset. The application provides historical sales analysis, forecasting, anomaly detection, and product demand segmentation to support data-driven business decisions.

---

## Features

### 📊 Sales Overview
- Key business KPIs
- Year-wise sales analysis
- Monthly sales trend
- Region and category filters

### 📈 Forecast Explorer
- Sales forecast for categories and regions
- Forecast horizon selection (1–3 months)
- Model performance summary

### 🚨 Sales Anomaly Report
- Weekly anomaly detection
- Interactive anomaly visualization
- Downloadable anomaly report

### 📦 Demand Segmentation
- Product clustering visualization
- Demand segment identification
- Downloadable cluster results

---

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- XGBoost

---

## Dataset

Superstore Sales Dataset

Additional generated files:

- `forecast_table.csv`
- `cluster_df.csv`

---

## Project Structure

```text
Sales-Forecasting-Dashboard/
│
├── app.py
├── requirements.txt
├── train.csv
├── forecast_table.csv
├── cluster_df.csv
├── screenshots/
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/Sales-Forecasting-Dashboard.git
```

Go to the project folder

```bash
cd Sales-Forecasting-Dashboard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## Dashboard Pages

- Sales Overview
- Forecast Explorer
- Anomaly Report
- Demand Segmentation

---

## Future Improvements

- Real-time forecasting
- Interactive filtering
- Cloud deployment
- User authentication

---

## Author

Kanchan
