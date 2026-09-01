import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sustainability.database import Database
from sustainability.reports import Emissions
from sustainability.utils import DateTimeEncoder


def add_data():

    emissions = Emissions()
    carbon_data = emissions.get_carbon(start_year=2023, end_year=2027)
    emissions.data_transform(data=carbon_data)


db = Database(db_path="aws_carbon_emissions.db")
df = db.read_table(name="emissions")
df["start_date"] = pd.to_datetime(df["start_date"])
df["end_date"] = pd.to_datetime(df["end_date"])
accounts = df["account_id"].unique()

with st.sidebar:
    st.header("Account Selector ☁️")
    selected_accounts = st.multiselect(
        "Select Account(s)",
        options=accounts,
        default=accounts[0] if len(accounts) > 0 else None,
        help="Filter the report by one or more AWS Account IDs."
    )

if selected_accounts:
    filtered_df = df[df["account_id"].isin(selected_accounts)]
else:
    filtered_df = df.copy()

st.title("AWS Account Emissions Report 🌱")

if len(selected_accounts) == 1:
    st.write(f"Account ID: {selected_accounts[0]}")
elif len(selected_accounts) > 1:
    st.write(f"Account IDs: {', '.join(selected_accounts)}")
else:
    st.write("No account selected, showing data from all accounts")

st.dataframe(data=filtered_df, width="stretch", height="auto", hide_index=True)

if len(filtered_df) > 0:
    st.subheader("Monthly Emissions (LBM/MBM) 🍃")
    filtered_df["month"] = filtered_df["start_date"].dt.to_period("M")

    monthly_emissions = (
        filtered_df.groupby(["account_id", "month"])
        .agg({"total_lbm_emissions": "sum", "total_mbm_emissions": "sum"})
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    for account_id in monthly_emissions["account_id"].unique():
        account_data = monthly_emissions[monthly_emissions["account_id"] == account_id]
        ax.plot(
            account_data["month"].astype(str),
            account_data["total_lbm_emissions"],
            marker="o",
            label=f"{account_id} (LBM)"
        )
        ax.plot(
            account_data["month"].astype(str),
            account_data["total_mbm_emissions"],
            marker="o",
            label=f"{account_id} (MBM)"
        )

    ax.set_xlabel("Month")
    ax.set_ylabel("Total Emissions (MTCO2e)")
    ax.set_title("Monthly LBL/MBM Emissions")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("No data available to plot!")
