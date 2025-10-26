# ──────────────────────────────────────────────────────────────
# 4️⃣ The Payment Schedule — calculated automatically
# ──────────────────────────────────────────────────────────────
elif menu == "4️⃣ The Payment Schedule":
    st.header("4️⃣ The Payment Schedule (Auto-Generated)")

    # Inputs
    n = 20            # years
    r = 0.06          # interest rate
    payment = 80_000  # annual payment
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

    df = pd.DataFrame(
        rows,
        columns=[
            "Year",
            "Opening liability",
            "Interest (6%)",
            "Payment",
            "Principal repaid",
            "Closing liability",
        ],
    )

    # Add cumulative totals
    cdf = df.copy()
    cdf["Cumulative Interest"] = df["Interest (6%)"].cumsum()
    cdf["Cumulative Principal"] = df["Principal repaid"].cumsum()

    st.markdown(
        """
The schedule below is **calculated entirely from formulas** — not from a manual table.

Each year:
- **Interest (6%)** = Opening × 6 %
- **Principal repaid** = Payment − Interest
- **Closing liability** = Opening − Principal

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

    st.markdown(
        """
The journal entries below are **auto-generated from the schedule above**,  
so each year's debit and credit values come directly from the calculations.
        """
    )

    # Nominal codes reference
    st.subheader("Nominal Codes (Example Chart of Accounts)")
    st.table({
        "Code": ["1150", "2100", "7000", "7500", "1000"],
        "Account Name": [
            "Right-of-Use Asset",
            "Lease Liability",
            "Depreciation Expense",
            "Interest Expense",
            "Bank",
        ],
        "Type": [
            "Non-current asset",
            "Non-current liability",
            "Expense (P&L)",
            "Finance cost (P&L)",
            "Asset",
        ],
    })

    # Show commencement entry once
    st.subheader("Year 0 — Lease Commencement")
    st.code(
        f"Dr 1150 Right-of-Use Asset........£{pv + 25_000:,.0f}\n"
        f"    Cr 2100 Lease Liability................£{pv:,.0f}\n"
        f"    Cr 1000 Bank (Initial direct costs)...£25,000",
        language="text",
    )

    # Generate year-by-year journals directly from df
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
- **P&L:** records depreciation and interest each year.  
- **SOFP:** shows reducing ROU asset and lease liability.  
- **Cash Flow:** splits principal (financing) and interest (policy choice).  

### Tax Treatment
- **Depreciation** is a book expense only (replaced by capital allowances).  
- **Interest** is normally deductible for tax purposes.  

### IFRS 16 Exemptions
Short-term (≤ 12 months) and low-value leases are expensed directly.
        """
    )
