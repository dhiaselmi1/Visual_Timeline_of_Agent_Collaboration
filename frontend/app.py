import streamlit as st
import requests
from datetime import datetime
from collections import defaultdict
import pdfkit
import os

st.set_page_config(page_title="Agent Timeline", layout="wide")

# --- Configuration ---
FASTAPI_URL = "http://localhost:8000"
API_URL = "http://localhost:8000"

# Configuration for PDF export only
# Attempt to find wkhtmltopdf in system's PATH
try:
    path_wkhtmltopdf = pdfkit.configuration().wkhtmltopdf
except OSError:
    # If not found, try a common Windows path as a fallback
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    if not os.path.exists(path_wkhtmltopdf):
        st.error("wkhtmltopdf not found. Please install it and ensure it's in your system's PATH or update the script with the correct path.")
        st.stop()

config_pdf = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Visual settings for each agent
AGENT_VISUALS = {
    "Research": {"icon": "🔬", "color": "#4CAF50"},
    "Summarizer": {"icon": "📝", "color": "#2196F3"},
    "Insight": {"icon": "💡", "color": "#FFC107"},
    "Devil": {"icon": "😈", "color": "#F44336"},
    "default": {"icon": "🤖", "color": "#9E9E9E"}
}

# --- Helper Functions ---
@st.cache_data(ttl=60)  # Cache logs for 60 seconds
def fetch_logs(topic):
    """Fetches and returns logs for a given topic."""
    try:
        response = requests.get(f"{API_URL}/logs/{topic}")
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json().get("logs", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the API: {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred while fetching logs: {e}")
        return None

def generate_html_report(logs_data, topic):
    """Generates an HTML string from the logs for reporting."""
    html = f"<html><head><title>Agent Collaboration Report: {topic}</title>"
    html += """
    <style>
        body { font-family: sans-serif; }
        .log-container { border-left: 4px solid; padding: 10px; margin-bottom: 10px; background-color: #f9f9f9; }
        .agent { font-weight: bold; font-size: 1.2em; }
        .timestamp { color: #555; font-size: 0.8em; }
        .content { margin-top: 5px; }
        h1, h2 { color: #333; }
    </style>
    </head><body>"""
    html += f"<h1>🤖 Agent Collaboration Report</h1>"
    html += f"<h2>Topic: {topic}</h2><hr>"

    for log in logs_data:
        agent_name = log.get('agent', 'Unknown')
        visuals = AGENT_VISUALS.get(agent_name, AGENT_VISUALS["default"])
        color = visuals['color']
        icon = visuals['icon']

        dt_object = datetime.fromisoformat(log['timestamp'])
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

        html += f'<div class="log-container" style="border-left-color: {color};">'
        html += f'<div class="agent">{icon} {agent_name}</div>'
        html += f'<div class="timestamp">🕒 {formatted_time}</div>'
        html += f'<div class="content"><p>{log["content"]}</p></div>'
        html += '</div>'

    html += "</body></html>"
    return html


# --- Sidebar ---
st.sidebar.title("⚙️ Controls")
topic = st.sidebar.text_input("Topic", "IA")
query = st.sidebar.text_input("Research Query", "")

agent_choice = st.sidebar.selectbox(
    "Choose an Agent",
    list(AGENT_VISUALS.keys())[:-1]  # Exclude default
)

if st.sidebar.button("Run Agent"):
    with st.spinner(f"Running {agent_choice} agent..."):
        payload = {"topic": topic}
        if agent_choice == "Research":
            payload["query"] = query

        try:
            response = requests.post(f"{FASTAPI_URL}/run/{agent_choice.replace(' ', '_')}", json=payload)
            response.raise_for_status()
            st.success(f"{agent_choice} agent ran successfully!")
            st.cache_data.clear()  # Clear cache to fetch new logs
        except requests.exceptions.RequestException as e:
            st.error(f"Error running {agent_choice}: {e}")

if st.sidebar.button("Refresh Logs"):
    st.cache_data.clear()
    st.success("Logs cache cleared. Refreshing...")

# --- Main content ---
st.title("🤖 Visual Timeline of Agent Collaboration")
st.subheader(f"📜 Timeline for topic: {topic}")

logs = fetch_logs(topic)

if logs is None:
    st.warning("Could not retrieve logs from the server.")
elif not logs:
    st.info(f"No logs found yet for the topic: '{topic}'. Run an agent to begin.")
else:
    # Group logs by agent
    grouped_logs = defaultdict(list)
    for log in logs:
        grouped_logs[log['agent']].append(log)

    # Render grouped logs in a timeline format
    for agent_name, agent_logs in grouped_logs.items():
        visuals = AGENT_VISUALS.get(agent_name, AGENT_VISUALS["default"])
        st.markdown(
            f"<h3 style='color: {visuals['color']};'>{visuals['icon']} Agent: {agent_name}</h3>",
            unsafe_allow_html=True
        )

        for log in sorted(agent_logs, key=lambda x: x['timestamp']):
            try:
                dt_object = datetime.fromisoformat(log['timestamp'])
                formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

                with st.expander(f"🕒 {formatted_time}", expanded=False):
                    st.markdown(log['content'])

            except (ValueError, TypeError) as e:
                st.warning(f"Could not parse timestamp '{log.get('timestamp')}'. Skipping log. Error: {e}")

    # --- Export Section ---
    st.markdown("---")
    st.subheader("📄 Export Timeline")

    report_html = generate_html_report(logs, topic)

    try:
        report_pdf = pdfkit.from_string(report_html, False, configuration=config_pdf)
        st.download_button(
            label="📥 Download as PDF",
            data=report_pdf,
            file_name=f"agent_report_{topic}.pdf",
            mime="application/pdf",
        )
    except Exception as e:
        st.error(f"Could not generate PDF: {e}")