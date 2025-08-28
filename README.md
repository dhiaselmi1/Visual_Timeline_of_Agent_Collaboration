# Visual Timeline of Agent Collaboration 🤖

A full-stack application for visualizing and tracking the outputs of a multi-agent system.

## Project Description

This project provides a comprehensive solution for monitoring and understanding AI agent workflows. It features a **Streamlit** frontend for user interaction and a **FastAPI** backend that manages the core agent logic. The application captures and timestamps all agent outputs, presenting them in a clear, chronological timeline. It leverages the **Llama 3** model to power multiple specialized AI agents that collaborate to complete tasks. Users can run these agents and observe their collaboration in real-time, making it an ideal tool for debugging and analyzing multi-agent systems.

## 🚀Features

* **Interactive Timeline⏳**: A dynamic, chronological view of agent responses.
* **Agent Grouping 🤝**: Organizes and displays interactions by agent and topic.
* **Specialized AI Agents 🧠**: Utilizes Llama 3 to power multiple agents, each with a unique role:
    * **Research Agent 🔬**: Finds factual answers and gathers context.
    * **Summarizer Agent 📝**: Condenses raw text into concise bullet points.
    * **Devil's Advocate Agent😈**: Challenges assumptions and raises counterpoints.
    * **Insight Agent💡**: Extracts actionable takeaways from conversation history.
* **PDF Export📄**: Generate a shareable PDF report of the entire timeline.
* **Modular Agent Architecture🧱**: Easily add new specialized agents to the backend.

## Technologies

**Frontend:**
* `Streamlit`: For building the interactive web application.

**Backend:**
* `FastAPI`: A modern, fast web framework for building the API.
* `Llama 3`: The large language model used to power the agents.
* `PDFKit`: A Python wrapper for `wkhtmltopdf` to generate PDF reports.
* `Requests`: For communication between the frontend and backend.
* `Python`
---
## 📂Project Structure


```
agent_timeline/
├── backend/
│   ├── agents/
│   │   ├── base.py
│   │   ├── devil_agent.py
│   │   ├── insight_agent.py
│   │   ├── research_agent.py
│   │   └── summarizer_agent.py
│   ├── main.py
├── frontend/
│   └── app.py
├── memory/
│   └── memory_store.json
└── README.md
```

---
## Setup and Installation

### Prerequisites

* Python 3.7+
* `wkhtmltopdf` installed on your system. You can download it from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html). Make sure the installation path is added to your system's PATH environment variable.

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You will need to create a `requirements.txt` file from your project dependencies.*

3.  Run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```
    The backend will run on `http://localhost:8000`.

### Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You will need to create a `requirements.txt` file from your project dependencies.*

3.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
    The frontend will open in your browser, running on `http://localhost:8501`.

## Usage

1.  Ensure both the backend and frontend servers are running.
2.  In the Streamlit app, enter a topic and a research query in the sidebar.
3.  Choose an agent from the dropdown menu and click "Run Agent" to start the collaboration.
4.  Observe the live timeline as the agents process the task and display their outputs.
5.  Click the "Download as PDF" button to export the full report of the collaboration.
