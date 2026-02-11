import streamlit as st
import time

def scroll_to_top():
    """
    Injects a script to scroll the page to the top.
    Forces scroll by targeting multiple containers and using a unique key to ensure execution.
    """
    # Use a unique timestamp to force re-execution if needed, though usually rerun handles it.
    ts = int(time.time() * 1000)
    
    js_code = f"""
    <script>
        var body = window.parent.document.body;
        var main = window.parent.document.querySelector('.main');
        var stMain = window.parent.document.querySelector('section[data-testid="stMain"]');
        
        if (main) {{ main.scrollTop = 0; }}
        if (stMain) {{ stMain.scrollTop = 0; }}
        if (body) {{ body.scrollTop = 0; }}
        window.parent.scrollTo(0, 0);
        
        // Console log for debugging
        console.log("Scrolled to top at {ts}");
    </script>
    """
    
    try:
        if hasattr(st, "html"):
            st.html(js_code)
        else:
            import streamlit.components.v1 as components
            components.html(js_code, height=0, width=0)
    except Exception:
        pass
