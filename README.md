# NavMind: A Multi-User Web UI for Autonomous Browser Agents

A powerful and intuitive web interface for controlling and managing autonomous browser agents, built with Gradio and Python. **NavMind** is designed from the ground up for multiple users, featuring secure authentication, isolated sessions, and parallel task execution.

[![NavMind Screenshot]([assets/Screenshot 2025-09-29 225455.png](https://github.com/haskbasirat/NavMind/blob/efdbf85f0c7a08562907c20bd65bb46fea07b208/assets/Screenshot%202025-09-29%20225455.png))
](https://github.com/haskbasirat/NavMind/blob/efdbf85f0c7a08562907c20bd65bb46fea07b208/assets/Screenshot%202025-09-29%20225455.png)

https://github.com/haskbasirat/NavMind/blob/efdbf85f0c7a08562907c20bd65bb46fea07b208/assets/Screenshot%202025-09-29%20225550.png

https://github.com/haskbasirat/NavMind/blob/efdbf85f0c7a08562907c20bd65bb46fea07b208/assets/Screenshot%202025-09-29%20225709.png

https://github.com/haskbasirat/NavMind/blob/efdbf85f0c7a08562907c20bd65bb46fea07b208/assets/Screenshot%202025-09-29%20225722.png

assets/Screenshot 2025-09-29 225733.png

> **Note**: Replace the link above with a real screenshot of your application! A good visual is the most important part of a README.

---

## ✨ Core Features

- **🔐 Secure Multi-User Authentication**  
  Built-in sign-up and login system to protect your agent. User credentials are securely hashed and stored in a local JSON file.

- **👤 Isolated User Sessions**  
  Each logged-in user gets their own independent agent instance. Chat history, browser state, and running tasks are completely separate from other users.

- **⚡ Parallel Task Execution**  
  The server is configured to handle multiple user requests concurrently, allowing several agents to run tasks at the same time without blocking each other.

- **🎨 Sleek Custom Interface**  
  A modern, custom-themed dark mode UI that is clean, responsive, and user-friendly.

- **⚙️ Comprehensive Configuration**  
  Easily configure agent and browser settings through the UI, including:
  - LLM provider, model, and temperature.
  - Headless mode and browser window size.
  - Paths for saving agent history, recordings, and downloads.

- **🚀 Developer Friendly**  
  Integrated auto-reloading for rapid development. Just save a file, and the server restarts with your changes.

---

## 🛠️ Technology Stack

- **Backend**: Python  
- **Web Framework**: Gradio  
- **Auto-Reload Server**: Uvicorn  
- **Environment Management**: `python-dotenv`  

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### 1. Prerequisites

- Python 3.10+  
- Git  

### 2. Installation

Clone the repository:

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 3. Create a Virtual Environment

It’s highly recommended to use a virtual environment to manage dependencies.

**On Windows:**
```bash
python -m venv .venv
.\.venv\Scriptsctivate
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

Install required packages:

```bash
pip install gradio uvicorn python-dotenv
# Add any other specific libraries your project needs, e.g.:
# pip install langchain-google-genai browser-use ...
```

Or, if a `requirements.txt` is provided:

```bash
pip install -r requirements.txt
```

### 5. Environment Setup

The application uses a `.env` file to manage secret keys and configurations.  
Create a file named `.env` in the root of the project and add your API keys:

```bash
# Example for Google Gemini
GOOGLE_API_KEY="your_google_api_key_here"

# Example for OpenAI
# OPENAI_API_KEY="your_openai_api_key_here"

# VNC password if you are using the browser view
VNC_PASSWORD="yourvncpword"
```

---

## 🏃‍♀️ Running the Application

You can run the server in two modes:

### 1. Standard Mode
```bash
python webui.py
```

### 2. Development Mode (with Auto-Reload)
This mode automatically restarts the server when you save changes:

```bash
python webui.py --reload
```

Once the server is running, open your browser and navigate to:

```bash
http://localhost:7788
```

---

## 👤 Signing Up a New User

The application has a built-in sign-up system integrated into the login screen:

1. Navigate to the running application in your browser.  
2. Click the **Sign Up** tab.  
3. Enter your desired username and password.  
4. Click **Sign Up**.  

Your account will be created in a local `user_database.json` file, and you will be logged in automatically. For future sessions, use the **Login** tab.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


