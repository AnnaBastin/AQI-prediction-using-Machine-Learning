import streamlit as st
import Comparison
import Simulation
import Camera
#import RealTime


st.set_page_config(
    page_title="AQI Prediction System",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM DARK ATMOSPHERIC THEME
# --------------------------------------------------
st.markdown("""
<style>

/* App background with gradient */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #0b1220 40%,
        #0a0f14 100%
    );
    color: #E6EDF3;
}

/* Soft glow overlay */
.stApp::before {
    content: "";
    position: fixed;
    top: -200px;
    left: -200px;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(168,85,247,0.15), transparent 70%);
    filter: blur(120px);
    z-index: -1;
}

.stApp::after {
    content: "";
    position: fixed;
    bottom: -200px;
    right: -200px;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(0,255,156,0.15), transparent 70%);
    filter: blur(120px);
    z-index: -1;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0a0f14,
        #06090d
    );
    border-right: 1px solid #1f2933;
}

/* Headers with neon glow */
h1 {
    color: #00FF9C;
    text-shadow: 0 0 12px #00FF9C, 0 0 24px #A855F7;
}

h2, h3 {
    color: #A855F7;
    text-shadow: 0 0 10px rgba(168,85,247,0.6);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#00FF9C,#A855F7);
    color: black;
    border-radius: 10px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 12px rgba(168,85,247,0.7);
}

/* Sidebar radio buttons */
div[role="radiogroup"] label {
    color: #E6EDF3;
}

/* Separator */
hr {
    border: 1px solid #30363D;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
"""
<h1 style='text-align:center'>
🌫️ AQI Prediction System
</h1>
""",
unsafe_allow_html=True
)

st.markdown("---")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("📡 Navigation")

choice = st.sidebar.radio(
    "Select Mode",
    [
        "🧪 Sensor Value-Based Simulation",
        #"📡 Sensor Based Real-Time Prediction",
        "📷 Camera Based Real Time Prediction",
        "📊 Comparison of Models"
    ]
)

# --------------------------------------------------
# MODULE SWITCHING
# --------------------------------------------------

if choice == "📊 Comparison of Models":
    Comparison.run()

elif choice == "🧪 Sensor Value-Based Simulation":
    Simulation.run()

elif choice == "📷 Camera Based Real Time Prediction":
    Camera.run()

#elif choice == "📡 Sensor Based Real-Time Prediction":
    #RealTime.run()


