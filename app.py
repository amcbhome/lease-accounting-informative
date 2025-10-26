import streamlit as st
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────────────────────
# Page setup
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="IFRS 16 — Lease Accounting Made Simple", layout="centered")
st.title("📘 IFRS 16 — Lease Accounting Made Simple")
st.caption("An educational walkthrough using a static scenario to explain key stages in lessee accounting under IFRS 16.")

# ──────────────────────────────────────────────────────────────
# Static scenario
# ──────────────────────────────────────────────────────────────
with st.expander("Stage 1 — Calculating the Present Value", expanded=True):
    st.markdown(
        r"""
A company leases a property for **20 years**, paying **£80,000** per year **in arrears** (end of year).  
The lessee’s **incremental borrowing rate** is **6 %**, and there are **£25,000** initial direct costs.

We calculate the **present value (PV)** of all lease payments:

\[
PV = \sum_{t=1}^{20} \frac{80{,}000}{(1.06)^t} = £917{,}594
\]

Adding initial direct costs (£25,000) gives a **Right‑of‑Use (ROU) asset** of **£942,594**.

💡 *If payments were made at the **start** of each year (in advance), the PV would be slightly higher because each payment is discounted for one fewer period.*
        """
    )

# ──────────────────────────────────────────────────────────────
# Payment schedule
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

with st.expander("Stage 2 — Building the Payment Schedule", expanded=True):
    st.markdown(
        r"""
Each year the lease liability changes as payments are made:

- **Interest (6 %)** = Opening × 6 %
- **Principal repaid** = Payment − Interest
- **Closing liability** = Opening − Principal

Example: Year 1 interest £55,056 (6 % of £917,594). Payment £80,000 ⇒ principal £24,944 ⇒ closing £892,649.
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
# Journalising
# ──────────────────────────────────────────────────────────────
with st.expander("Stage 3 — Journalising the Lease", expanded=True):
    y1_interest = df.loc[df["Year"] == 1, "Interest (6%)"].iloc[0]
    y1_principal = df.loc[df["Year"] == 1, "Principal repaid"].iloc[0]
    depreciation = 47_130

    st.markdown(
        "At the **start of the lease**, record the ROU asset and the lease liability (and direct costs)."
    )
    st.code(
        f"""
Dr Right‑of‑use asset                 £942,594
    Cr Lease liability                          £917,594
    Cr Cash (initial direct costs)               £25,000
        """
    )

    st.markdown(
        "At **year‑end**, interest builds up and the payment reduces the liability. Depreciation is charged on the ROU asset."
    )
    st.code(
        f"""
Dr Interest expense                    £{y1_interest:,.0f}
Dr Lease liability (principal)         £{y1_principal:,.0f}
    Cr Cash (lease payment)                     £80,000

Dr Depreciation expense                £{depreciation:,.0f}
    Cr Accumulated depreciation (ROU)          £{depreciation:,.0f}
        """
    )

# ──────────────────────────────────────────────────────────────
# Financial statements
# ──────────────────────────────────────────────────────────────
with st.expander("Stage 4 — Impact on the Financial Statements", expanded=True):
    st.markdown("**Income Statement:** Rent expense is replaced by depreciation + interest.")
    pol = pd.DataFrame(
        {"Line item": ["Depreciation (ROU)", "Interest expense"], "Amount": [depreciation, y1_interest]}
    )
    st.dataframe(pol.style.format({"Amount": "£{:,.0f}"}), use_container_width=True)

    st.markdown("**Statement of Financial Position:** Recognise the new asset and liability.")
    rou_carrying = 942_594 - depreciation
    sfp = pd.DataFrame(
        {"Caption": ["Right‑of‑use asset", "Lease liability"], "Amount": [rou_carrying, df.loc[df["Year"]==1,"Closing liability"].iloc[0]]}
    )
    st.dataframe(sfp.style.format({"Amount": "£{:,.0f}"}), use_container_width=True)

    st.markdown("**Cash Flow:** Payments split into interest + principal (usually financing).")
    cf = pd.DataFrame(
        {"Cash flow": ["Interest portion (IAS 7 policy)", "Principal portion (financing)"], "Amount": [y1_interest, y1_principal]}
    )
    st.dataframe(cf.style.format({"Amount": "£{:,.0f}"}), use_container_width=True)

# ──────────────────────────────────────────────────────────────
# ROU recognition test
# ──────────────────────────────────────────────────────────────
with st.expander("Stage 5 — Recognising a Right‑of‑Use Asset", expanded=True):
    st.markdown(
        r"""
A lessee recognises a **Right‑of‑Use (ROU) asset** when it controls the use of an identified asset for a period of time in exchange for payment.

**Checklist**
- ✅ There is an *identified asset* (specific property or equipment).  
- ✅ The lessee has the *right to obtain substantially all economic benefits* from its use.  
- ✅ The lessee has the *right to direct the use* of the asset.

**Exemptions** apply for short‑term (≤ 12 months) and low‑value leases.
        """
    )

# ──────────────────────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────────────────────
st.success(
    "This staged guide links the figures in the table to the IFRS 16 model — from PV calculation to the effect on each statement."
)
