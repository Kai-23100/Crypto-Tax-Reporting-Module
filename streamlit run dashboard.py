import streamlit as st
import pandas as pd
import datetime
import requests

st.set_page_config(page_title="URA eTax Crypto Integration", layout="wide")

st.title("URA eTax Digital Assets Declaration Module")

# Sidebar for Navigation
menu = ["Crypto Income Entry", "CSV Wallet Upload", "Gain/Loss Calculator", "Compliance Alerts", "Summary"]
choice = st.sidebar.radio("Navigate", menu)

# Helper function to fetch crypto price (demo: CoinGecko API)
def fetch_price(token_id, date):
    try:
        date_str = date.strftime("%d-%m-%Y")
        url = f"https://api.coingecko.com/api/v3/coins/{token_id}/history?date={date_str}"
        response = requests.get(url)
        data = response.json()
        price = data["market_data"]["current_price"]["ugx"]
        return price
    except Exception:
        return None

# Data container to store user entries in session state
if "crypto_data" not in st.session_state:
    st.session_state.crypto_data = []

if choice == "Crypto Income Entry":
    st.header("Enter Crypto Income Details")

    income_category = st.selectbox("Income Category", [
        "Crypto Trading Income",
        "Staking & Yield Farming Income",
        "Mining Income",
        "NFT Royalties & Sales",
        "DeFi Lending/Borrowing"
    ])

    entry = {"Income Category": income_category}

    if income_category == "Crypto Trading Income":
        entry["Transaction Type"] = st.selectbox("Transaction Type", ["Buy", "Sell", "Swap"])
        entry["Token Name"] = st.text_input("Token Name (e.g., BTC, ETH)")
        entry["Date"] = st.date_input("Transaction Date", datetime.date.today())
        entry["Value (UGX)"] = st.number_input("Value in UGX", min_value=0.0, format="%.2f")

    elif income_category == "Staking & Yield Farming Income":
        entry["Platform Used"] = st.text_input("Platform (e.g., Binance Staking)")
        entry["Annual Percentage Yield (APY)"] = st.number_input("APY (%)", min_value=0.0, max_value=100.0, format="%.2f")
        entry["Asset Earned"] = st.text_input("Asset Earned (e.g., ADA)")
        entry["Total Receipts (UGX)"] = st.number_input("Total Receipts in UGX", min_value=0.0, format="%.2f")

    elif income_category == "Mining Income":
        entry["Mining Type"] = st.selectbox("Proof Type", ["Proof-of-Work", "Proof-of-Stake"])
        entry["Mined Asset"] = st.text_input("Mined Asset (e.g., ETH)")
        entry["Wallet Address"] = st.text_input("Wallet Address")
        entry["Quantity Mined"] = st.number_input("Quantity Mined", min_value=0.0, format="%.6f")
        entry["Valuation (UGX)"] = st.number_input("Valuation in UGX", min_value=0.0, format="%.2f")

    elif income_category == "NFT Royalties & Sales":
        entry["Smart Contract Address"] = st.text_input("Smart Contract Address")
        entry["NFT ID"] = st.text_input("NFT ID")
        entry["Sale Price (UGX)"] = st.number_input("Sale Price in UGX", min_value=0.0, format="%.2f")
        entry["Resale Chain"] = st.text_input("Resale Chain")
        entry["Royalty Rate (%)"] = st.number_input("Royalty Rate (%)", min_value=0.0, max_value=100.0, format="%.2f")

    elif income_category == "DeFi Lending/Borrowing":
        entry["Protocol Used"] = st.text_input("Protocol (e.g., Aave)")
        entry["Asset Lent/Borrowed"] = st.text_input("Asset Lent/Borrowed")
        entry["Income Earned (UGX)"] = st.number_input("Income Earned in UGX", min_value=0.0, format="%.2f")

    if st.button("Add Entry"):
        st.session_state.crypto_data.append(entry)
        st.success("Entry added successfully!")

elif choice == "CSV Wallet Upload":
    st.header("Upload Wallet/Exchange CSV File")

    uploaded_file = st.file_uploader("Upload CSV/Excel from exchange or wallet export", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.write("Preview of Uploaded Data:")
            st.dataframe(df.head())

            # Simple example: Extract token names and amounts for review
            if "Token" in df.columns and "Amount" in df.columns:
                st.write("Tokens and amounts found:")
                st.dataframe(df[["Token", "Amount"]].head())
            else:
                st.warning("CSV does not contain 'Token' and 'Amount' columns for auto parsing.")

        except Exception as e:
            st.error(f"Error reading file: {e}")

elif choice == "Gain/Loss Calculator":
    st.header("Automated Gain/Loss Calculator (Demo)")

    token = st.text_input("Token ID (CoinGecko format, e.g., bitcoin, ethereum)", "bitcoin")
    purchase_date = st.date_input("Purchase Date", datetime.date.today() - datetime.timedelta(days=30))
    sale_date = st.date_input("Sale Date", datetime.date.today())
    purchase_amount = st.number_input("Amount Purchased", min_value=0.0, format="%.6f")
    sale_amount = st.number_input("Amount Sold", min_value=0.0, format="%.6f")

    if st.button("Calculate Gain/Loss"):
        purchase_price = fetch_price(token, purchase_date)
        sale_price = fetch_price(token, sale_date)
        if purchase_price is None or sale_price is None:
            st.error("Could not fetch prices for given dates. Try another token or check your internet connection.")
        else:
            cost_basis = purchase_amount * purchase_price
            realization = sale_amount * sale_price
            gain_loss = realization - cost_basis
            st.write(f"Purchase Price on {purchase_date}: UGX {purchase_price:,.2f}")
            st.write(f"Sale Price on {sale_date}: UGX {sale_price:,.2f}")
            st.write(f"Cost Basis: UGX {cost_basis:,.2f}")
            st.write(f"Realization Value: UGX {realization:,.2f}")
            st.success(f"Net Gain/Loss: UGX {gain_loss:,.2f}")

elif choice == "Compliance Alerts":
    st.header("Automated Compliance & Risk Alerts")

    # For demo, we simulate some alerts based on dummy logic
    if len(st.session_state.crypto_data) == 0:
        st.info("No crypto income entries yet to analyze.")
    else:
        alerts = []
        total_value = 0
        for entry in st.session_state.crypto_data:
            val = entry.get("Value (UGX)") or entry.get("Total Receipts (UGX)") or entry.get("Valuation (UGX)") or entry.get("Sale Price (UGX)") or entry.get("Income Earned (UGX)") or 0
            if val and val > 10_000_000:
                alerts.append(f"High-value transaction detected in {entry['Income Category']}: UGX {val:,.2f}")

            total_value += val if val else 0

        if total_value == 0:
            st.success("All entries appear below the reporting threshold. Good compliance!")
        else:
            for alert in alerts:
                st.warning(alert)

elif choice == "Summary":
    st.header("Summary of Crypto Income Entries")
    if len(st.session_state.crypto_data) == 0:
        st.info("No crypto income entries yet.")
    else:
        df_summary = pd.DataFrame(st.session_state.crypto_data)
        st.dataframe(df_summary)

        total_ugx = 0
        for col in df_summary.columns:
            if "UGX" in col:
                total_ugx += df_summary[col].sum()

        st.write(f"**Total Declared Crypto Income (UGX):** {total_ugx:,.2f}")

st.markdown("""
---
### Notes:
- This demo app models core components of URA’s crypto integration.
- Real implementation requires secure backend, authentication, data validation, and integration with URA systems.
- APIs used (CoinGecko) are public and may have limitations.
- Automated gain/loss calculator here is simplified; official logic must follow TPCA and URA guidelines.
""")
