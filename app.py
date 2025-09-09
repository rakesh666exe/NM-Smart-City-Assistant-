import streamlit as st
import matplotlib.pyplot as plt
import os

from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai import Credentials

# =======================
# Load secrets safely
# =======================
# Use environment variables directly as Streamlit secrets are not available in this environment
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY", "v2pjUHPAm5HfLBGpVN5T1-DHjM3tbAVIzyQmEUhMS_0v")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "443a8ed4-48fd-4630-ab81-e5a5480dd375")


# =======================
# Initialize LLM safely
# =======================
def _make_llm():
    credentials = Credentials(url=WATSONX_URL, api_key=WATSONX_APIKEY)
    return Model(
        model_id="ibm/granite-13b-instruct-v2",
        credentials=credentials,
        params={
            "decoding_method": "sample",
            "temperature": 0.7,
            "max_new_tokens": 500,
        },
        project_id=WATSONX_PROJECT_ID,
    )

# If inside Streamlit runtime → cache the LLM
if os.environ.get("STREAMLIT_RUNTIME"):
    @st.cache_resource
    def initialize_llm():
        return _make_llm()
else:
    # bare Python mode
    def initialize_llm():
        return _make_llm()

llm = initialize_llm()

# =======================
# Page config
# =======================
st.set_page_config(page_title="Smart City Assistant", page_icon="🏙", layout="wide")

# =======================
# Custom CSS
# =======================
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to right, #0f2027, #203a43, #2c5364),
                          url("https://cdn.pixabay.com/photo/2017/06/19/10/31/city-2418970_1280.jpg");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }
    .main-title {
        font-size: 40px;
        text-align: center;
        color: #00f5ff;
        animation: glow 1.5s infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #00f5ff; }
        to   { text-shadow: 0 0 20px #00f5ff; }
    }
    .report-box {
        background-color: rgba(40, 40, 40, 0.9);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# =======================
# Sidebar Navigation
# =======================
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Home", "🤖 AI Assistant", "📊 Dashboard", "📑 Reports", "ℹ️ About"])

# =======================
# Home
# =======================
if page == "🏠 Home":
    st.markdown('<h1 class="main-title">🌆 Smart City Assistant</h1>', unsafe_allow_html=True)
    st.write("""
    Welcome to the Smart City AI-powered Assistant.
    This platform provides **real-time insights**, AI-powered citizen support, and smart dashboards
    for energy, water, transport, and environment monitoring.
    """)

# =======================
# AI Assistant
# =======================
elif page == "🤖 AI Assistant":
    st.markdown('<h1 class="main-title">🤖 Smart City AI Assistant</h1>', unsafe_allow_html=True)
    user_input = st.text_area("💬 Ask me anything about Smart City services:")

    if st.button("Generate Response"):
        if user_input.strip():
            with st.spinner("Thinking..."):
                response = llm.generate_text(prompt=user_input)
                st.success("AI Response:")
                st.write(response)
        else:
            st.warning("⚠️ Please enter a question.")

# =======================
# Dashboard
# =======================
elif page == "📊 Dashboard":
    st.markdown('<h1 class="main-title">📊 Smart City Dashboard</h1>', unsafe_allow_html=True)
    st.write("Visualizing Smart City data for better decision-making:")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Air Quality Index (AQI)")
        aqi_data = [50, 60, 70, 80, 65, 55, 75]
        plt.plot(aqi_data, marker='o')
        plt.title("AQI Over Time")
        st.pyplot(plt)

    with col2:
        st.subheader("Electricity Consumption")
        energy_data = [300, 320, 310, 290, 330, 340, 325]
        plt.plot(energy_data, color='orange', marker='s')
        plt.title("Energy Usage (MW)")
        st.pyplot(plt)

# =======================
# Reports
# =======================
elif page == "📑 Reports":
    st.markdown('<h1 class="main-title">📑 Sustainability Reports</h1>', unsafe_allow_html=True)

    st.subheader("🌱 Weekly Report")
    report_text = """
    ✅ Energy Consumption reduced by 5%
    ✅ AQI improved from 80 → 70
    ✅ Water usage reduced by 10%
    ✅ Smart transport usage increased by 15%
    """
    st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)

    st.download_button("⬇ Download Report", report_text, file_name="sustainability_report.txt")

# =======================
# About
# =======================
elif page == "ℹ️ About":
    st.markdown('<h1 class="main-title">ℹ️ About This Project</h1>', unsafe_allow_html=True)
    st.write("""
    The **Smart City Assistant** leverages **IBM WatsonX AI** and **Streamlit** to
    provide real-time AI-powered services, dashboards, and citizen engagement tools.
    🚀 Designed for **sustainability, transparency, and efficiency**.
    """)
    
    
