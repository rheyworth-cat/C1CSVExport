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
        page_title="Player ID URL Splitter",
        page_icon="⚾",
        layout="wide"
    )
    
    st.title("⚾ Player ID URL Splitter")
    st.markdown("This app splits a URL with multiple player IDs into chunks of 500 athletes each for easier CSV export.")
    
    # URL input
    st.subheader("Enter Your URL")
    url_input = st.text_area(
        "Paste your URL here:",
        height=100,
        placeholder="Enter a URL containing playerIDs parameter..."
    )
    
    # Advanced settings in collapsed section
    with st.expander("⚙️ Advanced Settings"):
        chunk_size = st.number_input(
            "Athletes per URL:",
            min_value=1,
            max_value=2000,
            value=500,
            help="Number of athletes to include in each URL chunk"
        )
    
    if st.button("Split URL", type="primary"):
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
    st.subheader("📖 Example")
    st.markdown("**Original URL with 500 athletes:**")
    st.code("https://example.com/data?playerIDs=player1%2Cplayer2%2C...%2Cplayer500&other=params")
    
    st.markdown("**Will be split into 1 URL (500 athletes each):**")
    st.code("URL 1: https://example.com/data?playerIDs=player1%2C...%2Cplayer500&other=params")

if __name__ == "__main__":
    main()