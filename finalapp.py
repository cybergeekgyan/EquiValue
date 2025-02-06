import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch stock financial data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    try:
        data = {
            "Current Price": info.get("currentPrice", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "Revenue": info.get("totalRevenue", "N/A"),
            "Net Income": info.get("netIncomeToCommon", "N/A"),
            "Free Cash Flow": info.get("freeCashflow", "N/A"),
            "EPS": info.get("trailingEps", "N/A"),
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "TTM P/E": info.get("forwardPE", "N/A"),
            "P/B Ratio": info.get("priceToBook", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "EV/EBITDA": info.get("enterpriseToEbitda", "N/A"),
            "Beta": info.get("beta", "N/A"),
            "Face Value": info.get("bookValue", "N/A"),
            "Sector P/E": info.get("industryKeyStats", {}).get("peRatio", "N/A"),
            "Debt-to-Equity": info.get("debtToEquity", "N/A"),
            "ROA": info.get("returnOnAssets", "N/A"),
            "ROE": info.get("returnOnEquity", "N/A"),
            "ROCE": info.get("returnOnCapitalEmployed", "N/A"),
            "ROIC": info.get("returnOnInvestedCapital", "N/A"),
            "Change in Promoter Holding": info.get("changeInPromotersHolding", "N/A"),
            "Shares Outstanding": info.get("sharesOutstanding", "N/A"),
        }
        return data
    except Exception as e:
        return {"Error": str(e)}

# Streamlit UI
st.title("📊 Indian Stock Valuation Calculator")
st.sidebar.header("Select Valuation Methods")
valuation_method = st.sidebar.multiselect(
    "Choose Methods",
    ["DCF Valuation", "P/E Ratio Comparison", "Dividend Discount Model (DDM)", "EV/EBITDA Valuation"]
)

# User Input for Stock Ticker
stock_ticker = st.text_input("Enter Stock Ticker (e.g., TCS.NS, INFY.NS)")

if st.button("Search"):
    if stock_ticker:
        stock_data = get_stock_data(stock_ticker)

        if "Error" in stock_data:
            st.error("Error fetching data. Please check the ticker symbol.")
        else:
            st.write("### Stock Financials")
            st.json(stock_data)

            # Display Key Financial Metrics
            st.write("### 📊 Key Financial Metrics")
            metrics_df = pd.DataFrame(
                [
                    ["ROA (Return on Assets)", stock_data["ROA"]],
                    ["ROE (Return on Equity)", stock_data["ROE"]],
                    ["ROCE (Return on Capital Employed)", stock_data["ROCE"]],
                    ["ROIC (Return on Invested Capital)", stock_data["ROIC"]],
                    ["Debt-to-Equity Ratio", stock_data["Debt-to-Equity"]],
                    ["Beta (Stock Volatility)", stock_data["Beta"]],
                    ["Face Value (₹)", stock_data["Face Value"]],
                    ["Sector P/E", stock_data["Sector P/E"]],
                    ["TTM P/E Ratio", stock_data["TTM P/E"]],
                    ["Change in Promoter Holding (%)", stock_data["Change in Promoter Holding"]],
                ],
                columns=["Metric", "Value"],
            )
            st.table(metrics_df)

            # Stock Valuation Methods
            if "DCF Valuation" in valuation_method and stock_data["Free Cash Flow"] != "N/A":
                fcf = stock_data["Free Cash Flow"]
                intrinsic_value = fcf * 10  # Simplified DCF calculation
                intrinsic_per_share = intrinsic_value / stock_data["Shares Outstanding"]

                st.write("### 📈 DCF Valuation")
                st.write(f"**Intrinsic Value per Share:** ₹{intrinsic_per_share:.2f}")

            if "P/E Ratio Comparison" in valuation_method and stock_data["P/E Ratio"] != "N/A":
                fair_value_pe = stock_data["EPS"] * 15  # Assuming fair P/E of 15
                st.write("### 📊 P/E Ratio Valuation")
                st.write(f"**Fair Value per Share (P/E Method):** ₹{fair_value_pe:.2f}")

            if "Dividend Discount Model (DDM)" in valuation_method and stock_data["Dividend Yield"] != "N/A":
                intrinsic_ddm = (stock_data["Dividend Yield"] * 100) / 0.07  # Assuming 7% discount rate
                st.write("### 💰 Dividend Discount Model (DDM)")
                st.write(f"**Intrinsic Value per Share (DDM):** ₹{intrinsic_ddm:.2f}")

            if "EV/EBITDA Valuation" in valuation_method and stock_data["EV/EBITDA"] != "N/A":
                ev_ebitda_value = stock_data["EV/EBITDA"] * stock_data["Net Income"]
                st.write("### 🏢 EV/EBITDA Valuation")
                st.write(f"**Fair Value based on EV/EBITDA:** ₹{ev_ebitda_value:.2f}")

    else:
        st.error("Please enter a valid stock ticker!")
