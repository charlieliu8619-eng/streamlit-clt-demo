import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from scipy import stats

# --- Page Configuration ---
st.set_page_config(
    page_title="Ad Click Events & Poisson Distribution",
    page_icon="🎯",
    layout="wide"
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .st-emotion-cache-1y4p8pa {
        max-width: 100%;
    }
    .stButton>button {
        background-color: #00b0f0;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        border: none;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0099d1;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.title("🎯 Ad Click Events & The Poisson Distribution")
st.markdown("""
This dashboard demonstrates the **Poisson Distribution** for modeling rare events in digital advertising: **ad clicks per time period**.

The Poisson distribution is perfect for modeling:
- Number of ad clicks per hour/day
- Click events that occur randomly and independently
- Rare events with a known average rate

**Key Properties:**
- Models count data (0, 1, 2, 3... clicks)
- Single parameter λ (lambda) = average rate of events
- Variance equals the mean (λ)
- Useful for capacity planning and performance analysis
---
""")

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("⚙️ Simulation Controls")
    st.markdown("Adjust parameters to see how click patterns change.")

    # Lambda parameter (average clicks per time period)
    lambda_rate = st.number_input(
        "Average clicks per hour (λ):",
        min_value=0.1,
        max_value=50.0,
        value=5.0,
        step=0.5,
        help="The average number of clicks expected per hour. This is the λ parameter of the Poisson distribution."
    )

    # Number of time periods to simulate
    num_periods = st.slider(
        "Number of hours to simulate:",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100,
        help="How many hourly periods to simulate for our analysis."
    )

    # Time period selector
    time_unit = st.selectbox(
        "Time period:",
        ["Hour", "Day", "Week"],
        help="Choose the time unit for analysis."
    )

    run_simulation = st.button("Run Simulation")

# --- Main Panel for Output ---
if run_simulation:
    st.header("📊 Poisson Distribution Analysis")

    with st.spinner("Generating click event data..."):
        # Generate Poisson-distributed click data
        click_data = np.random.poisson(lam=lambda_rate, size=num_periods)
        
        # Calculate statistics
        observed_mean = np.mean(click_data)
        observed_var = np.var(click_data)
        theoretical_var = lambda_rate

    # --- Display Results ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Simulated Click Distribution")
        
        # Create histogram of observed data
        fig1 = px.histogram(
            x=click_data,
            title=f"Observed Clicks per {time_unit}",
            labels={'x': f'Number of Clicks per {time_unit}', 'y': 'Frequency'},
            template="plotly_white"
        )
        fig1.update_traces(marker_color='#FF5733', opacity=0.7)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Theoretical vs Observed")
        
        # Create comparison with theoretical Poisson
        x_range = np.arange(0, max(click_data) + 1)
        theoretical_pmf = stats.poisson.pmf(x_range, lambda_rate)
        observed_counts = np.bincount(click_data, minlength=len(x_range))
        observed_pmf = observed_counts / num_periods

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=x_range,
            y=theoretical_pmf,
            name='Theoretical Poisson',
            marker_color='#00b0f0',
            opacity=0.7
        ))
        fig2.add_trace(go.Bar(
            x=x_range,
            y=observed_pmf,
            name='Observed Data',
            marker_color='#FF5733',
            opacity=0.5
        ))
        fig2.update_layout(
            title="Theoretical vs Observed Distribution",
            xaxis_title=f"Number of Clicks per {time_unit}",
            yaxis_title="Probability",
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # --- Key Statistics ---
    st.header("📈 Key Statistics & Properties")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Expected Mean (λ)", f"{lambda_rate:.2f}")
    with col2:
        st.metric("Observed Mean", f"{observed_mean:.2f}")
    with col3:
        st.metric("Expected Variance (λ)", f"{theoretical_var:.2f}")
    with col4:
        st.metric("Observed Variance", f"{observed_var:.2f}")

    # --- Business Applications ---
    st.header("💼 Business Applications")
    st.markdown(f"""
    **Why Poisson Distribution matters for digital advertising:**

    1. **Capacity Planning:** With λ = {lambda_rate:.1f} clicks per {time_unit.lower()}, you can predict server load and plan infrastructure capacity.

    2. **Performance Monitoring:** If observed clicks deviate significantly from λ, it may indicate campaign performance changes or technical issues.

    3. **Statistical Testing:** The Poisson model helps determine if changes in click rates are statistically significant.

    4. **Rare Event Analysis:** Perfect for modeling low-frequency, high-value events like premium ad clicks or conversions.

    **Key Insight:** Notice how the observed variance ({observed_var:.2f}) approximately equals the mean ({observed_mean:.2f}), 
    confirming the Poisson property that variance = mean = λ.
    """)

    # --- Probability Calculator ---
    st.header("🎲 Click Probability Calculator")
    target_clicks = st.number_input(
        f"Calculate probability of exactly X clicks per {time_unit.lower()}:",
        min_value=0,
        max_value=50,
        value=int(lambda_rate),
        step=1
    )
    
    prob_exact = stats.poisson.pmf(target_clicks, lambda_rate)
    prob_at_least = 1 - stats.poisson.cdf(target_clicks - 1, lambda_rate)
    prob_at_most = stats.poisson.cdf(target_clicks, lambda_rate)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"P(exactly {target_clicks} clicks)", f"{prob_exact:.4f}")
    with col2:
        st.metric(f"P(≥ {target_clicks} clicks)", f"{prob_at_least:.4f}")
    with col3:
        st.metric(f"P(≤ {target_clicks} clicks)", f"{prob_at_most:.4f}")

else:
    st.info("👈 Adjust the controls in the sidebar and click 'Run Simulation' to see the Poisson distribution in action!")

