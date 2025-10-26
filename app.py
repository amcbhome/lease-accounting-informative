import streamlit as st
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────────────────────
# Page setup
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="IFRS 16 — Lease Teaching App", layout="centered")
st.title("📘 IFRS 16 — Leases (Lessee) — Teaching App")
st.caption(
    "Informative walkthrough using a static test scenario: initial recognition, subsequent measurement, journal entries, and financial statement impacts."
)

# ──────────────────────────────────────────────────────────────
# Static test scenario (from your spreadsheet)
# ──────────────────────────────────────────────────────────────
with st.expander("Scenario overview (static test data)", expanded=True):
    st.markdown(
        r"""
**Lessee enters a 20‑year property lease** with fixed annual payments of **£80,000** payable in arrears.

- **Lease term:** 20 years  
- **Annual lease payment:** £80,000 (end of each year)  
- **Discount rate (incremental borrowing rate):** 6%  
- **Initial direct costs:** £25,000  
- **Present value (PV) of lease payments at commencement:** **£917,594**  
- **Right‑of‑use (ROU) asset at cost:** PV £917,594 **+** initial direct costs £25,000 **= £942,594**  
- **Depreciation:** Straight‑line over 20 years = **£47,130 per year**
        """
    )

# Amortisation schedule — fixed from the provided sheet
schedule_data = [
    # year, opening, interest, payment, closing
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

with st.expander("Lease liability amortisation schedule", expanded=True):
    st.dataframe(df.style.format({
        "Opening liability": "£{:,.0f}",
        "Interest (6%)": "£{:,.0f}",
        "Payment": "£{:,.0f}",
        "Closing liability": "£{:,.0f}",
        "Principal repaid": "£{:,.0f}",
    }), use_container_width=True)

# ──────────────────────────────────────────────────────────────
# IFRS 16 logic — concise teaching points
# ──────────────────────────────────────────────────────────────
with st.expander("IFRS 16 — recognition & measurement (key points)", expanded=True):
    st.markdown(
        r"""
**Initial recognition (lessee)**  
- Recognise a **lease liability** at the present value of lease payments discounted at the rate implicit in the lease or the **incremental borrowing rate**.  
- Recognise a **ROU asset** initially at cost: the amount of the lease liability **plus** initial direct costs, prepaid lease payments, and dismantling/restoration provisions (if any).  

**Subsequent measurement**  
- **Lease liability:** increase by interest; reduce by payments; remeasure on certain changes (e.g., lease term, index/rate, modifications).  
- **ROU asset:** carried at cost less accumulated depreciation and impairment. Depreciate S/L over the **lease term** (or useful life if ownership transfers or there is a purchase option reasonably certain to be exercised).
        """
    )

# ──────────────────────────────────────────────────────────────
# Journal entries (Year 0 and Year 1)
# ──────────────────────────────────────────────────────────────
with st.expander("Journal entries — simple illustration", expanded=True):
    y1_interest = df.loc[df["Year"] == 1, "Interest (6%)"].iloc[0]
    y1_principal = df.loc[df["Year"] == 1, "Principal repaid"].iloc[0]
    depreciation = 47_130

    st.markdown("**At commencement (Year 0):**")
    st.code(
        f"""
Dr Right‑of‑use asset                 £942,594
    Cr Lease liability                          £917,594
    Cr Cash (initial direct costs)               £25,000
        """
    )

    st.markdown("**End of Year 1 (payment in arrears):**")
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
# Financial statements snapshot (Year 1)
# ──────────────────────────────────────────────────────────────
with st.expander("Financial statement impact — snapshot (end of Year 1)", expanded=True):
    # Statement of Profit or Loss
    st.subheader("Statement of Profit or Loss (extract)")
    pol = pd.DataFrame(
        {
            "Line item": ["Depreciation (ROU)", "Interest on lease liability"],
            "Amount": [47_130, y1_interest],
        }
    )
    st.dataframe(pol.style.format({"Amount": "£{:,.0f}"}), use_container_width=True)

    # Statement of Financial Position
    st.subheader("Statement of Financial Position (extract)")
    rou_carrying = 942_594 - 47_130
    sfp = pd.DataFrame(
        {
            "Caption": ["Right‑of‑use asset", "Lease liability (non‑current/current split not shown)"],
            "Amount": [rou_carrying, df.loc[df["Year"] == 1, "Closing liability"].iloc[0]],
        }
    )
    st.dataframe(sfp.style.format({"Amount": "£{:,.0f}"}), use_container_width=True)

    # Statement of Cash Flows
    st.subheader("Statement of Cash Flows (extract)")
    cash_flows = pd.DataFrame(
        {
            "Cash flow caption": [
                "Lease payment — interest portion (policy per IAS 7)",
                "Lease payment — principal portion (financing)",
            ],
            "Amount": [y1_interest, y1_principal],
        }
    )
    st.dataframe(cash_flows.style.format({"Amount": "£{:,.0f}"}), use_container_width=True)

# ──────────────────────────────────────────────────────────────
# Notes & validation
# ──────────────────────────────────────────────────────────────
with st.expander("Notes & validation (IFRS cross‑references)", expanded=True):
    st.markdown(
        r"""
- **Single lessee model & recognition** — recognise ROU asset and lease liability for most leases (short‑term/low‑value exemptions exist).  
- **Lease liability at PV of payments** (discounted using the rate implicit in the lease or lessee’s IBR).  
- **ROU asset at cost** = lease liability plus initial direct costs and other adjustments.  
- **Subsequent measurement** — liability unwinds with interest and is reduced by payments; ROU asset depreciated on a systematic basis; remeasure on specified changes.  
- **Presentation & cash flows** — present ROU assets and lease liabilities; principal repayments in **financing**; interest per IAS 7 accounting policy.

*This teaching app uses a fixed dataset and is intended for learning and presentation purposes.*
        """
    )

st.success("Loaded the IFRS 16 teaching scenario. Use the expanders to explore each section.")
