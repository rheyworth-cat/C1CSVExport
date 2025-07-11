import streamlit as st
import streamlit.components.v1 as components
import webbrowser
import urllib.parse

def split_player_ids(url, chunk_size=100):
    """
    Extract playerIDs from the original URL and split them into chunks of specified size
    """
    try:
        # Extract playerIDs from the original URL
        player_ids = url.split("playerIDs=")[1].split("&")[0].split("%2C")
        
        # Split the playerIDs into chunks of specified size
        chunks = []
        for i in range(0, len(player_ids), chunk_size):
            chunk = player_ids[i:i + chunk_size]
            chunks.append(chunk)
        
        # Generate the new URLs for each chunk
        urls = []
        for chunk in chunks:
            new_url = url.replace("playerIDs=" + "%2C".join(player_ids), "playerIDs=" + "%2C".join(chunk))
            urls.append(new_url)
        
        return urls, len(player_ids)
    except Exception as e:
        st.error(f"Error processing URL: {str(e)}")
        return None, None

def main():
    st.set_page_config(
        page_title="Catapult CSV Exporter",
        page_icon="⚡",
        layout="wide"
    )
    
    # Custom CSS to match Catapult styling
    st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    .main-header {
        color: #1a1a1a;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .sub-header {
        color: #6c757d;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .export-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin: 1rem 0;
    }
    .export-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    .url-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .url-link {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 500;
        display: inline-block;
        margin-top: 0.5rem;
        transition: all 0.3s ease;
    }
    .url-link:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        text-decoration: none;
        color: white;
    }
    .success-message {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">⚡ Catapult CSV Exporter</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Export large datasets by automatically splitting URLs into manageable chunks</p>', unsafe_allow_html=True)
    
    # URL input
    st.subheader("🔗 Enter Your Export URL")
    url_input = st.text_area(
        "Paste your Catapult export URL here:",
        height=100,
        placeholder="Enter a URL containing playerIDs parameter..."
    )
    
    # Advanced settings in collapsed section
    with st.expander("⚙️ Advanced Settings"):
        chunk_size = st.number_input(
            "Athletes per CSV file:",
            min_value=1,
            max_value=2000,
            value=500,
            help="Number of athletes to include in each CSV export"
        )
    
    # Single Export button that does everything
    if st.button("🚀 Export CSVs", type="primary", help="Split URL and download all CSV files"):
        if url_input.strip():
            # Check if URL contains playerIDs parameter
            if "playerIDs=" not in url_input:
                st.error("❌ URL must contain 'playerIDs=' parameter")
                return
                
            # Split the URL
            urls, total_athletes = split_player_ids(url_input.strip(), chunk_size)
            
            if urls and total_athletes:
                # Show success message
                st.markdown(f'<div class="success-message">✅ Found {total_athletes} athletes! Creating {len(urls)} CSV exports...</div>', unsafe_allow_html=True)
                
                # Create HTML that opens all URLs automatically
                auto_download_html = f"""
                <div style="text-align: center; margin: 2rem 0;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                        <h3 style="margin: 0;">🚀 Auto-Downloading {len(urls)} CSV Files</h3>
                        <p style="margin: 0.5rem 0 0 0;">Your CSV files are opening automatically. Allow pop-ups if prompted.</p>
                    </div>
                </div>
                <script>
                function autoDownloadCSVs() {{
                    const urls = {str(urls).replace("'", '"')};
                    let openedCount = 0;
                    
                    urls.forEach((url, index) => {{
                        setTimeout(() => {{
                            window.open(url, '_blank');
                            openedCount++;
                            if (openedCount === urls.length) {{
                                console.log('All CSV exports opened successfully!');
                            }}
                        }}, index * 800);
                    }});
                }}
                
                // Auto-trigger the download
                setTimeout(autoDownloadCSVs, 1000);
                </script>
                """
                
                st.components.v1.html(auto_download_html, height=150)
                
                # Show summary
                st.markdown(f'<div class="info-card">📊 <strong>Export Summary:</strong> {total_athletes} athletes split into {len(urls)} CSV files with up to {chunk_size} athletes each</div>', unsafe_allow_html=True)
        if url_input.strip():
            # Check if URL contains playerIDs parameter
            if "playerIDs=" not in url_input:
                st.error("❌ URL must contain 'playerIDs=' parameter")
                return
                
            # Split the URL
            urls, total_athletes = split_player_ids(url_input.strip(), chunk_size)
            
            if urls and total_athletes:
                st.success(f"✅ URL successfully split! Found {total_athletes} athletes, created {len(urls)} URLs")
                
                # Show summary
                st.info(f"📊 **Summary:** {total_athletes} athletes split into {len(urls)} chunks of up to {chunk_size} athletes each")
                
                # Download All section
                st.subheader("🚀 Quick Actions")
                
                # Create a grid of "Download All" links
                st.markdown("**📥 Download All CSVs** (Click each link to open):")
                
                # Create columns for the download all links
                cols = st.columns(min(len(urls), 4))
                for i, url in enumerate(urls):
                    with cols[i % 4]:
                        athletes_in_chunk = min(chunk_size, total_athletes - (i * chunk_size))
                        st.markdown(f'<a href="{url}" target="_blank" style="display: inline-block; padding: 8px 12px; background-color: #ff4b4b; color: white; text-decoration: none; border-radius: 4px; font-size: 14px; margin: 2px; text-align: center; width: 100%;">📥 CSV {i+1}<br>({athletes_in_chunk} athletes)</a>', unsafe_allow_html=True)
                
                st.markdown("**💡 Tip:** Click each red button above to download the CSV files. They will open in new tabs.")
                
                # Display results in a more organized way
                st.subheader("Individual URLs")
                
                # Create tabs for each URL if there are many
                if len(urls) <= 5:
                    # Show all URLs in columns if 5 or fewer
                    cols = st.columns(min(len(urls), 3))
                    for i, url in enumerate(urls):
                        with cols[i % 3]:
                            athletes_in_chunk = min(chunk_size, total_athletes - (i * chunk_size))
                            st.markdown(f"**URL {i+1}** ({athletes_in_chunk} athletes)")
                            st.code(url, language=None)
                            
                            # Use HTML link instead of button to prevent page reload
                            st.markdown(f'<a href="{url}" target="_blank" style="display: inline-block; padding: 0.25rem 0.75rem; background-color: #0066cc; color: white; text-decoration: none; border-radius: 0.25rem; font-size: 0.875rem;">🔗 Open URL {i+1}</a>', unsafe_allow_html=True)
                            st.markdown("")  # Add spacing
                else:
                    # Show URLs in expandable sections if more than 5
                    for i, url in enumerate(urls):
                        athletes_in_chunk = min(chunk_size, total_athletes - (i * chunk_size))
                        with st.expander(f"URL {i+1} ({athletes_in_chunk} athletes)"):
                            st.code(url, language=None)
                            
                            # Use HTML link instead of button to prevent page reload
                            st.markdown(f'<a href="{url}" target="_blank" style="display: inline-block; padding: 0.25rem 0.75rem; background-color: #0066cc; color: white; text-decoration: none; border-radius: 0.25rem; font-size: 0.875rem;">🔗 Open URL {i+1}</a>', unsafe_allow_html=True)
                
                # Instructions
                st.markdown("---")
                st.subheader("📋 Instructions")
                st.markdown(f"""
                1. Click on each **"Open URL X"** button to open the URLs in new tabs
                2. Export the CSV file from each page
                3. You will have {len(urls)} CSV files with up to {chunk_size} athletes each
                4. Combine the CSV files if needed for your analysis
                """)
                
                # Additional info
                st.info("💡 **Tip:** The URLs will open in new browser tabs. Make sure your browser allows pop-ups for this site.")
        else:
            st.warning("⚠️ Please enter a URL")
    
    # Example section
    st.markdown("---")
    st.subheader("📖 Example Usage")
    st.markdown("**Original Catapult export URL with 1,200 athletes:**")
    st.code("https://one.catapultsports.com/export?playerIDs=player1%2Cplayer2%2C...%2Cplayer1200&other=params")
    
    st.markdown("**Will be automatically split into 3 CSV files:**")
    st.code("CSV 1: Athletes 1-500")
    st.code("CSV 2: Athletes 501-1000") 
    st.code("CSV 3: Athletes 1001-1200")

if __name__ == "__main__":
    main()