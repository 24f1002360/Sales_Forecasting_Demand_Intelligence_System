import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px



st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📈",
    layout="wide"
)

@st.cache_data
def load_data():

    df = pd.read_csv("train.csv")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True
    )

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.month_name()

    return df


df = load_data()

forecast_df = pd.read_csv("forecast_table.csv")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Sales Overview",
        "Forecast Explorer",
        "Anomaly Report",
        "Demand Segments"
    ]
)

if page == "Sales Overview":

    st.title("📊 Sales Overview Dashboard")

    st.markdown(
        "Interactive overview of Superstore sales performance."
    )


    total_sales = df["Sales"].sum()

    total_orders = len(df)

    total_categories = df["Category"].nunique()

    avg_sales = df["Sales"].mean()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Total Sales",
        f"${total_sales:,.0f}"
    )

    c2.metric(
        "Orders",
        total_orders
    )

    c3.metric(
        "Categories",
        total_categories
    )

    c4.metric(
        "Average Order Value",
        f"${avg_sales:.2f}"
    )

    st.divider()


    yearly = (
        df.groupby("Year")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        yearly,
        x="Year",
        y="Sales",
        text_auto=True,
        title="Total Sales by Year"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    monthly = (
        df.groupby(
            pd.Grouper(
                key="Order Date",
                freq="ME"
            )
        )["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        monthly,
        x="Order Date",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )

    st.divider()


    st.subheader("Interactive Filters")

    col1,col2 = st.columns(2)

    region = col1.selectbox(
        "Select Region",
        ["All"] + list(df["Region"].unique())
    )

    category = col2.selectbox(
        "Select Category",
        ["All"] + list(df["Category"].unique())
    )

    filtered = df.copy()

    if region != "All":

        filtered = filtered[
            filtered["Region"]==region
        ]

    if category != "All":

        filtered = filtered[
            filtered["Category"]==category
        ]

    summary = (
        filtered.groupby(
            ["Region","Category"]
        )["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.bar(
        summary,
        x="Region",
        y="Sales",
        color="Category",
        barmode="group",
        title="Sales by Region and Category"
    )

    st.plotly_chart(
        fig3,
        width="stretch"
    )

elif page=="Forecast Explorer":

    st.title("📈 Forecast Explorer")

    st.markdown(
        "Forecast generated using the best-performing XGBoost model."
    )

    option = st.selectbox(

        "Forecast Type",

        [
            "Furniture",
            "Technology",
            "Office Supplies",
            "West",
            "East"
        ]

    )

    horizon = st.slider(

        "Forecast Horizon",

        1,

        3,

        3

    )

    values = forecast_df.loc[
        forecast_df.iloc[:,0]==option
    ].iloc[:,1:4].values.flatten()

    months = [
        "Month 1",
        "Month 2",
        "Month 3"
    ]

    chart = pd.DataFrame({

        "Month":months[:horizon],

        "Forecast Sales":values[:horizon]

    })

    fig = px.line(

        chart,

        x="Month",

        y="Forecast Sales",

        markers=True,

        title=f"{option} Forecast"

    )

    st.plotly_chart(

        fig,

        width="stretch"

    )

    st.subheader("Forecast Values")

    st.dataframe(chart)

    st.subheader("Model Performance")

    m1,m2 = st.columns(2)

    m1.metric(

        "MAE",

        "14763.81"

    )

    m2.metric(

        "RMSE",

        "18337.41"

    )

    st.success(

        "XGBoost achieved the lowest prediction error among all forecasting models and was selected as the production model."

    )
elif page == "Anomaly Report":

    st.title("🚨 Sales Anomaly Report")

    st.markdown(
        """
        This page highlights unusual weekly sales detected using
        statistical anomaly detection.
        """
    )

    weekly = (
        df.groupby(
            pd.Grouper(
                key="Order Date",
                freq="W"
            )
        )["Sales"]
        .sum()
        .reset_index()
    )

    Q1 = weekly["Sales"].quantile(0.25)
    Q3 = weekly["Sales"].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    weekly["Anomaly"] = (
        (weekly["Sales"] < lower) |
        (weekly["Sales"] > upper)
    )

    fig = px.line(
        weekly,
        x="Order Date",
        y="Sales",
        title="Weekly Sales with Detected Anomalies",
        markers=True
    )

    anomalies = weekly[weekly["Anomaly"]]

    fig.add_scatter(
        x=anomalies["Order Date"],
        y=anomalies["Sales"],
        mode="markers",
        marker=dict(
            color="red",
            size=12,
            symbol="x"
        ),
        name="Anomaly"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.subheader("Detected Anomalies")

    anomaly_table = anomalies.copy()

    anomaly_table["Order Date"] = (
        anomaly_table["Order Date"]
        .dt.strftime("%d-%m-%Y")
    )

    anomaly_table = anomaly_table.rename(
        columns={
            "Order Date":"Date",
            "Sales":"Weekly Sales"
        }
    )

    st.dataframe(
        anomaly_table,
        width="stretch"
    )

    st.metric(
        "Total Anomalies Detected",
        len(anomaly_table)
    )

    csv = anomaly_table.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        " Download Anomaly Report",
        csv,
        "anomaly_report.csv",
        "text/csv"
    )

    st.success(
        "Red markers indicate unusually high or low weekly sales."
    )
    
elif page == "Demand Segments":

    st.title("📦 Product Demand Segmentation")

    st.markdown(
        """
        Products are grouped according to their
        demand behaviour using clustering.
        """
    )

    cluster_df = pd.read_csv("cluster_df.csv")

    cluster_df["Cluster"] = (
        cluster_df["Cluster"]
        .astype(str)
    )

    fig = px.scatter(
    cluster_df,
    x="PC1",
    y="PC2",
    color="Cluster Name",
    hover_name="Sub-Category",
    size="Total Sales",
    title="Demand Segments"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    
    st.subheader("Product Segments")

    st.dataframe(

        cluster_df[
    [
        "Sub-Category",
        "Cluster Name"
    ]
    ],

        width="stretch"

    )

    counts = (
    cluster_df["Cluster Name"]
    .value_counts()
    .reset_index()
    )

    counts.columns = [
        "Segment",
        "Products"
    ]

    fig2 = px.bar(
        counts,
        x="Segment",
        y="Products",
        text_auto=True,
        title="Products per Demand Segment"
    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )

    csv = cluster_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        " Download Cluster Results",
        csv,
        "cluster_results.csv",
        "text/csv"
    )

    st.success(
        "Use these demand segments to decide stocking strategies."
    )