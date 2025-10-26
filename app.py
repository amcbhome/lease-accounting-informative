import streamlit as st
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────────────────────
# Page setup
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="IFRS 16 — Lease Accounting Made Simple", layout="centered")
st.title("📘 IFRS 16 — Lease Accounting Made Simple")
st.caption("An interactive teaching resource explaining the accounting for leases under IFRS 16 using a clear, stage-by-stage approach.")

# ──────────────────────────────────────────────────────────────
# CONTENTS PANEL
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📑 Contents")
    st.markdown(
        """
1. Introduction  
2. Scenario  
3. Calculating the Present Value  
4. The Payment Schedule  
5. How to Update the Financial Statements  
        """
    )

# ──────────────────────────────────────────────────────────────
# 1. Introduction
# ──────────────────────────────────────────────────────────────
with st.expander("1️⃣ Introduction", expanded=True):
    st.markdown(
        r"""
Leases are a common way for businesses to access assets such as property, machinery, or vehicles **without purchasing them outright**. Instead, a lessee pays regular instalments to use the asset for an agreed period.

Under **IFRS 16 – Leases**, companies must record most leases **on the balance sheet**, recognising:
- a **Right-of-Use (ROU) asset**, representing the right to use the asset; and
- a **Lease liability**, representing the obligation to make future payments.

This approach replaced older rules (IAS 17), where many leases were treated as off‑balance‑sheet operating expenses. IFRS 16 therefore improves **transparency** and **comparability** across companies by reflecting the economic reality of leases.

The impact is seen across the main financial statements:
- **Statement of Financial Position:** records the ROU asset and the lease liability.  
- **Profit or Loss:** rent expense is replaced by **depreciation** and **interest expense**.  
- **Cash Flow Statement:** payments are split between **principal** (financing) and **interest** (policy choice under IAS 7).
        """
    )

# ──────────────────────────────────────────────────────────────
# 2. Scenario (based on ACCA source)
# ──────────────────────────────────────────────────────────────
with st.expander("2️⃣ Scenario (based on ACCA example)", expanded=True):
    st.markdown(
        r"""
A company leases a property for **20 years**, paying **£80,000 per year in arrears** (end of year).  
The **incremental borrowing rate** is **6 %**, and the company incurs **£25,000** in initial direct costs.

This example is adapted from the ACCA article *“IFRS 16 Leases”* and demonstrates how the lease liability and right‑of‑use asset are recognised and measured.
        """
    )

# ──────────────────────────────────────────────────────────────
# 3. Calculating the Present Value
# ──────────────────────────────────────────────────────────────
with st.expander("3️⃣ Calculating the Present Value", expanded=True):
    st.markdown(
        r"""
To measure the **lease liability**, the company calculates the **present value (PV)** of the future lease payments, discounted at 6 % (the incremental borrowing rate):

\[
PV = \sum_{t=1}^{20} \frac{80{,}000}{(1.06)^t} = £917{,}594
\]

Adding the **initial direct costs (£25,000)** gives a **Right‑of‑Use (ROU) asset** of **£942,594**.

💡 *If payments were made at the **beginning** of each year (in advance), the PV would be slightly higher because each payment is discounted for one fewer period.*
        """
    )

# ──────────────────────────────────────────────────────────────
# 4. The Payment Schedule
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

with st.expander("4️⃣ The Payment Schedule", expanded=True):
    st.markdown(
        r"""
The schedule shows how each year’s **interest** and **principal repayment** change the lease liability:

- **Interest (6 %)** = Opening × 6 %  
- **Principal repaid** = Payment − Interest  
- **Closing liability** = Opening − Principal  

Example: Year 1 interest £55,056 (6 % of £917,594). Payment £80,000 ⇒ principal £24,944 ⇒ closing £892,649.
        """
    )
    st.dataframe(df.style.format({
        "Opening liability": "£{:,.0f}",
        "Interest (6%)": "£{:,.0f}",
        "Payment": "£{:,.0f}",
        "Closing liability": "£{:,.0f}",
        "Principal repaid": "£{:,.0f}",
    }), use_container_width=True)

# ──────────────────────────────────────────────────────────────
# 5. How to Update the Financial Statements
# ──────────────────────────────────────────────────────────────
with st.expander("5️⃣ How to Update the Financial Statements", expanded=True):
    y1_interest = df.loc[df["Year"] == 1, "Interest (6%)"].iloc[0]
    y1_principal = df.loc[df["Year"] == 1, "Principal repaid"].iloc[0]
    depreciation = 47_130

    st.markdown(
        r"""
Under **IFRS 16**, the financial statements reflect both the asset and liability sides of the lease:

### 🧾 Statement of Profit or Loss
- **Depreciation expense** on the ROU asset: £47,130 (straight-line over 20 years).  
- **Interest expense** on the lease liability: £55,056 (6 % of opening balance).  

These replace the old *lease rental expense*. Total expense is higher in early years but lower later (front-loaded effect).

### 💰 Statement of Financial Position
- **ROU asset** (cost £942,594 less accumulated depreciation £47,130) = £895,464.  
- **Lease liability** closing balance = £892,649.  

Both are shown on balance sheet, increasing transparency and gearing ratios.

### 💸 Statement of Cash Flows
- **Principal repayment (£24,944)** — Financing activity.  
- **Interest payment (£55,056)** — either Operating or Financing depending on policy.

### 📚 Tax adjustment
While IFRS 16 depreciation is a **book expense**, it is *not* an allowable deduction for tax.  
For **taxable profit**, depreciation is replaced with **capital allowances** if applicable, and interest remains deductible as a finance cost.

### 🚫 Exempt leases
IFRS 16 allows lessees not to recognise:
- **Short-term leases** (≤ 12 months), and  
- **Low-value leases** (e.g., small office equipment).

These continue to be expensed straight to profit or loss.
        """
    )

    st.markdown("**Example of Year 1 Journals:**")
    st.code(
        f"""
Dr Right-of-use asset                 £942,594
    Cr Lease liability                          £917,594
    Cr Cash (initial direct costs)               £25,000

Dr Interest expense                    £{y1_interest:,.0f}
Dr Lease liability (principal)         £{y1_principal:,.0f}
    Cr Cash (lease payment)                     £80,000

Dr Depreciation expense                £{depreciation:,.0f}
    Cr Accumulated depreciation (ROU)          £{depreciation:,.0f}
        """
    )

st.success("All stages loaded — from introduction to financial statement impact under IFRS 16.")
