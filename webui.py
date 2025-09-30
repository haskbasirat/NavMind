# webui.py (parallel-ready, full login/signup, custom UI)

from dotenv import load_dotenv
load_dotenv()
import argparse
import os
import json
import hashlib
import gradio as gr
from concurrent.futures import ThreadPoolExecutor
from src.webui.interface import create_ui as create_main_app_ui, theme_map

# --- 1. User Management ---
USER_DB_PATH = "user_database.json"

def load_users():
    if not os.path.exists(USER_DB_PATH):
        return {}
    with open(USER_DB_PATH, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(USER_DB_PATH, 'w') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- 2. ThreadPoolExecutor for parallel processing ---
executor = ThreadPoolExecutor(max_workers=10)  # adjust for your CPU

def run_in_thread(fn, *args, **kwargs):
    future = executor.submit(fn, *args, **kwargs)
    return future.result()

# --- 3. Full UI creation ---
def create_ui(theme_name="Ocean"):
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    :root{
        --bg-primary: #111014; --bg-secondary: #1C1B22; --bg-tertiary: #2A2931;
        --bg-sidebar: #111014; --border-primary: #333238; --text-primary: #e5e7eb;
        --text-secondary: #9ca3af; --accent-primary: #6d28d9; --radius-sm: 6px;
        --radius-md: 10px; --header-height: 56px; --sidebar-width: 260px;
    }
    * { box-sizing: border-box !important; font-family: 'Inter', sans-serif !important; }
    html, body { background: var(--bg-primary) !important; color: var(--text-primary) !important; overflow-x: hidden !important; }
    .gradio-container { background: var(--bg-primary) !important; padding: 0 !important; }
    .gradio-group { border: none !important; padding: 0 !important; background: transparent !important; }
    #auth-container { max-width: 400px; margin: auto; padding-top: 10vh; }
    #auth-container .gradio-tabs { background-color: var(--bg-secondary); border-radius: var(--radius-md); border: 1px solid var(--border-primary); }
    #auth-container .gradio-button { background-color: var(--accent-primary); font-weight: 600; }
    #login-status, #signup-status { min-height: 24px; text-align: center; }
    .app-header {
        position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important;
        height: var(--header-height) !important; display: flex !important; align-items: center !important;
        padding: 0 1.5rem !important; z-index: 1200 !important; background: rgba(17, 16, 20, 0.8) !important;
        border-bottom: 1px solid var(--border-primary) !important; backdrop-filter: blur(8px) !important;
    }
    .app-title { font-size: 1.2rem !important; font-weight: 600 !important; color: var(--text-primary) !important; }
    .app-layout { padding-top: var(--header-height) !important; display: flex !important; }
    .app-sidebar {
        position: fixed !important; left: 0 !important; top: var(--header-height) !important;
        width: var(--sidebar-width) !important; height: calc(100vh - var(--header-height)) !important;
        background: var(--bg-sidebar) !important; border-right: 1px solid var(--border-primary) !important;
        padding: 1rem 0.75rem !important; display: flex !important; flex-direction: column !important;
        gap: 0.25rem !important; z-index: 1100 !important;
    }
    .sidebar-tab { 
        width: 100%; padding: 0.6rem 0.85rem !important; border-radius: var(--radius-sm) !important; 
        color: var(--text-secondary) !important; font-weight: 500 !important; font-size: 0.9rem !important; 
        cursor: pointer !important; display: flex !important; gap: 0.75rem !important; 
        align-items: center !important; border: none !important; background: transparent !important;
        transition: background 0.2s ease, color 0.2s ease;
    }
    .sidebar-tab:hover { background: var(--bg-tertiary) !important; color: var(--text-primary) !important; }
    .sidebar-tab.tab-active { background: var(--accent-primary) !important; color: white !important; font-weight: 600 !important; }
    .main-content { margin-left: var(--sidebar-width) !important; flex: 1 !important; }
    .content-area { padding: 1.5rem !important; }
    .section-header {
        background: var(--bg-secondary) !important; border: 1px solid var(--border-primary) !important;
        color: var(--text-primary) !important; padding: 0.5rem 0.75rem !important;
        border-radius: var(--radius-sm) !important; font-weight: 500 !important;
        font-size: 0.9rem !important; margin-bottom: 0.75rem !important;
    }
    ::-webkit-scrollbar { width: 8px !important; }
    ::-webkit-scrollbar-thumb { background: var(--bg-tertiary) !important; border-radius: 4px !important; }
    """

    with gr.Blocks(theme=gr.themes.Base(), css=css, title="NavMind") as demo:
        is_authenticated = gr.State(value=False)

        with gr.Column(elem_id="auth-container", visible=True) as auth_view:
            gr.Markdown("# Welcome to NavMind")
            with gr.Tabs():
                with gr.TabItem("Login"):
                    login_user = gr.Textbox(label="Username", placeholder="Enter your username")
                    login_pass = gr.Textbox(label="Password", type="password", placeholder="Enter your password")
                    login_btn = gr.Button("Login", variant="primary")
                    login_status = gr.Markdown(elem_id="login-status")

                with gr.TabItem("Sign Up"):
                    signup_user = gr.Textbox(label="New Username", placeholder="Choose a username")
                    signup_pass = gr.Textbox(label="New Password", type="password", placeholder="Choose a password")
                    signup_btn = gr.Button("Sign Up", variant="primary")
                    signup_status = gr.Markdown(elem_id="signup-status")

        with gr.Column(visible=False) as main_app_view:
            create_main_app_ui(theme_name=theme_name)

        def attempt_auth(current_auth_state, username, password, is_signup=False):
            if current_auth_state:
                return True, gr.update(visible=False), gr.update(visible=True), ""
            users, status_message, auth_success = load_users(), "", False
            if is_signup:
                if not username or not password:
                    status_message = "<p style='color:red;'>Username and password required.</p>"
                elif username in users:
                    status_message = f"<p style='color:red;'>Username '{username}' exists.</p>"
                else:
                    users[username] = hash_password(password)
                    save_users(users)
                    status_message, auth_success = "<p style='color:green;'>Sign-up successful! Welcome.</p>", True
            else:  # Login
                if username in users and users[username] == hash_password(password):
                    status_message, auth_success = "<p style='color:green;'>Login successful! Welcome.</p>", True
                else:
                    status_message = "<p style='color:red;'>Invalid username or password.</p>"
            if auth_success:
                return True, gr.update(visible=False), gr.update(visible=True), status_message
            else:
                return False, gr.update(visible=True), gr.update(visible=False), status_message

        def handle_login(state, u, p):
            return run_in_thread(attempt_auth, state, u, p, False)

        def handle_signup(state, u, p):
            return run_in_thread(attempt_auth, state, u, p, True)

        login_btn.click(handle_login, [is_authenticated, login_user, login_pass], [is_authenticated, auth_view, main_app_view, login_status])
        signup_btn.click(handle_signup, [is_authenticated, signup_user, signup_pass], [is_authenticated, auth_view, main_app_view, signup_status])

    return demo

# --- 4. Main Launch Logic ---
def main():
    parser = argparse.ArgumentParser(description="Gradio WebUI for Browser Agent")
    parser.add_argument("--ip", type=str, default="0.0.0.0", help="IP address to bind to.")
    parser.add_argument("--port", type=int, default=7788, help="Port to listen on.")
    parser.add_argument("--theme", type=str, default="Ocean", choices=theme_map.keys(), help="Theme to use for the UI.")
    args = parser.parse_args()

    demo = create_ui(theme_name=args.theme)
    
    # Enable async queue (parallel requests handled automatically via ThreadPoolExecutor)
    demo.queue(max_size=20).launch(
        server_name=args.ip,
        server_port=args.port
    )

if __name__ == '__main__':
    main()
