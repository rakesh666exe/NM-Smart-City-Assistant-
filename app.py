# Install dependencies
# !pip install gradio matplotlib transformers torch

import gradio as gr
import matplotlib.pyplot as plt
from transformers import pipeline

# =======================
# Load Hugging Face LLM
# =======================
llm = pipeline("text2text-generation", model="google/flan-t5-xl", device=-1)

# =======================
# AI Assistant function
# =======================
def ask_ai(user_input):
    if not user_input.strip():
        return "⚠️ Please enter a question."
    response = llm(user_input, max_new_tokens=200, temperature=0.7)
    return response[0]["generated_text"]

# =======================
# Dashboard plots
# =======================
def plot_aqi():
    aqi_data = [50, 60, 70, 80, 65, 55, 75]
    fig, ax = plt.subplots(facecolor="#1e293b")
    ax.plot(aqi_data, marker="o", color="#00c853", linewidth=2)
    ax.set_facecolor("#1e293b")
    ax.set_title("AQI Over Time", color="white")
    ax.set_ylabel("AQI", color="white")
    ax.set_xlabel("Days", color="white")
    ax.tick_params(colors="white")
    return fig

def plot_energy():
    energy_data = [300, 320, 310, 290, 330, 340, 325]
    fig, ax = plt.subplots(facecolor="#1e293b")
    ax.plot(energy_data, color="orange", marker="s", linewidth=2)
    ax.set_facecolor("#fff")
    ax.set_title("Energy Usage (MW)", color="white")
    ax.set_ylabel("MW", color="white")
    ax.set_xlabel("Days", color="white")
    ax.tick_params(colors="white")
    return fig

# =======================
# Reports
# =======================
def get_report():
    report_text = """
    ✅ Energy Consumption reduced by 5%<br>
    ✅ AQI improved from 80 → 70<br>
    ✅ Water usage reduced by 10%<br>
    ✅ Smart transport usage increased by 15%<br>
    """
    return report_text.strip()

# =======================
# Define Gradio UI
# =======================
custom_css = """
.gradio-container {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1, h2, h3,p {color: white;
    text-align: center;
}

.card {color: white;
    background: rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    margin: 10px 0;
}

button {
    background-color: #4CAF50 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px 16px !important;
    font-weight: bold !important;
    transition: 0.3s;
}

button:hover {
    background-color: #45a049 !important;
}

textarea, input {
    border-radius: 10px !important;
    padding: 8px !important;
    background: #1e293b !important;
    color: white !important;
}
"""

with gr.Blocks(css=custom_css, theme="soft") as demo:
    with gr.Tab("🏠 Home"):
        with gr.Column(elem_classes="card"):
            gr.HTML("<h2>🌆 Smart City Assistant</h2>")
            gr.HTML("""
            <p>Welcome to the <b>Smart City AI-powered Assistant</b> 🚀<br>
            Get <b>real-time insights, AI-powered citizen support, and smart dashboards</b><br>
            for energy, water, transport, and environment monitoring.</p>
            """)

    with gr.Tab("🤖 AI Assistant"):
        with gr.Column(elem_classes="card"):
            gr.HTML("<h2>🤖 Ask the AI Assistant</h2>")
            user_input = gr.Textbox(label="💬 Your Question", lines=2, placeholder="Type your question here...")
            output = gr.Textbox(label="✨ AI Response", lines=6)
            gr.Button("⚡ Generate Response").click(ask_ai, inputs=user_input, outputs=output)

    with gr.Tab("📊 Dashboard"):
        gr.HTML("<h2>📊 Smart City Dashboard</h2>")
        with gr.Row():
            with gr.Column(elem_classes="card"):
                gr.HTML("<h3>🌍 Air Quality Index (AQI)</h3>")
                aqi_plot = gr.Plot()
                gr.Button("📈 Show AQI").click(fn=plot_aqi, outputs=aqi_plot)

            with gr.Column(elem_classes="card"):
                gr.HTML("<h3>💡 Electricity Consumption</h3>")
                energy_plot = gr.Plot()
                gr.Button("⚡ Show Energy").click(fn=plot_energy, outputs=energy_plot)

    with gr.Tab("📑 Reports"):
        with gr.Column(elem_classes="card"):
            gr.HTML("<h2 style='color:white;''>📑 Weekly Sustainability Report</h2>")
            report_output = gr.Textbox(label="🌱 Report", lines=6)
            gr.Button("📄 Generate Report").click(get_report, outputs=report_output)

    with gr.Tab("ℹ️ About"):
        with gr.Column(elem_classes="card"):
            gr.HTML("<h2>ℹ️ About This Project</h2>")
            gr.HTML("""
            <p>The <b>Smart City Assistant</b> leverages<br>
            🧠 Hugging Face Transformers + 🎨 Gradio<br>
            to provide <b>AI-powered services, dashboards, and citizen engagement tools</b>.<br><br>
            🌱 Designed for <b>sustainability, transparency, and efficiency</b>.</p>
            """)

# =======================
# Launch App
# =======================
if __name__ == "__main__":
    demo.launch(share=True)
