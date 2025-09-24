import streamlit as st
import pandas as pd
import xlrd
import io
from datetime import datetime

# Reuse your financial_fields and processing logic
financial_fields = [
    "Net Revenue", "Cost of Materials Consumed", "Gross Profit Margin (%)",
    "EBITDA Margin (%)", "Depreciation and Amortization Expense",
    "Finance Costs", "Profit for the Period", "Total Non-current Liabilities",
    "Total Current Liabilities", "Total Equity", "Intangible Assets",
    "Current Ratio", "Short Term Borrowings", "Long Term Borrowings",
    "Operating Profit ( EBITDA )", "Interest Coverage Ratio",
    "Payables / Sales (Days)", "Debtors / Sales (Days)",
    "Inventory / Sales (Days)", "Cash Conversion Cycle (Days)",
    "Return on Capital Employed (%)", "Return on Equity (%)",
    "Total Net Fixed Assets"
]

def process_files(uploaded_files):
    output_data = []
    for uploaded_file in uploaded_files:
        try:
            wb_about = xlrd.open_workbook(file_contents=uploaded_file.read())

            # Sheet 1: "About the Company"
            about_sheet = wb_about.sheet_by_name("About the Company")
            company_name = about_sheet.cell_value(0, 1)

            # Date of Incorporation Lookup
            incorporation_date = None
            for row in range(about_sheet.nrows):
                if str(about_sheet.cell_value(row, 0)).strip() == "Date of Incorporation":
                    incorporation_date = str(about_sheet.cell_value(row, 1)).strip()
                    break

            incorporation_year = None
            vintage_years = None
            if incorporation_date:
                try:
                    parsed_date = datetime.strptime(incorporation_date, "%d %b, %Y")
                    incorporation_year = parsed_date.year
                    vintage_years = datetime.now().year - incorporation_year
                except:
                    incorporation_year = incorporation_date

            # Sheet 2: "Standalone Financial Data"
            fin_sheet = wb_about.sheet_by_name("Standalone Financial Data")

            latest_col = None
            date_of_report = None
            for col in reversed(range(fin_sheet.ncols)):
                if fin_sheet.cell_value(0, col):
                    latest_col = col
                    date_of_report = str(fin_sheet.cell_value(0, col)).strip()
                    break

            fin_data = {}
            for row in range(fin_sheet.nrows):
                key = str(fin_sheet.cell_value(row, 0)).strip()
                if key in financial_fields:
                    try:
                        val = fin_sheet.cell_value(row, latest_col)
                        val = float(val) if isinstance(val, (int, float)) else None
                    except:
                        val = None
                    fin_data[key] = val

            # Derived calculations (same as your script)
            net_revenue = fin_data.get("Net Revenue", 0)
            depreciation = fin_data.get("Depreciation and Amortization Expense", 0)
            finance_costs = fin_data.get("Finance Costs", 0)
            pat = fin_data.get("Profit for the Period", 0)
            total_non_current = fin_data.get("Total Non-current Liabilities", 0)
            total_current = fin_data.get("Total Current Liabilities", 0)
            total_equity = fin_data.get("Total Equity", 0)
            intangible_assets = fin_data.get("Intangible Assets", 0)
            current_ratio = fin_data.get("Current Ratio", 0)
            short_term = fin_data.get("Short Term Borrowings", 0)
            long_term = fin_data.get("Long Term Borrowings", 0)
            ebitda = fin_data.get("Operating Profit ( EBITDA )", 0)
            cost_of_materials = fin_data.get("Cost of Materials Consumed", 0)
            gross_margin = fin_data.get("Gross Profit Margin (%)", 0) / 100 if fin_data.get("Gross Profit Margin (%)") else None

            total_outside_liabilities = total_non_current + total_current
            tangible_net_worth = total_equity - intangible_assets
            tol_tnw = total_outside_liabilities / tangible_net_worth if tangible_net_worth else None
            total_debt = short_term + long_term
            debt_ebitda = total_debt / ebitda if ebitda else None
            depreciation_pct = depreciation / net_revenue if net_revenue else None
            finance_pct = finance_costs / net_revenue if net_revenue else None
            pat_margin = pat / net_revenue if net_revenue else None
            fatr = net_revenue / fin_data.get("Total Net Fixed Assets", 0) if fin_data.get("Total Net Fixed Assets", 0) else None

            output_data.append({
                "Company Name": company_name,
                "Net Revenue": net_revenue,
                "Gross Margin(%)": gross_margin,
                "EBITDA (%)": fin_data.get("EBITDA Margin (%)")/100 if fin_data.get("EBITDA Margin (%)") else None,
                "Depreciation (% of sales)": depreciation_pct,
                "Finance Cost (% of sales)": finance_pct,
                "PAT %": pat_margin,
                "TOL": total_outside_liabilities,
                "TNW": tangible_net_worth,
                "Current Ratio": current_ratio,
                "TOL/TNW ": tol_tnw,
                "Debt": total_debt,
                "Debt/EBITDA": debt_ebitda,
                "Interest Coverage Ratio": fin_data.get("Interest Coverage Ratio"),
                "Payables (Days)": fin_data.get("Payables / Sales (Days)"),
                "Debtors (Days)": fin_data.get("Debtors / Sales (Days)"),
                "Inventory (Days)": fin_data.get("Inventory / Sales (Days)"),
                "CCC (Days)": fin_data.get("Cash Conversion Cycle (Days)"),
                "ROCE (%)": fin_data.get("Return on Capital Employed (%)")/100 if fin_data.get("Return on Capital Employed (%)") else None,
                "ROE (%)": fin_data.get("Return on Equity (%)")/100 if fin_data.get("Return on Equity (%)") else None,
                "Fixed Asset Turnover Ratio": fatr,
                "Net Fixed Assets": fin_data.get("Total Net Fixed Assets"),
                "Vintage (Years)": vintage_years,
                "Date of Incorporation": incorporation_date,
                "Date of Report": date_of_report,
                "Cost of Materials Consumed": cost_of_materials
            })
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")

    return pd.DataFrame(output_data)

# ------------------- Streamlit UI -------------------
st.title("📊 Probe Data Processor")

uploaded_files = st.file_uploader(
    "Upload multiple Financial Excel (.xls) files",
    type=["xls"],
    accept_multiple_files=True
)

if uploaded_files:
    df = process_files(uploaded_files)
    df = df.sort_values(by="Net Revenue", ascending=False)
    cols_to_round = [
        "Gross Margin(%)", "EBITDA (%)", "Depreciation (% of sales)",
        "Finance Cost (% of sales)", "PAT %", "TOL/TNW ", 
        "Debt/EBITDA", "ROCE (%)", "ROE (%)", "Fixed Asset Turnover Ratio"
    ]
    for col in cols_to_round:
        if col in df.columns:
            df[col] = df[col].round(3)
    st.dataframe(df)

    # Save output to Excel in memory
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    st.download_button(
        label="📥 Download Processed Excel",
        data=output,
        file_name="financial_summary_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
