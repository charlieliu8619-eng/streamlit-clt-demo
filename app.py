import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Ad Revenue & The Central Limit Theorem",
    page_icon="📈",
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
        background-color: #00b0f0; /* A blue shade */
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
        color: #1E3A8A; /* Dark Blue */
    }
</style>
""", unsafe_allow_html=True)


# --- App Header ---
st.title("📈 Ad Revenue Simulation & The Central Limit Theorem")
st.markdown("""
This dashboard demonstrates the **Central Limit Theorem (CLT)** using a real-world example relevant to content creators: **daily ad revenue**.

Daily ad revenue can be unpredictable. Some days might have unusually high earnings due to a viral post, while most days are average. This results in a **skewed distribution**. The CLT tells us that if we take the *average* revenue over a sample of many days (e.g., 30 days) and repeat this process many times, the distribution of these averages will look like a **normal distribution (a bell curve)**.
---
""")

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("⚙️ Simulation Controls")
    st.markdown("Adjust the parameters to see how the distributions change.")

    # Input for the average daily revenue
    avg_daily_revenue = st.number_input(
        "Average Daily Revenue ($):",
        min_value=10,
        max_value=1000,
        value=150,
        step=10,
        help="This sets the average for our simulated daily revenue data. It's the 'scale' parameter for the exponential distribution."
    )

    # Slider for the number of days in each sample
    sample_size = st.slider(
        "Days in each sample (N):",
        min_value=1,
        max_value=100,
        value=30,
        step=1,
        help="How many days of revenue to average at a time? A typical value is 30 for a monthly average. As N increases, the distribution of averages becomes more normal."
    )

    # Slider for the number of samples to simulate
    num_samples = st.slider(
        "Number of samples to simulate:",
        min_value=100,
        max_value=10000,
        value=2000,
        step=100,
        help="How many times should we calculate the sample average? More samples create a smoother final distribution."
    )

    # A button to run the simulation
    run_simulation = st.button("Run Simulation")


# --- Main Panel for Output ---
if run_simulation:
    st.header("📊 Simulation Results")

    with st.spinner("Simulating revenue data..."):
        # We generate a large pool of daily revenue data using an exponential distribution
        # This distribution is skewed, which is realistic for daily revenue.
        total_days_to_simulate = num_samples * sample_size
        daily_revenue_data = np.random.exponential(scale=avg_daily_revenue, size=total_days_to_simulate)
        
        # Reshape data into our samples and calculate the mean of each sample
        samples = daily_revenue_data.reshape(num_samples, sample_size)
        sample_means = np.mean(samples, axis=1)

    # --- Display Plots Side-by-Side ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribution of Daily Revenue")
        # Plotting the distribution of the underlying daily revenue data
        fig1 = px.histogram(
            x=daily_revenue_data,
            title="Original (Skewed) Daily Data",
            labels={'x': 'Daily Revenue ($)', 'y': 'Frequency'},
            template="plotly_white"
        )
        fig1.update_traces(marker_color='#FF5733', opacity=0.7)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("Notice that this distribution is **not a bell curve**. It's heavily skewed to the right, with a long tail representing rare, high-earning days.")

    with col2:
        st.subheader("Distribution of Sample Averages")
        # Plotting the distribution of the sample means
        fig2 = px.histogram(
            x=sample_means,
            title=f"Averages of {sample_size}-Day Samples",
            labels={'x': f'Average Revenue over {sample_size} days ($)', 'y': 'Frequency'},
            template="plotly_white"
        )
        fig2.update_traces(marker_color='#00b0f0', opacity=0.7)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(f"This distribution **is a bell curve**, centered around the true average of ${avg_daily_revenue:.2f}. This is the Central Limit Theorem in action!")

    # --- Explanation of the Results ---
    st.header("💡 Business Implications")
    st.markdown(f"""
    This simulation shows why the Central Limit Theorem is so important for Raptive.

    1.  **Predictability from Unpredictability:** Even though individual daily earnings for a creator are volatile and skewed (as seen in the left chart), the average earnings over a period (like a month) become very predictable and stable (as seen in the right chart).

    2.  **Accurate Forecasting:** Because the distribution of these averages is normal, we can use its statistical properties to create accurate earnings forecasts and confidence intervals. For example, we can say with high confidence that a creator's average monthly revenue will fall within a certain range.

    3.  **Risk Management:** Understanding this principle helps manage risk. We know that a single bad day won't sink long-term earnings, as it will be balanced out over the sampling period.

    By increasing the **'Days in each sample (N)'** slider, you'll see the bell curve on the right become even narrower and more defined, signifying that longer-term averages are even more stable and predictable.
    """)

else:
    st.info("👈 Adjust the controls in the sidebar and click 'Run Simulation' to see the results!")

