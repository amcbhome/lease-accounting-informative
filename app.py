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
# Sidebar Contents Menu — Clickable Navigation
# ──────────────────────────────────────────────────────────────
menu = st.sidebar.radio(
    "📑 Contents",
    [
        "1️⃣ Introduction",
        "2️⃣ Scenario",
        "3️⃣ Calculating the Present Value",
        "4️⃣ The Payment Schedule",
        "5️⃣ Updating the Financial Statements"
    ]
)

# ──────────────────────────────────────────────────────────────
# Static dataset (for reference)
# ──────────────────────────────────────────────────────────────
schedule_data = [
    (1, 917_594, 55_056, 80_000, 892_649),
    (2, 892_649, 53_559, 80_000, 866_208),
    (3, 866_208, 51_972, 80_000, 838_181),
    (4, 838_181, 50_291, 80_000, 808_472),
    (5, 808_472, 48_508, 80_000, 776_980),
    (6, 776_980, 46_619, 80_000, 743_599),
    (7, 743_599, 44_616, 80_000, 708_215),
    (8, 708_215, 42_493, 80_000, 670_708),
    (9, 670_708, 40_242, 80_000, 630_950),
    (10, 630_950, 37_857, 80_000, 588_807),
    (11, 588_807, 35_328, 80_000, 544_135),
    (12, 544_135, 32_648, 80_000, 496_784),
    (13, 496_784, 29_807, 80_000, 446_591),
    (14, 446_591, 26_795, 80_000, 393_386),
    (15, 393_386, 23_603, 80_000, 336_989),
    (16, 336_989, 20_219, 80_000, 277_208),
    (17, 277_208, 16_633, 80_000, 213_841),
    (18, 213_841, 12_830, 80_000, 146_671),
    (19, 146_671, 8_800, 80_000, 75_472),
    (20, 75_472, 4_528, 80_000, 0),
]
columns = ["Year", "Opening liability", "Interest (6%)", "Payment", "Closing liability"]
df = pd.DataFrame(schedule_data, columns=columns)
df["Principal repaid"] = df["Payment"] - df["Interest (6%)"]

# ──────────────────────────────────────────────────────────────
# 1. Introduction
# ──────────────────────────────────────────────────────────────
if menu == "1️⃣ Introduction":
    st.header("1️⃣ Introduction")
    st.markdown(
        """
Leases allow a business to use assets such as property, machinery, or vehicles **without purchasing them outright**.  
Under **IFRS 16 – Leases**, most leases are brought **on the balance sheet**, ensuring greater transparency.

Companies must recognise:
- A **Right-of-Use (ROU) asset** – representing the right to use the asset.  
- A **Lease liability** – representing the obligation to make lease payments.

This replaced the previous off-balance-sheet treatment under IAS 17. The effect is:
- **Balance Sheet:** records both asset and liability.  
- **Profit or Loss:** rent expense is replaced by depreciation + interest.  
- **Cash Flow:** split between interest and principal (usually financing).

Accounting for leases under IFRS 16 ensures financial statements reflect the **economic substance** of leasing arrangements rather than their legal form.
        """
    )

# ──────────────────────────────────────────────────────────────
# 2. Scenario
# ──────────────────────────────────────────────────────────────
elif menu == "2️⃣ Scenario":
    st.header("2️⃣ Scenario (based on ACCA example)")
    st.markdown(
        """
A company leases a property for **20 years**, paying **£80,000 per year in arrears** (end of year).  
The **incremental borrowing rate** is **6 %**, and the company incurs **£25,000** in initial direct costs.

This example, adapted from the ACCA article *“IFRS 16 Leases”*, demonstrates the recognition of both the **lease liability** and **right-of-use asset**.
        """
    )

# ──────────────────────────────────────────────────────────────
# 3. Calculating the Present Value
# ──────────────────────────────────────────────────────────────
elif menu == "3️⃣ Calculating the Present Value":
    st.header("3️⃣ Calculating the Present Value")
    st.markdown("To measure the **lease liability**, calculate the present value (PV) of the future lease payments discounted at 6 %:")
    st.latex(r"PV = \sum_{t=1}^{20} \frac{80{,}000}{(1.06)^t} = £917{,}594")
    st.markdown(
        """
Adding **initial direct costs (£25,000)** gives a **Right-of-Use (ROU) asset** of **£942,594**.

💡 *If payments were made at the **start** of each year, the PV would be slightly higher because each payment is discounted for one fewer period.*
        """
    )

# ──────────────────────────────────────────────────────────────
# 4. The Payment Schedule
# ──────────────────────────────────────────────────────────────
elif menu == "4️⃣ The Payment Schedule":
    st.header("4️⃣ The Payment Schedule")
    st.markdown(
        """
Each year the lease liability changes as payments are made.  
This pattern below assumes payments are made at the **end of each year (arrears)**:

- **Interest (6 %)** = Opening × 6 %  
- **Principal repaid** = Payment − Interest  
- **Closing liability** = Opening − Principal  

Example: Year 1 interest £55,056 (6 % of £917,594). Payment £80,000 ⇒ principal £24,944 ⇒ closing £892,649.
        """
    )

    st.dataframe(
        df.style.format({
            "Opening liability": "£{:,.0f}",
            "Interest (6%)": "£{:,.0f}",
            "Payment": "£{:,.0f}",
            "Closing liability": "£{:,.0f}",
            "Principal repaid": "£{:,.0f}",
        }),
        use_container_width=True,
    )

# ──────────────────────────────────────────────────────────────
# 5. Updating the Financial Statements
# ──────────────────────────────────────────────────────────────
elif menu == "5️⃣ Updating the Financial Statements":
    st.header("5️⃣ Updating the Financial Statements")
    y1_interest = df.loc[df["Year"] == 1, "Interest (6%)"].iloc[0]
    y1_principal = df.loc[df["Year"] == 1, "Principal repaid"].iloc[0]
    depreciation = 47_130

    st.markdown(
        """
Under **IFRS 16**, updates to the accounts are made through **journal entries**, which record transactions in the general ledger using nominal codes.
        """
    )

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

    st.subheader("Year 0 — Lease Commencement")
    st.code(
        "Dr 1150 Right-of-Use Asset........£942,594\n"
        "    Cr 2100 Lease Liability................£917,594\n"
        "    Cr 1000 Bank (Initial direct costs)...£25,000",
        language="text"
    )

    st.subheader("Year 1 — End of First Year")
    st.code(
        f"Dr 7500 Interest Expense..............£{y1_interest:,.0f}\n"
        f"Dr 2100 Lease Liability (Principal)...£{y1_principal:,.0f}\n"
        f"    Cr 1000 Bank (Lease Payment)........£80,000\n\n"
        f"Dr 7000 Depreciation Expense..........£{depreciation:,.0f}\n"
        f"    Cr 1150 Accumulated Depreciation....£{depreciation:,.0f}",
        language="text"
    )

    st.markdown(
        """
### How the journals update the statements
- **Profit or Loss:** depreciation and interest recorded as expenses.  
- **Statement of Financial Position:** ROU asset and liability reduced accordingly.  
- **Cash Flow Statement:** principal = financing; interest = operating or financing depending on policy.

### IFRS 16 and Tax Treatment
- Depreciation is a **book expense** only — replaced with **capital allowances** for tax purposes.  
- Interest remains **deductible** as a finance cost.  

### Exempt Leases under IFRS 16
- **Short-term leases (≤ 12 months)**  
- **Low-value assets (e.g., laptops, printers)**  

These are expensed directly to Profit or Loss.
        """
    )

st.success("Use the sidebar menu to navigate each stage of IFRS 16 lease accounting — from introduction to journal-led financial updates.")

