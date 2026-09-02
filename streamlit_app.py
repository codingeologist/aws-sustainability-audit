"""Streamlit Module"""
import pandas as pd
import streamlit as st
import plotly.express as px
from sustainability.database import Database
from sustainability.utils import theming
theming()


db = Database(db_path="aws_carbon_emissions.db")
df = db.read_table(name="emissions")
df["start_date"] = pd.to_datetime(df["start_date"])
df["end_date"] = pd.to_datetime(df["end_date"])
accounts = df["account_id"].unique()

st.title("AWS Account Emissions Report 🌱")

with st.sidebar:
    st.header("Account Selector ☁️")
    selected_accounts = st.multiselect(
        "Select Account(s)",
        options=accounts,
        default=None,
        help="Filter the report by one or more AWS Account IDs."
    )

if selected_accounts:
    filtered_df = df[df["account_id"].isin(selected_accounts)]
    if len(selected_accounts) == 1:
        st.write(f"Account ID: {selected_accounts[0]}")
    else:
        st.write(f"Account IDs: {', '.join(selected_accounts)}")

else:
    filtered_df = (
        df.groupby(["start_date", "end_date", "region", "model", "unit"])
        .agg({
            "total_lbm_emissions": "sum",
            "total_mbm_emissions": "sum"
        })
        .reset_index()
    )
    filtered_df.insert(0, "account_id", "aggregated")
    st.write("Showing aggregated data from all accounts")

st.dataframe(data=filtered_df, width="stretch", height="auto", hide_index=True)

if len(filtered_df) > 0:
    st.subheader("Monthly Emissions (LBM/MBM) 🍃")
    filtered_df["month"] = filtered_df["start_date"].dt.strftime("%Y-%m")

    monthly_emissions = (
        filtered_df.groupby(["account_id", "month"])
        .agg({"total_lbm_emissions": "sum", "total_mbm_emissions": "sum"})
        .reset_index()
    )

    melted_df = monthly_emissions.melt(
        id_vars=["account_id", "month"],
        value_vars=["total_lbm_emissions", "total_mbm_emissions"],
        var_name="emission_type",
        value_name="emissions"
    )
    melted_df["emission_type"] = melted_df["emission_type"].replace({
        "total_lbm_emissions": "LBM",
        "total_mbm_emissions": "MBM"
    })

    fig1 = px.line(
        melted_df,
        x="month",
        y="emissions",
        color="account_id",
        line_dash="emission_type",
        title="Monthly LBM/MBM Emissions",
        labels={
            "month": "Month",
            "emissions": "Total Emissions (MTCO2e)"
        },
        hover_data={
            "month": True,
            "emissions": ":.4f"
        }
    )

    greens = ["#2ecc71", "#27ae60", "#1e8449", "#196f3d", "#0e6251"]
    reds = ["#e74c3c", "#c0392b", "#992d22", "#78281f", "#5e1914"]

    for i, trace in enumerate(fig1.data):
        # LBM solid lines
        if trace.line.dash == "solid":
            fig1.data[i].line.color = reds[i % len(reds)]
        # MBM dashed lines
        else:
            fig1.data[i].line.color = greens[i % len(greens)]

    fig1.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Emissions (MTCO2e)",
        legend_title="Account & Emission Type",
        hovermode="x unified"
    )

    st.plotly_chart(fig1, width="stretch")

    st.subheader("Emissions by Region 🌍")

    region_emissions = (
        filtered_df.groupby(["account_id", "region"])
        .agg({"total_lbm_emissions": "sum"})
        .reset_index()
    )

    fig2 = px.pie(
        region_emissions,
        names="region",
        values="total_lbm_emissions",
        facet_col="account_id",
        title="Emissions by Region per Account",
        hole=0.3
    )

    fig2.update_traces(textposition="inside", textinfo="percent+label")
    fig2.update_layout(
        showlegend=True,
        height=600,
        width=1200,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig2, width="stretch")

else:
    st.warning("No data available to plot!")
