import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import webbrowser
import urllib.parse

# Page configuration with custom logo icon
st.set_page_config(
    page_title="Catapult CSV Exporter",
    page_icon='assets/catapult_logo.png',
    layout="wide"
)

# Inject custom CSS for Catapult styling and dark mode support
def load_css():
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
      body, .streamlit-container { font-family: 'Roboto', sans-serif; }
      .stApp { background-color: #F2F4F8; }
      .main-header-text {
        color: #005EB8;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 0.5rem 0;
      }
      .sub-header {
        color: #6C757D;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
      }
      button.stButton>button {
        background-color: #00AEEF;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: transform 0.2s ease;
        width: 100%;
      }
      button.stButton>button:hover { transform: translateY(-2px); }
      .success-message {
        background: linear-gradient(135deg, #56AB2F 0%, #A8E6CF 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
      }
      .info-card {
        background: linear-gradient(135deg, #005EB8 0%, #00AEEF 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
      }
      a.download-link {
        display: inline-block;
        padding: 0.5rem 1rem;
        background-color: #FF4B4B;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        margin: 2px;
        font-size: 0.9rem;
      }
      a.download-link:hover { opacity: 0.85; }
      @media (prefers-color-scheme: dark) {
        .stApp { background-color: #0E1117 !important; }
        .main-header-text, .sub-header { color: #FFFFFF !important; }
        .success-message, .info-card { filter: brightness(1.2); }
        button.stButton>button { background-color: #005EB8 !important; }
        a.download-link { background-color: #FF4B4B !important; }
      }
    </style>
    """, unsafe_allow_html=True)

# Helper: split player IDs into chunks
def split_player_ids(url, chunk_size=100):
    try:
        player_ids = url.split("playerIDs=")[1].split("&")[0].split("%2C")
        chunks = [player_ids[i:i+chunk_size] for i in range(0, len(player_ids), chunk_size)]
        urls = []
        for chunk in chunks:
            urls.append(url.replace(
                "playerIDs=" + "%2C".join(player_ids),
                "playerIDs=" + "%2C".join(chunk)
            ))
        return urls, len(player_ids)
    except Exception as e:
        st.error(f"Error processing URL: {e}")
        return None, None

# Main application
def main():
    load_css()

    # Logo above the header
    try:
        logo = Image.open('assets/catapult_logo.png')
        st.image(logo, width=80, use_container_width=False)
    except Exception:
        pass

    # Header text
    st.markdown('<div class="main-header-text">Catapult CSV Exporter</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Export large datasets by automatically splitting URLs into manageable chunks</div>', unsafe_allow_html=True)

    # URL input
    url_input = st.text_area(
        "🔗 Paste your Catapult export URL here:",
        height=100,
        placeholder="Enter a URL containing playerIDs= parameter..."
    )

    # Advanced settings
    with st.expander("⚙️ Advanced Settings"):
        chunk_size = st.number_input(
            "Athletes per CSV file:",
            min_value=1,
            max_value=2000,
            value=500,
            help="Number of athletes to include in each CSV export"
        )

    # Export logic
    if st.button("🚀 Export CSVs"):
        if not url_input or "playerIDs=" not in url_input:
            st.error("❌ URL must contain 'playerIDs=' parameter")
            return

        urls, total = split_player_ids(url_input.strip(), chunk_size)
        if urls:
            st.markdown(f'<div class="success-message">✅ Found {total} athletes and created {len(urls)} CSV exports!</div>', unsafe_allow_html=True)
            components.html(f"""
            <script>
            const urls = {urls};
            urls.forEach((u, i) => setTimeout(() => window.open(u, '_blank'), i * 800));
            </script>
            """, height=0)
            st.markdown(f'<div class="info-card">📊 Summary: {total} athletes → {len(urls)} CSVs (up to {chunk_size} each)</div>', unsafe_allow_html=True)
            st.subheader("📥 Download All CSVs")
            cols_dl = st.columns(min(4, len(urls)))
            for i, u in enumerate(urls):
                with cols_dl[i % 4]:
                    count = min(chunk_size, total - i * chunk_size)
                    st.markdown(f'<a class="download-link" href="{u}" target="_blank">📥 CSV {i+1}<br>({count} athletes)</a>', unsafe_allow_html=True)

    # User guide
    st.markdown("---")
    st.subheader("📘 User Guide")
+    st.markdown("**Step 1: Export as Normal:** In your PlayerTek dashboard, click **Export to CSV**. If the download succeeds, you’re done. If nothing happens, proceed to Developer Tools.")
+    st.markdown("**Step 2: Open Developer Tools:** Press **Ctrl+Shift+I** (Windows/Linux) or **Cmd+Option+I** (Mac) in Chrome. For other browsers like Firefox or Edge, use the equivalent DevTools shortcut.")
+    st.markdown("[Learn more about Chrome DevTools](https://developer.chrome.com/docs/devtools/)")
+    st.markdown("**Step 3: Access the Console:** Click the **Console** tab in DevTools and look for errors referencing `ExportService`.")
+    st.markdown("**Step 4: Identify & Copy URL:** Find the error line containing the URL with `/webinterface/ExportService`. Right-click the link and select **Copy link address**.")
+    st.markdown("**Step 5: Paste & Export:** Paste the copied URL into the field above and click **🚀 Export CSVs** to split and download your CSV files.")

if __name__ == "__main__":
    main()
