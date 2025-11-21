import streamlit as st
import pandas as pd

st.set_page_config(page_title="Session 1 — Asset Pricing Foundations", page_icon="📊")

st.title("Session 1 — Asset Pricing Foundations")

st.markdown("""
### 🎯 Session Overview

This session covers the microfoundations of asset pricing theory and introduces key pricing frameworks:
- **Optimization fundamentals** (FOCs, KKT conditions)
- **The time dimension** (intertemporal substitution, Fisher's model)
- **The risk dimension** (contingent claims, Arrow-Debreu pricing)
- **General equilibrium** (Pareto optimality, welfare theorems)
- **Asset pricing approaches** (safe vs. risky cash flows, no-arbitrage vs. equilibrium)
""")

# ============================================================
st.header("1. Microfoundations: The Time Dimension")

st.markdown("""
Asset pricing begins with **intertemporal choice**: how do agents allocate consumption between today and tomorrow?

**Fisher's Two-Period Model:**
$$U = u(c_0) + \\beta u(c_1)$$

where $\\beta$ is the discount factor and $u$ is concave (preference for smooth consumption).
""")

with st.expander("🔄 Interactive: Intertemporal Choice"):
    st.markdown("Explore how discount factor and interest rates affect optimal consumption allocation.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        Y0 = st.number_input("Income today (Y₀)", 50.0, 200.0, 100.0, 10.0)
        Y1 = st.number_input("Income tomorrow (Y₁)", 50.0, 200.0, 100.0, 10.0)
        
    with col2:
        beta = st.slider("Discount factor (β)", 0.80, 0.99, 0.95, 0.01)
        r = st.slider("Interest rate (r, %)", 0.0, 10.0, 3.0, 0.5) / 100
    
    # Lifetime budget constraint: Y0 + Y1/(1+r) >= c0 + c1/(1+r)
    pv_income = Y0 + Y1/(1+r)
    
    st.markdown(f"""
    **Lifetime Budget Constraint:**
    $$Y_0 + \\frac{{Y_1}}{{1+r}} = {Y0:.1f} + \\frac{{{Y1:.1f}}}{{1+{r:.3f}}} = {pv_income:.2f}$$
    
    **Intertemporal MRS Condition:**
    $$\\frac{{u'(c_0)}}{{\\beta u'(c_1)}} = 1+r$$
    """)
    
    # For log utility: c0/c1 = (1+r)/β
    # And c0 + c1/(1+r) = pv_income
    # Solving: c0 = pv_income * (1+r) / ((1+r) + β)
    c0_optimal = pv_income * (1+r) / ((1+r) + beta)
    c1_optimal = pv_income * beta * (1+r)**2 / ((1+r) + beta)
    savings = Y0 - c0_optimal
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Optimal c₀", f"{c0_optimal:.2f}")
    col2.metric("Optimal c₁", f"{c1_optimal:.2f}")
    col3.metric("Savings (s)", f"{savings:.2f}")
    
    if savings > 0:
        st.info(f"💰 The agent **saves** ${savings:.2f} today, earning ${savings*(1+r):.2f} in interest.")
    elif savings < 0:
        st.info(f"💳 The agent **borrows** ${-savings:.2f} today, paying ${-savings*(1+r):.2f} in interest.")
    else:
        st.info("⚖️ The agent neither saves nor borrows (consumption = income each period).")

# ============================================================
st.header("2. Microfoundations: The Risk Dimension")

st.markdown("""
When future income is uncertain, we need **contingent claims** (Arrow-Debreu securities):
- $q_G$ = price of claim paying \\$1 in the **good state**
- $q_B$ = price of claim paying \\$1 in the **bad state**

**Expected Utility Under Uncertainty:**
$$U = u(c_0) + \\beta[\\pi u(c_1^G) + (1-\\pi)u(c_1^B)]$$

**Lifetime Budget Constraint:**
$$Y_0 + q_G Y_1^G + q_B Y_1^B \\geq c_0 + q_G c_1^G + q_B c_1^B$$
""")

with st.expander("🎲 Interactive: Contingent Claims Pricing"):
    st.markdown("See how state prices relate to probabilities and marginal utilities.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pi = st.slider("Probability of good state (π)", 0.3, 0.9, 0.6, 0.05)
        beta_risk = st.slider("Discount factor (β)", 0.90, 0.99, 0.95, 0.01, key="beta_risk")
    
    with col2:
        c1_G = st.number_input("Consumption in good state", 50.0, 200.0, 120.0, 10.0)
        c1_B = st.number_input("Consumption in bad state", 30.0, 150.0, 80.0, 10.0)
    
    # Assume log utility: u'(c) = 1/c, normalized c0 = 100
    c0 = 100
    
    # FOC gives: q_G = β * π * u'(c1_G) / u'(c0) = β * π * (c0/c1_G)
    q_G = beta_risk * pi * (c0 / c1_G)
    q_B = beta_risk * (1-pi) * (c0 / c1_B)
    
    # Risk-free rate: 1/(1+r) = q_G + q_B
    rf_price = q_G + q_B
    rf_rate = (1/rf_price - 1) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("q_G (good state)", f"{q_G:.4f}")
    col2.metric("q_B (bad state)", f"{q_B:.4f}")
    col3.metric("Risk-free rate", f"{rf_rate:.2f}%")
    
    st.markdown(f"""
    **FOC conditions:**
    $$q_G = \\beta \\pi \\frac{{u'(c_1^G)}}{{u'(c_0)}} = {q_G:.4f}$$
    $$q_B = \\beta (1-\\pi) \\frac{{u'(c_1^B)}}{{u'(c_0)}} = {q_B:.4f}$$
    
    **Risk-free bond pricing:** A bond paying \\$1 in every state costs:
    $$q_{{\\text{{bond}}}} = q_G + q_B = {rf_price:.4f} \\quad \\Rightarrow \\quad r = {rf_rate:.2f}\\%$$
    """)
    
    # State price ratio
    state_price_ratio = q_G / q_B
    prob_ratio = pi / (1-pi)
    mu_ratio = (c1_B / c1_G)  # For log utility: u'(c1_G)/u'(c1_B) = c1_B/c1_G
    
    st.markdown(f"""
    **State price relationship:**
    $$\\frac{{q_G}}{{q_B}} = \\frac{{\\pi}}{{1-\\pi}} \\cdot \\frac{{u'(c_1^G)}}{{u'(c_1^B)}} = {prob_ratio:.3f} \\times {mu_ratio:.3f} = {state_price_ratio:.3f}$$
    
    The state in which consumption is **lower** has a **higher marginal utility**, making claims on that state more valuable (insurance principle).
    """)

# ============================================================
st.header("3. General Equilibrium Insights")

st.markdown("""
**Pareto Optimality Condition:**

In a two-consumer economy, an allocation is Pareto optimal when:
$$MRS_1 = MRS_2$$

That is, both consumers' marginal rates of substitution are equalized.

**Welfare Theorems:**
1. **First Welfare Theorem**: Any competitive equilibrium is Pareto optimal (CE ⇒ PO)
2. **Second Welfare Theorem**: Any Pareto optimal allocation can be supported as a competitive equilibrium with appropriate prices (PO ⇒ CE)
""")

with st.expander("⚖️ Interactive: Pareto Optimality"):
    st.markdown("Visualize when two consumers achieve Pareto optimal allocations.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        c_a1 = st.slider("Consumer 1: Good A consumption", 0.0, 10.0, 5.0, 0.5)
        alpha = st.slider("Consumer 1: Weight α", 0.5, 2.0, 1.0, 0.1)
    
    with col2:
        beta_ge = st.slider("Consumer 2: Weight β", 0.5, 2.0, 1.0, 0.1, key="beta_ge")
        Y_a = st.number_input("Total endowment of good A", 5.0, 15.0, 10.0, 1.0)
        Y_b = st.number_input("Total endowment of good B", 5.0, 15.0, 10.0, 1.0)
    
    # Resource constraints
    c_a2 = Y_a - c_a1
    
    # Derive c_b1 and c_b2 from Pareto condition (assuming log utility)
    # MRS_1 = u'(c_a1)/(α*u'(c_b1)) = (1/c_a1)/(α/c_b1) = c_b1/(α*c_a1)
    # MRS_2 = v'(c_a2)/(β*v'(c_b2)) = c_b2/(β*c_a2)
    # Setting equal: c_b1/(α*c_a1) = c_b2/(β*c_a2)
    # With c_b2 = Y_b - c_b1:
    # c_b1/(α*c_a1) = (Y_b - c_b1)/(β*c_a2)
    # Solving for c_b1:
    c_b1 = Y_b * beta_ge * c_a2 / (alpha * c_a1 + beta_ge * c_a2)
    c_b2 = Y_b - c_b1
    
    mrs_1 = c_b1 / (alpha * c_a1)
    mrs_2 = c_b2 / (beta_ge * c_a2)
    
    results = pd.DataFrame({
        'Consumer': ['Consumer 1', 'Consumer 2'],
        'Good A': [f"{c_a1:.2f}", f"{c_a2:.2f}"],
        'Good B': [f"{c_b1:.2f}", f"{c_b2:.2f}"],
        'MRS': [f"{mrs_1:.3f}", f"{mrs_2:.3f}"]
    })
    
    st.dataframe(results, hide_index=True, use_container_width=True)
    
    if abs(mrs_1 - mrs_2) < 0.01:
        st.success(f"✅ **Pareto optimal!** Both MRS are approximately equal: {mrs_1:.3f} ≈ {mrs_2:.3f}")
    else:
        st.warning(f"⚠️ Not Pareto optimal. MRS₁ = {mrs_1:.3f} ≠ MRS₂ = {mrs_2:.3f}. Further gains from trade exist.")

# ============================================================
st.header("4. Pricing Safe Cash Flows")

st.markdown("""
**Discount Bond:** Pays \\$1 at maturity $T$. Price today:
$$P_T = \\frac{1}{(1+r_T)^T}$$

**Coupon Bond:** Pays coupon $C$ each year and face value $F$ at maturity:
$$P_T^C = \\sum_{t=1}^T \\frac{C}{(1+r_t)^t} + \\frac{F}{(1+r_T)^T}$$
""")

with st.expander("💰 Interactive: Bond Pricing"):
    st.markdown("Calculate the price of discount bonds and coupon bonds.")
    
    bond_type = st.radio("Select bond type:", ["Discount Bond", "Coupon Bond"])
    
    if bond_type == "Discount Bond":
        col1, col2 = st.columns(2)
        with col1:
            T_discount = st.slider("Maturity (years)", 1, 30, 10)
        with col2:
            r_discount = st.slider("Yield (% per year)", 0.0, 10.0, 3.0, 0.5) / 100
        
        P_discount = 1 / (1 + r_discount)**T_discount
        
        st.metric("Bond Price", f"${P_discount:.4f}")
        st.markdown(f"""
        **Calculation:**
        $$P_{{{T_discount}}} = \\frac{{1}}{{(1+{r_discount:.4f})^{{{T_discount}}}}} = \\${P_discount:.4f}$$
        
        You pay \\${P_discount:.4f} today to receive \\$1 in {T_discount} years.
        """)
    
    else:  # Coupon Bond
        col1, col2 = st.columns(2)
        with col1:
            T_coupon = st.slider("Maturity (years)", 1, 30, 10, key="T_coupon")
            C_coupon = st.number_input("Annual coupon ($)", 1.0, 100.0, 5.0, 1.0)
        with col2:
            F_coupon = st.number_input("Face value ($)", 50.0, 1000.0, 100.0, 10.0)
            r_coupon = st.slider("Yield (% per year)", 0.0, 10.0, 3.0, 0.5, key="r_coupon") / 100
        
        # Calculate coupon bond price
        pv_coupons = sum([C_coupon / (1 + r_coupon)**t for t in range(1, T_coupon + 1)])
        pv_face = F_coupon / (1 + r_coupon)**T_coupon
        P_coupon = pv_coupons + pv_face
        
        st.metric("Bond Price", f"${P_coupon:.2f}")
        
        breakdown = pd.DataFrame({
            'Component': ['Present Value of Coupons', 'Present Value of Face', 'Total Price'],
            'Value ($)': [f"{pv_coupons:.2f}", f"{pv_face:.2f}", f"{P_coupon:.2f}"]
        })
        st.dataframe(breakdown, hide_index=True, use_container_width=True)
        
        coupon_rate = (C_coupon / F_coupon) * 100
        
        if P_coupon > F_coupon:
            st.info(f"💎 Bond trades at a **premium** (price > face value): coupon rate ({coupon_rate:.2f}%) > yield ({r_coupon*100:.2f}%).")
        elif P_coupon < F_coupon:
            st.info(f"🔻 Bond trades at a **discount** (price < face value): coupon rate ({coupon_rate:.2f}%) < yield ({r_coupon*100:.2f}%).")
        else:
            st.info(f"⚖️ Bond trades at **par** (price = face value): coupon rate ({coupon_rate:.2f}%) = yield ({r_coupon*100:.2f}%).")

# ============================================================
st.header("5. Pricing Risky Cash Flows")

st.markdown("""
Three equivalent approaches to pricing risky assets:

### 1. Risk-Adjusted Discounting
$$P_t = \\frac{E(\\tilde{C}_t)}{(1+r_t+\\psi_t)^t} = \\frac{E(\\tilde{C}_t) - \\Psi_t}{(1+r_t)^t}$$

where $\\psi_t$ is the risk premium and $\\Psi_t$ is the risk adjustment.

### 2. Arrow-Debreu (Contingent Claims)
$$P_t = \\sum_{i=1}^n q_{t,i} C_{t,i}$$

Decompose the risky payoff into state-contingent components and price each.

### 3. Risk-Neutral Pricing
$$P_t = \\frac{\\hat{E}(C_t)}{(1+r_t)^t}$$

where $\\hat{E}$ uses "risk-neutral" probabilities $\\hat{\\pi}_i$ instead of physical probabilities $\\pi_i$.
""")

with st.expander("📊 Interactive: Compare Pricing Methods"):
    st.markdown("Price a risky asset using different approaches and verify they give the same result.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        C_good = st.number_input("Payoff in good state ($)", 50.0, 200.0, 150.0, 10.0, key="C_good")
        C_bad = st.number_input("Payoff in bad state ($)", 0.0, 100.0, 50.0, 10.0, key="C_bad")
        pi_pricing = st.slider("Probability of good state", 0.3, 0.9, 0.6, 0.05, key="pi_pricing")
    
    with col2:
        rf_pricing = st.slider("Risk-free rate (%)", 0.0, 10.0, 3.0, 0.5, key="rf_pricing") / 100
        # Use state prices from earlier calculation or compute new ones
        qG_pricing = 0.45  # Simplified for illustration
        qB_pricing = 0.52
    
    # Method 1: Arrow-Debreu
    price_AD = qG_pricing * C_good + qB_pricing * C_bad
    
    # Method 2: Risk-neutral (derive from state prices)
    # q_i = π̂_i / (1+r), so π̂_i = q_i * (1+r)
    pi_hat_good = qG_pricing * (1 + rf_pricing)
    pi_hat_bad = qB_pricing * (1 + rf_pricing)
    # Normalize (should sum to 1 if q_G + q_B = 1/(1+r))
    total_prob = pi_hat_good + pi_hat_bad
    pi_hat_good_norm = pi_hat_good / total_prob
    pi_hat_bad_norm = pi_hat_bad / total_prob
    
    expected_payoff_RN = pi_hat_good_norm * C_good + pi_hat_bad_norm * C_bad
    price_RN = expected_payoff_RN / (1 + rf_pricing)
    
    # Method 3: Expected value with risk adjustment
    expected_payoff = pi_pricing * C_good + (1-pi_pricing) * C_bad
    # Assume risk premium proportional to volatility
    risk_adjustment = 5.0  # Simplified
    price_RA = (expected_payoff - risk_adjustment) / (1 + rf_pricing)
    
    st.markdown("### Pricing Results")
    
    methods_df = pd.DataFrame({
        'Method': [
            '1. Arrow-Debreu',
            '2. Risk-Neutral',
            '3. Risk-Adjusted'
        ],
        'Price ($)': [
            f"{price_AD:.2f}",
            f"{price_RN:.2f}",
            f"{price_RA:.2f}"
        ],
        'Formula': [
            f'qG×{C_good:.0f} + qB×{C_bad:.0f}',
            f'E[C]/(1+r) with π̂',
            f'(E[C] - Ψ)/(1+r)'
        ]
    })
    
    st.dataframe(methods_df, hide_index=True, use_container_width=True)
    
    st.info("""
    **Key insight**: All three methods are equivalent under no-arbitrage conditions. 
    Arrow-Debreu is the most fundamental; risk-neutral and risk-adjusted approaches 
    are convenient reformulations.
    """)

# ============================================================
st.header("6. No-Arbitrage vs. Equilibrium")

st.markdown("""
Asset pricing can be analyzed from two complementary perspectives:

### No-Arbitrage Perspective
- Takes some prices as given
- Derives other prices by replication/arbitrage arguments
- Example: Price a coupon bond using discount bond prices
- Requires only that arbitrage opportunities don't exist

### Equilibrium Perspective  
- Uses microeconomic foundations (utility maximization, market clearing)
- Determines all prices simultaneously from fundamentals
- Links asset prices to preferences, endowments, and technology
- Example: Derive state prices from consumer optimization (FOCs)

**Both approaches are valid and complementary!** No-arbitrage is simpler but less fundamental; 
equilibrium provides deeper economic insight but requires more structure.
""")

with st.expander("🎓 Key Takeaways"):
    st.markdown("""
    ### Core Concepts from This Session
    
    1. **Intertemporal choice**: Agents smooth consumption across time using discount factor $\\beta$ and interest rate $r$
    
    2. **Risk and states**: Uncertain outcomes require state-contingent claims (Arrow-Debreu securities)
    
    3. **Contingent claim prices**: States with low consumption have higher marginal utility, making claims more valuable (insurance)
    
    4. **General equilibrium**: Competitive equilibria are Pareto optimal (First Welfare Theorem)
    
    5. **Safe asset pricing**: Present value of certain cash flows using risk-free rates
    
    6. **Risky asset pricing**: Three equivalent approaches:
       - Risk-adjusted discounting (CAPM, CCAPM, APT)
       - Arrow-Debreu (state prices)  
       - Risk-neutral pricing (distorted probabilities)
    
    7. **Two perspectives**: No-arbitrage (takes some prices as given) vs. Equilibrium (derives all prices from fundamentals)
    """)

# ============================================================
st.header("7. 🧠 Test Your Understanding")

with st.expander("📝 Quiz"):
    q1 = st.radio(
        "**Q1**: If $\\beta = 0.95$ and $r = 5\\%$, what happens in equilibrium?",
        [
            "The agent saves (c₀ < Y₀)",
            "The agent borrows (c₀ > Y₀)",
            "The agent neither saves nor borrows"
        ],
        index=None
    )
    
    if q1 == "The agent neither saves nor borrows":
        st.success("✅ Correct! With β = 0.95 and 1/(1+r) = 1/1.05 ≈ 0.952, these are approximately equal, so the agent's time preferences match market prices.")
    elif q1:
        st.error("❌ Try again. Compare β with 1/(1+r).")
    
    st.markdown("---")
    
    q2 = st.radio(
        "**Q2**: Why is the bad-state contingent claim typically more expensive per unit probability?",
        [
            "Because bad states are more likely",
            "Because marginal utility is higher when consumption is low",
            "Because of transaction costs"
        ],
        index=None,
        key="q2"
    )
    
    if q2 == "Because marginal utility is higher when consumption is low":
        st.success("✅ Correct! State prices reflect both probabilities AND marginal utilities. Low consumption → high MU → higher q.")
    elif q2:
        st.error("❌ Not quite. Think about the insurance principle.")
    
    st.markdown("---")
    
    q3 = st.radio(
        "**Q3**: The First Welfare Theorem states that:",
        [
            "All Pareto optimal allocations are competitive equilibria",
            "All competitive equilibria are Pareto optimal",
            "Prices always equal marginal costs"
        ],
        index=None,
        key="q3"
    )
    
    if q3 == "All competitive equilibria are Pareto optimal":
        st.success("✅ Correct! CE ⇒ PO (the Second Welfare Theorem goes the other direction).")
    elif q3:
        st.error("❌ That's the Second Welfare Theorem (or incorrect).")

# ============================================================
st.header("8. 📥 Download Materials")

st.markdown("Download the complete lecture notes with detailed derivations:")

try:
    with open("summaries/session1_summary.pdf", "rb") as f:
        st.download_button(
            label="📄 Download PDF Summary",
            data=f,
            file_name="session1_asset_pricing_foundations.pdf",
            mime="application/pdf",
        )
except FileNotFoundError:
    st.error("PDF not found. Please contact the instructor.")

st.markdown("---")
st.caption("Session 1 • Asset Pricing Foundations • Use the sidebar to navigate")
