# Portfolio Website

## Overview

This repository hosts my personal portfolio website, designed to showcase my skills, projects, and professional experience. The application is built using a modern, containerized architecture, separating the front-end components (Streamlit) from the back-end services (Flask API).

This dual-framework approach allows for both interactive data-focused showcases (via Streamlit) and robust, traditional web features (via Flask).

## Features

* **Interactive Demonstrations:** Uses Streamlit for data-intensive projects, dashboards, and interactive showcases.
* **Robust Backend API:** A Flask-based RESTful API handles core logic, data fetching, and content management.
* **Modular Architecture:** Clear separation between the `Frontend` (Streamlit app) and `Backend` (Flask app).
* **Containerized Environment:** Fully configured with Docker and Docker-Compose for easy and consistent deployment across any environment.

## Technologies Used

| Category | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python | The core programming language. |
| **Backend** | **Flask** | A lightweight WSGI web application framework used to build the REST API. |
| **Frontend** | **Streamlit** | An open-source app framework used to turn data scripts into shareable web apps. |
| **Containerization** | **Docker** | Used to package the Flask and Streamlit applications into isolated containers. |
| **Orchestration** | **Docker Compose** | Used to define and run the multi-container application with a single command. |

## API Endpoints (Backend):

| Method                             | Route                     | Description                      |
| ---------------------------------- | ------------------------- | -------------------------------- |
| GET                                | `/get_projects`           | Fetch all projects               |
| POST                               | `/insert_project`         | Add a new project                |
| GET                                | `/get_singleproject/<id>` | Fetch a single project by ID     |
| GET                                | `/get_skills`             | Fetch all skills                 |
| POST                               | `/insert_skills`          | Add a skill                      |
| GET                                | `/get_singleskill/<id>`   | Fetch skill by ID                |
| GET                                | `/get_experience`         | Fetch all experiences            |
| POST                               | `/insert_experience`      | Add an experience                |
| GET                                | `/get_singleexp/<id>`     | Fetch experience by ID           |
| GET                                | `/analytics/overview`     | Fetch summary counts & stats     |
| GET                                | `/analytics/trend`        | Fetch skills distribution trends |


Here are some of the key API routes provided by the Flask backend:
## Installation and Setup

### Prerequisites

You need to have the following installed on your system:

* [**Docker**](https://docs.docker.com/get-docker/)
* [**Docker Compose**](https://docs.docker.com/compose/install/)

### Local Setup (Recommended via Docker)

The easiest way to run this project is using Docker Compose, which will build and start both the Flask and Streamlit services simultaneously.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/vishalm019/portfolio.git
    cd portfolio
    ```

2.  **Build and Run the Containers:**
    Execute the following command in the root directory (where `docker-compose.yaml` is located):
    ```bash
    docker-compose up --build
    ```
    *The `--build` flag ensures that the latest images are built from the Dockerfiles.*

3.  **Access the Application:**
    Once the services are running:
    * **Frontend (Streamlit):** Access the main portfolio interface at `http://localhost:8501`
    * **Backend (Flask API):** The API should be accessible on a different port, often `http://localhost:5000` (check your `docker-compose.yaml` file for exact port mapping).

---

### Alternative Local Setup (Without Docker)

If you prefer to run the applications directly on your host machine:

1.  **Install Dependencies:**
    You will need to install dependencies for both the Backend and Frontend.

    ```bash
    # Backend Dependencies (Flask)
    pip install -r Backend/requirements.txt

    # Frontend Dependencies (Streamlit)
    pip install -r Frontend/requirements.txt
    ```

2.  **Run the Backend (Flask):**
    ```bash
    cd Backend
    python app.py
    ```
    *The Flask API should now be running, typically at `http://127.0.0.1:5000`.*

3.  **Run the Frontend (Streamlit):**
    Open a *new* terminal window.
    ```bash
    cd Frontend
    streamlit run app.py
    ```
    *The Streamlit application will start and provide a local URL in your console.*

## 🗺️ Project Structure

The repository is divided into two main components:

portfolio/
├── Backend/
│   ├── Dockerfile             # Docker instructions for the Flask API
│   ├── app.py                 # Main Flask application file
│   └── requirements.txt       # Python dependencies for the Flask API
|
├── Frontend/
│   ├── Dockerfile             # Docker instructions for the Streamlit app
│   ├── app.py                 # Main Streamlit application file
│   └── requirements.txt       # Python dependencies for the Streamlit app
|
├── .devcontainer/             # Configuration for VS Code Dev Containers (optional)
├── docker-compose.yaml        # Defines and links the Backend and Frontend services
└── README.md                  # This file