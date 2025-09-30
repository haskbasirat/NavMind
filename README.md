Here is a complete, professional README.md file for your project, including a title, a detailed description, feature list, and setup instructions. You can copy and paste this directly into a file named README.md in your project's root folder.
NavMind: A Multi-User Web UI for Autonomous Browser Agents
A powerful and intuitive web interface for controlling and managing autonomous browser agents, built with Gradio and Python. NavMind is designed from the ground up for multiple users, featuring secure authentication, isolated sessions, and parallel task execution.
Note: Replace the link above with a real screenshot of your application! A good visual is the most important part of a README.
✨ Core Features
🔐 Secure Multi-User Authentication: Built-in sign-up and login system to protect your agent. User credentials are securely hashed and stored.
👤 Isolated User Sessions: Each logged-in user gets their own independent agent instance. Chat history, browser state, and running tasks are completely separate from other users.
⚡ Parallel Task Execution: The server is configured to handle multiple user requests concurrently, allowing several agents to run tasks at the same time without blocking each other.
🎨 Sleek Custom Interface: A modern, custom-themed dark mode UI that is clean, responsive, and user-friendly.
⚙️ Comprehensive Configuration: Easily configure agent and browser settings through the UI, including:
LLM provider, model, and temperature.
Headless mode and browser window size.
Paths for saving agent history, recordings, and downloads.
🚀 Developer Friendly: Integrated auto-reloading for rapid development. Just save a file, and the server restarts with your changes.
🛠️ Technology Stack
Backend: Python
Web Framework: Gradio
Auto-Reload Server: Uvicorn
Environment Management: python-dotenv
🚀 Getting Started
Follow these instructions to set up and run the project on your local machine.
1. Prerequisites
Python 3.10+
Git
2. Installation
First, clone the repository to your local machine:
code
Bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
3. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.
On Windows:
code
Bash
python -m venv .venv
.\.venv\Scripts\activate
On macOS / Linux:
code
Bash
python3 -m venv .venv
source .venv/bin/activate
4. Install Dependencies
This project's dependencies are managed in requirements.txt.
Important: If you don't have a requirements.txt file yet, create one by running this command in your activated virtual environment:
code
Bash
pip freeze > requirements.txt
Now, install all the required packages:
code
Bash
pip install -r requirements.txt
5. Environment Setup
The application uses a .env file to manage secret keys and configurations.
Create a file named .env in the root of the project and add your API keys and any other necessary variables. You can use the example below as a template:
.env file:
code
Code
# Example for Google Gemini
GOOGLE_API_KEY="your_google_api_key_here"

# Example for OpenAI
# OPENAI_API_KEY="your_openai_api_key_here"

# VNC password if you are using the browser view
VNC_PASSWORD="yourvncpword"
🏃‍♀️ Running the Application
You can run the server in two modes:
1. Standard Mode
This is the standard way to run the application.
code
Bash
python webui.py
2. Development Mode (with Auto-Reload)
This mode is perfect for development. The server will automatically restart whenever you save a change to a Python file.
code
Bash
python webui.py --reload
Once the server is running, open your browser and navigate to http://localhost:7788.
Signing Up a New User
The application has a built-in sign-up system. When you first arrive at the login page:
Click the "Sign Up" tab.
Enter your desired username and password.
Click the "Sign Up" button.
Your account will be created in a local user_database.json file, and you will be logged in automatically. For future sessions, you can use the "Login" tab.
📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
