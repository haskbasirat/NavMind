# src/webui/interface.py (FINAL VERSION - Per-User Sessions, KeyError Fix, Full UI)

import gradio as gr
from gradio.components import Component
from typing import Dict, Any, AsyncGenerator
import os

from src.webui.webui_manager import WebuiManager
from src.webui.components.agent_settings_tab import create_agent_settings_tab
from src.webui.components.browser_settings_tab import create_browser_settings_tab
from src.webui.components.browser_use_agent_tab import (
    create_browser_use_agent_tab,
    handle_submit,
    handle_stop,
    handle_pause_resume,
    handle_clear,
)
from src.webui.components.deep_research_agent_tab import create_deep_research_agent_tab
from src.webui.components.load_save_config_tab import create_load_save_config_tab

theme_map = {"Base": gr.themes.Base()}


def _connect_event_handlers(layout_manager: WebuiManager, session_state: gr.State):
    """
    Connects all event handlers.
    - layout_manager: Holds references to the UI components.
    - session_state: Holds the unique data manager for each user.
    """
    run_button = layout_manager.get_component_by_id("browser_use_agent.run_button")
    stop_button = layout_manager.get_component_by_id("browser_use_agent.stop_button")
    pause_resume_button = layout_manager.get_component_by_id("browser_use_agent.pause_resume_button")
    clear_button = layout_manager.get_component_by_id("browser_use_agent.clear_button")
    user_input = layout_manager.get_component_by_id("browser_use_agent.user_input")

    all_components = layout_manager.get_components()
    run_tab_outputs = [c for c in all_components if layout_manager.get_id_by_component(c).startswith("browser_use_agent.")]
    valid_outputs = [c for c in run_tab_outputs if not isinstance(c, (gr.Column, gr.Row, gr.Group, gr.Accordion, gr.Tab))]

    # --- WRAPPER FUNCTIONS ---
    # These wrappers receive the session data and ensure it's ready for the real handlers.
    async def submit_wrapper(session_data, *args):
        # KEY FIX: Ensure the session's data manager has the UI component references.
        session_data.id_to_component = layout_manager.id_to_component
        session_data.component_to_id = layout_manager.component_to_id
        
        components_dict = {comp: val for comp, val in zip(all_components, args)}
        async for update in handle_submit(session_data, components_dict):
            yield update

    async def stop_wrapper(session_data):
        session_data.id_to_component = layout_manager.id_to_component
        session_data.component_to_id = layout_manager.component_to_id
        yield await handle_stop(session_data)
        
    async def pause_resume_wrapper(session_data):
        session_data.id_to_component = layout_manager.id_to_component
        session_data.component_to_id = layout_manager.component_to_id
        yield await handle_pause_resume(session_data)

    async def clear_wrapper(session_data):
        session_data.id_to_component = layout_manager.id_to_component
        session_data.component_to_id = layout_manager.component_to_id
        yield await handle_clear(session_data)

    # --- EVENT REGISTRATION ---
    # The session_state is passed as the first input to every handler.
    run_button.click(fn=submit_wrapper, inputs=[session_state] + all_components, outputs=valid_outputs)
    user_input.submit(fn=submit_wrapper, inputs=[session_state] + all_components, outputs=valid_outputs)
    stop_button.click(fn=stop_wrapper, inputs=[session_state], outputs=valid_outputs)
    pause_resume_button.click(fn=pause_resume_wrapper, inputs=[session_state], outputs=valid_outputs)
    clear_button.click(fn=clear_wrapper, inputs=[session_state], outputs=valid_outputs)


def create_ui(theme_name="Base"):
    """
    Builds the complete Gradio UI, including the session state management.
    """
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
    .settings-container { max-width: 95%; margin: 0 auto; }
    .settings-container .gradio-row { display: grid !important; grid-template-columns: repeat(2, 1fr) !important; gap: 1.5rem !important; align-items: start !important; }
    .settings-container .gradio-row > *:only-child { grid-column: 1 / -1 !important; }
    .settings-container .gradio-accordion { background: var(--bg-secondary) !important; border: 1px solid var(--border-primary) !important; border-radius: var(--radius-md) !important; margin-bottom: 1.5rem !important; }
    .settings-container .gradio-accordion summary { padding: 0.75rem 1rem !important; font-weight: 600 !important; color: var(--text-primary) !important; border-bottom: 1px solid var(--border-primary); }
    .settings-container .gradio-accordion[open] > summary { border-bottom: 1px solid var(--border-primary); }
    .settings-container .gradio-accordion > div { padding: 1.5rem !important; background: transparent !important; }
    ::-webkit-scrollbar { width: 8px !important; }
    ::-webkit-scrollbar-thumb { background: var(--bg-tertiary) !important; border-radius: 4px !important; }
    """

    # This manager is created once and holds the static UI component layout.
    layout_manager = WebuiManager()

    with gr.Blocks(title="NavMind", theme=gr.themes.Base(), css=css) as demo:
        # This state is the key. It creates a new, unique WebuiManager
        # for each user's data (chat history, agent instances, etc.).
        session_state = gr.State(lambda: WebuiManager())

        # --- Build the UI Layout ---
        # This structure is created once and is the same for all users.
        gr.HTML(
            """
            <div class="app-header">
                <div style="display:flex; align-items:center; gap:0.75rem;">
                     <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 17L12 22L22 17" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 12L12 17L22 12" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    <h1 class="app-title">NavMind</h1>
                </div>
            </div>
            """
        )

        with gr.Row(elem_classes="app-layout"):
            with gr.Column(elem_classes="app-sidebar", scale=0, min_width=280):
                chat_tab_btn = gr.Button("💬 Chat", elem_classes="sidebar-tab tab-active")
                agent_tab_btn = gr.Button("🤖 Agent Settings", elem_classes="sidebar-tab")
                browser_tab_btn = gr.Button("🌐 Browser Settings", elem_classes="sidebar-tab")
                research_tab_btn = gr.Button("🔍 Research Agent", elem_classes="sidebar-tab")
                config_tab_btn = gr.Button("💾 Configuration", elem_classes="sidebar-tab")

            with gr.Column(elem_classes="main-content", scale=1):
                with gr.Column(elem_classes="content-area"):
                    with gr.Group(visible=True) as chat_tab_content:
                        create_browser_use_agent_tab(layout_manager)
                    with gr.Group(visible=False, elem_classes="settings-container") as agent_tab_content:
                        create_agent_settings_tab(layout_manager)
                    with gr.Group(visible=False, elem_classes="settings-container") as browser_tab_content:
                        create_browser_settings_tab(layout_manager)
                    with gr.Group(visible=False, elem_classes="settings-container") as research_tab_content:
                        create_deep_research_agent_tab(layout_manager)
                    with gr.Group(visible=False, elem_classes="settings-container") as config_tab_content:
                        create_load_save_config_tab(layout_manager)

        # Connect tab switching logic (this is global and doesn't need session state)
        tab_contents = [chat_tab_content, agent_tab_content, browser_tab_content, research_tab_content, config_tab_content]
        tab_buttons = [chat_tab_btn, agent_tab_btn, browser_tab_btn, research_tab_btn, config_tab_btn]
        all_tab_outputs = tab_contents + tab_buttons
        def create_tab_handler(tab_index):
            def handler():
                content_updates = [gr.update(visible=(i == tab_index)) for i in range(len(tab_contents))]
                button_updates = [gr.update(elem_classes="sidebar-tab tab-active" if i == tab_index else "sidebar-tab") for i in range(len(tab_buttons))]
                return content_updates + button_updates
            return handler
        for i, button in enumerate(tab_buttons):
            button.click(fn=create_tab_handler(i), inputs=None, outputs=all_tab_outputs, show_progress="hidden")
        
        # --- VNC Loader ---
        def update_vnc_on_load(request: gr.Request):
            host_header = request.headers.get("host")
            server_ip = host_header.split(":")[0] if host_header else "127.0.0.1"
            vnc_password = os.getenv("VNC_PASSWORD", "youvncpassword")
            vnc_port = os.getenv("VNC_PORT", "6080")
            vnc_url = f"http://{server_ip}:{vnc_port}/vnc.html?password={vnc_password}&autoconnect=true&resize=scale"
            iframe_html = f'<iframe src="{vnc_url}" style="width: 100%; height: 800px; border: 1px solid var(--border-primary); border-radius: var(--radius-md);"></iframe>'
            return gr.update(value=iframe_html)
        
        vnc_view_component = layout_manager.get_component_by_id("browser_use_agent.vnc_view")
        demo.load(fn=update_vnc_on_load, inputs=None, outputs=[vnc_view_component])
        
        # --- Connect all the interactive event handlers ---
        _connect_event_handlers(layout_manager, session_state)

    return demo