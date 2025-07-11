import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import webbrowser
import urllib.parse

# Page configuration with logo in title area
st.set_page_config(
    page_title="Catapult CSV Exporter",
    page_icon="⚡",
    layout="wide"
)

# Load Catapult logo and display in sidebar
def load_logo():
    try:
        logo = Image.open('assets/catapult_logo.png')  # ensure this file exists
        st.sidebar.image(logo, use_column_width=True)
    except Exception:
        st.sidebar.markdown("<h3>Catapult CSV Exporter</h3>", unsafe_allow_html=True)

# Inject custom CSS to match Catapult styling
def load_css():
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
      body, .streamlit-container {
        font-family: 'Roboto', sans-serif;
      }
      .stApp {
        background-color: #F2F4F8;
      }
      .main-header {
        color: #005EB8;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
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
      button.stButton>button:hover {
        transform: translateY(-2px);
      }
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
      a.download-link:hover {
        opacity: 0.85;
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
    load_logo()
    load_css()

    st.markdown('<h1 class="main-header">⚡ Catapult CSV Exporter</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Export large datasets by automatically splitting URLs into manageable chunks</p>', unsafe_allow_html=True)

    url_input = st.text_area(
        "🔗 Paste your Catapult export URL here:",
        height=100,
        placeholder="Enter a URL containing playerIDs= parameter..."
    )

    with st.expander("⚙️ Advanced Settings"):
        chunk_size = st.number_input(
            "Athletes per CSV file:",
            min_value=1,
            max_value=2000,
            value=500,
            help="Number of athletes to include in each CSV export"
        )

    if st.button("🚀 Export CSVs"):
        if not url_input or "playerIDs=" not in url_input:
            st.error("❌ URL must contain 'playerIDs=' parameter")
            return

        urls, total = split_player_ids(url_input.strip(), chunk_size)
        if urls:
            st.markdown(f'<div class="success-message">✅ Found {total} athletes and created {len(urls)} CSV exports!</div>', unsafe_allow_html=True)
            html = f"""
            <script>
            const urls = {urls};
            urls.forEach((u, i) => setTimeout(() => window.open(u, '_blank'), i*800));
            </script>
            """
            components.html(html, height=0)

            st.markdown(f'<div class="info-card">📊 Summary: {total} athletes → {len(urls)} CSVs (up to {chunk_size} each)</div>', unsafe_allow_html=True)

            st.subheader("📥 Download All CSVs")
            cols = st.columns(min(4, len(urls)))
            for i, u in enumerate(urls):
                with cols[i % 4]:
                    count = min(chunk_size, total - i*chunk_size)
                    st.markdown(f'<a class="download-link" href="{u}" target="_blank">📥 CSV {i+1}<br>({count} athletes)</a>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📖 Example Usage")
    st.code(
        "https://one.catapultsports.com/export?playerIDs=player1%2Cplayer2%2C...%2Cplayer1200&other=params"
    )
    st.markdown("**Will be split into:**")
    st.write("- CSV 1: Athletes 1–500")
    st.write("- CSV 2: Athletes 501–1000")
    st.write("- CSV 3: Athletes 1001–1200")

if __name__ == "__main__":
    main()
