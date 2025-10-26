# ──────────────────────────────────────────────────────────────
# 5️⃣ Updating the Financial Statements — automated and concise
# ──────────────────────────────────────────────────────────────
elif menu == "5️⃣ Updating the Financial Statements":
    st.header("5️⃣ Updating the Financial Statements (Automated Journals)")

    st.markdown(
        """
This section demonstrates how the **lease liability schedule** automatically produces  
the **accounting journals** for lease commencement and subsequent years.
        """
    )

    # ── Inputs and calculations
    n = 20; r = 0.06; payment = 80_000
    pv = payment * (1 - (1 + r) ** -n) / r
    depreciation = (pv + 25_000) / n

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

    # ── Layout: side-by-side
    col1, col2 = st.columns(2, gap="large")

    # Left: payment schedule
    with col1:
        st.subheader("📊 Lease Payment Schedule (First Two Years)")
        st.dataframe(
            df.head(2).style.format({
                "Opening liability": "£{:,.0f}",
                "Interest (6%)": "£{:,.0f}",
                "Payment": "£{:,.0f}",
                "Principal repaid": "£{:,.0f}",
                "Closing liability": "£{:,.0f}",
            }),
            use_container_width=True,
        )
        st.caption("The closing liability becomes the next year's opening balance.")

    # Right: automated journals
    with col2:
        st.subheader("🧾 Automated Journal Entries")

        # Year 0 – Lease Commencement
        st.markdown("**Year 0 — Lease Commencement**")
        st.code(
            f"Dr 1150 Right-of-Use Asset........£{pv + 25_000:,.0f}\n"
            f"    Cr 2100 Lease Liability...............£{pv:,.0f}\n"
            f"    Cr 1000 Bank (Initial Direct Costs)...£25,000",
            language="text",
        )

        # Years 1–2 from schedule
        for _, row in df.head(2).iterrows():
            year = int(row["Year"])
            interest = row["Interest (6%)"]
            principal = row["Principal repaid"]
            st.markdown(f"**Year {year} — End of Year {year}**")
            st.code(
                f"Dr 7500 Interest Expense..............£{interest:,.0f}\n"
                f"Dr 2100 Lease Liability (Principal)...£{principal:,.0f}\n"
                f"    Cr 1000 Bank (Lease Payment)........£80,000\n\n"
                f"Dr 7000 Depreciation Expense..........£{depreciation:,.0f}\n"
                f"    Cr 1150 Accumulated Depreciation....£{depreciation:,.0f}",
                language="text",
            )

    # ── Summary text
    st.markdown(
        """
### 📘 Summary
- **Year 0:** records the Right-of-Use asset and Lease liability.  
- **Years 1–2:** record interest, principal repayment, and depreciation.  
- Journal figures are pulled **directly from the schedule**, showing accounting automation in action.
        """
    )
