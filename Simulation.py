import streamlit as st
import time
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go


def run():

    # -------------------------------
    # GAUGE ANIMATION FUNCTION
    # -------------------------------
    def animate_gauge(target_aqi, duration=4):
        steps = 40
        delay = duration / steps
        gauge_placeholder = st.empty()

        for i in range(steps + 1):
            value = target_aqi * (i / steps)

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=value,
                    title={'text': "AQI Level"},
                    gauge={
                        'axis': {'range': [0, 500]},
                        'bar': {
                'color': "black",
                'thickness': 0.80   # thinner needle bar
            },
                        'steps': [
                            {'range': [0, 50], 'color': "#4CAF50"},
                            {'range': [50, 100], 'color': "#FFEB3B"},
                            {'range': [100, 200], 'color': "#FF9800"},
                            {'range': [200, 500], 'color': "#F44336"},
                        ],
                    }
                )
            )

            gauge_placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(delay)

    # -------------------------------
    # LOAD MODEL ONLY ONCE
    # -------------------------------
    if "simulation_model" not in st.session_state:
        try:
            st.session_state.simulation_model = joblib.load("aqi_model.pkl")
        except Exception:
            st.session_state.simulation_model = None

    model = st.session_state.simulation_model

    # -------------------------------
    # SENSOR RANGES
    # -------------------------------
    RANGES = {
        "pm25": (12.916628, 400.863043),
        "nh3": (0.0, 50.0),
        "co": (0.01, 10.0)
    }

    # -------------------------------
    # UI
    # -------------------------------
    st.title("☁️ Urban Air Quality: Sky-Fusion System")

    st.markdown(
        "**Mode:** <span style='color:green'>Simulation (Manual Test)</span>",
        unsafe_allow_html=True
    )

    st.write("Enter chemical sensor values to predict AQI using Gradient Boosting.")

    if model is None:
        st.error("⚠️ Model not found! Please make sure 'aqi_model.pkl' is in same folder.")
        return

    st.markdown("---")

    st.markdown(
        """
        <div style="padding:10px;border-radius:5px;background-color:#1E2A40;
        color:#4caf50;border-left:5px solid #4caf50;">
        🧪 Chemical Domain (Simulation)
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------
    # INPUT FIELDS
    # -------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        pm25 = st.number_input(
            "PM2.5 (µg/m³)",
            min_value=RANGES["pm25"][0],
            max_value=RANGES["pm25"][1],
            value=RANGES["pm25"][0],
            step=0.1
        )
        st.caption(f"Range: {RANGES['pm25'][0]} – {RANGES['pm25'][1]}")

    with col2:
        co_level = st.number_input(
            "CO (ppm)",
            min_value=RANGES["co"][0],
            max_value=RANGES["co"][1],
            value=RANGES["co"][0],
            step=0.01
        )
        st.caption(f"Range: {RANGES['co'][0]} – {RANGES['co'][1]}")

    with col3:
        nh3_level = st.number_input(
            "NH3 (µg/m³)",
            min_value=RANGES["nh3"][0],
            max_value=RANGES["nh3"][1],
            value=RANGES["nh3"][0],
            step=0.1
        )
        st.caption(f"Range: {RANGES['nh3'][0]} – {RANGES['nh3'][1]}")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------
    # PREDICTION
    # -------------------------------
    if st.button("🚀 CALCULATE AQI"):

        with st.spinner("Analyzing pollutant concentrations..."):
            time.sleep(0.5)

            input_df = pd.DataFrame(
                [[pm25, co_level, nh3_level]],
                columns=['PM2.5', 'CO', 'NH3']
            )

            predicted_aqi = int(model.predict(input_df)[0])

        st.subheader("📊 Gradient Boosting Analysis Results")

        if predicted_aqi <= 50:
            status = "GOOD 🟢"
        elif predicted_aqi <= 100:
            status = "SATISFACTORY 🟡"
        elif predicted_aqi <= 200:
            status = "MODERATE 🟠"
        else:
            status = "POOR / HAZARDOUS 🔴"

        st.success(f"Status: {status}")

        # Gauge animation
        animate_gauge(predicted_aqi, duration=4)
