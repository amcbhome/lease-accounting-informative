import streamlit as st
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────────────────────
# Page setup
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="IFRS 16 — Lease Accounting Made Simple", layout="wide")
st.title("📘 IFRS 16 — Lease Accounting Made Simple")
st.caption("An interactive teaching resource explaining the accounting for leases under IFRS 16 using a clear, stage-by-stage approach.")

# ──────────────────────────────────────────────────────────────
# Sidebar menu — clickable navigation
# ──────────────────────────────────────────────────────────────
menu = st.sidebar.radio(
    "📑 Contents",
    [
        "1️⃣ Introduction",
        "2️⃣ Scenario",
        "3️⃣ Calculating the Present Value",
        "4️⃣ The Payment Schedule",
        "5️⃣ Updating the Financial Statements",
    ]
)

# ──────────────────────────────────────────────────────────────
# 1️⃣ Introduction
# ──────────────────────────────────────────────────────────────
if menu == "1️⃣ Introduction":
    st.header("1️⃣ Introduction")
    st.markdown(
        """
Leases allow a business to use assets such as property, machinery, or vehicles **without purchasing them outright**.  
Under **IFRS 16 – Leases**, most leases are brought **on the balance sheet**, ensuring greater transparency.

Companies must recognise:
- A **Right-of-Use (ROU) asset** – representing the right to use the asset  
- A **Lease liability** – representing the obligation to make lease payments  

This replaced the previous off-balance-sheet treatment under IAS 17.

**Financial statement impact**
- **Statement of Financial Position:** records both asset and liability  
- **Profit or Loss:** rent expense replaced by depreciation + interest  
- **Cash Flow:** payments split between interest and principal  

Accounting under IFRS 16 ensures that the financial statements reflect the **economic substance** of leasing arrangements rather than their legal form.
        """
    )

# ──────────────────────────────────────────────────────────────
# 2️⃣ Scenario
# ──────────────────────────────────────────────────────────────
elif menu == "2️⃣ Scenario":
    st.header("2️⃣ Scenario (based on ACCA example)")
    st.markdown(
        """
A company leases a property for **20 years**, paying **£80 000 per year in arrears** (end of year).  
The **incremental borrowing rate** is **6 %**, and the company incurs **£25 000** in initial direct costs.

This scenario, adapted from the ACCA article *“IFRS 16 Leases”*, demonstrates the recognition of both the **lease liability** and **Right-of-Use asset**.
        """
    )

# ──────────────────────────────────────────────────────────────
# 3️⃣ Calculating the Present Value
# ──────────────────────────────────────────────────────────────
elif menu == "3️⃣ Calculating the Present Value":
    st.header("3️⃣ Calculating the Present Value")
    st.markdown("To measure the **lease liability**, calculate the present value (PV) of future lease payments discounted at 6 %:")
    st.latex(r"PV = \sum_{t=1}^{20} \frac{80{,}000}{(1.06)^t} = £917{,}594")
    st.markdown(
        """
Adding **initial direct costs (£25 000)** gives a **Right-of-Use (ROU) asset** of **£942 594**.

💡 *If payments were made at the **start** of each year, the PV would be slightly higher because each payment is discounted for one fewer period.*
        """
    )

# ──────────────────────────────────────────────────────────────
# 4️⃣ The Payment Schedule — automatic calculation
# ──────────────────────────────────────────────────────────────
elif menu == "4️⃣ The Payment Schedule":
    st.header("4️⃣ The Payment Schedule (Auto-Generated)")

    # Inputs
    n = 20           # years
    r = 0.06         # rate
    payment = 80_000 # annual
    pv = payment * (1 - (1 + r) ** -n) / r  # initial liability
    depreciation = (pv + 25_000) / n        # ROU straight-line

    # Build amortisation schedule
    rows = []
    liability = pv
    for t in range(1, n + 1):
        interest = liability * r
        principal = payment - interest
        closing = liability - principal
        rows.append((t, liability, interest, payment, principal, closing))
        liability = closing

    df = pd.DataFrame(rows, columns=[
        "Year", "Opening liability", "Interest (6%)",
        "Payment", "Principal repaid", "Closing liability"
    ])

    # Cumulative version
    cdf = df.copy()
    cdf["Cumulative Interest"] = df["Interest (6%)"].cumsum()
    cdf["Cumulative Principal"] = df["Principal repaid"].cumsum()

    st.markdown(
        """
The schedule below is **generated entirely from formulas**, not a manual table.

Each year:
- **Interest (6 %) = Opening × 6 %**  
- **Principal repaid = Payment − Interest**  
- **Closing liability = Opening − Principal**  

The closing liability becomes the next year's opening balance.
        """
    )

    st.dataframe(
        df.style.format({
            "Opening liability": "£{:,.0f}",
            "Interest (6%)": "£{:,.0f}",
            "Payment": "£{:,.0f}",
            "Principal repaid": "£{:,.0f}",
            "Closing liability": "£{:,.0f}",
        }),
        use_container_width=True,
    )

    st.markdown("#### Cumulative totals (optional view)")
    st.dataframe(
        cdf[["Year", "Cumulative Interest", "Cumulative Principal"]]
        .style.format("£{:,.0f}"),
        use_container_width=True,
    )

# ──────────────────────────────────────────────────────────────
# 5️⃣ Updating the Financial Statements — linked to df
# ──────────────────────────────────────────────────────────────
elif menu == "5️⃣ Updating the Financial Statements":
    st.header("5️⃣ Updating the Financial Statements (Linked Journals)")

    # Recalculate df (so Stage 5 works even if user jumps directly here)
    n = 20; r = 0.06; payment = 80_000
    pv = payment * (1 - (1 + r) ** -n) / r
    depreciation = (pv + 25_000) / n
    rows = []
    liability = pv
    for t in range(1, n + 1):
        interest = liability * r
        principal = payment - interest
        closing = liability - principal
        rows.append((t, liability, interest, payment, principal, closing))
        liability = closing
    df = pd.DataFrame(rows, columns=[
        "Year", "Opening liability", "Interest (6%)",
        "Payment", "Principal repaid", "Closing liability"
    ])

    st.markdown(
        """
The journals below are **auto-generated from the payment schedule**,  
so each year's debit and credit entries are linked directly to the calculations above.
        """
    )

    # Nominal codes table
    st.subheader("Nominal Codes (Example Chart of Accounts)")
    st.table({
        "Code": ["1150", "2100", "7000", "7500", "1000"],
        "Account Name": [
            "Right-of-Use Asset",
            "Lease Liability",
            "Depreciation Expense",
            "Interest Expense",
            "Bank"
        ],
        "Type": [
            "Non-current asset",
            "Non-current liability",
            "Expense (P&L)",
            "Finance cost (P&L)",
            "Asset"
        ]
    })

    # Lease commencement entry
    st.subheader("Year 0 — Lease Commencement")
    st.code(
        f"Dr 1150 Right-of-Use Asset........£{pv + 25_000:,.0f}\n"
        f"    Cr 2100 Lease Liability................£{pv:,.0f}\n"
        f"    Cr 1000 Bank (Initial direct costs)...£25,000",
        language="text",
    )

    # Year-by-year journals from df
    st.subheader("📒 Year-by-Year Lease Journals")

    for _, row in df.iterrows():
        year = int(row["Year"])
        interest = row["Interest (6%)"]
        principal = row["Principal repaid"]
        payment = row["Payment"]
        st.markdown(f"**Year {year}**")
        st.code(
            f"Dr 7500 Interest Expense..............£{interest:,.0f}\n"
            f"Dr 2100 Lease Liability (Principal)...£{principal:,.0f}\n"
            f"    Cr 1000 Bank (Lease Payment)........£{payment:,.0f}\n\n"
            f"Dr 7000 Depreciation Expense..........£{depreciation:,.0f}\n"
            f"    Cr 1150 Accumulated Depreciation....£{depreciation:,.0f}",
            language="text",
        )

    st.markdown(
        """
### Summary of Financial Statement Impact
- **Profit or Loss:** records depreciation and interest each year  
- **Statement of Financial Position:** shows reducing ROU asset and liability  
- **Cash Flow:** principal = financing; interest = operating or financing  

### Tax Treatment
- Depreciation is a book expense only (replaced by capital allowances)  
- Interest is normally deductible for tax purposes  

### IFRS 16 Exemptions
Short-term (≤ 12 months) and low-value leases are expensed directly to P&L.
        """
    )

st.success("Use the sidebar menu to navigate each stage of IFRS 16 lease accounting —from introduction to linked journals.")
