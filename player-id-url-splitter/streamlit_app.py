import streamlit as st
import webbrowser
import urllib.parse

def split_player_ids(url):
    """
    Extract playerIDs from the original URL and split them into two equal parts
    """
    try:
        # Extract playerIDs from the original URL
        player_ids = url.split("playerIDs=")[1].split("&")[0].split("%2C")
        
        # Calculate the midpoint to split the playerIDs into two equal parts
        midpoint = len(player_ids) // 2
        
        # Split the playerIDs into two equal parts
        player_ids_a = player_ids[:midpoint]
        player_ids_b = player_ids[midpoint:]
        
        # Generate the new URLs
        url_a = url.replace("playerIDs=" + "%2C".join(player_ids), "playerIDs=" + "%2C".join(player_ids_a))
        url_b = url.replace("playerIDs=" + "%2C".join(player_ids), "playerIDs=" + "%2C".join(player_ids_b))
        
        return url_a, url_b
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
    st.markdown("This app splits a URL with multiple player IDs into two separate URLs for easier CSV export.")
    
    # URL input
    st.subheader("Enter Your URL")
    url_input = st.text_area(
        "Paste your URL here:",
        height=100,
        placeholder="Enter a URL containing playerIDs parameter..."
    )
    
    if st.button("Split URL", type="primary"):
        if url_input.strip():
            # Check if URL contains playerIDs parameter
            if "playerIDs=" not in url_input:
                st.error("❌ URL must contain 'playerIDs=' parameter")
                return
                
            # Split the URL
            url_a, url_b = split_player_ids(url_input.strip())
            
            if url_a and url_b:
                st.success("✅ URL successfully split!")
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("URL A (First Half)")
                    st.code(url_a, language=None)
                    
                    # Button to open URL A
                    if st.button("🔗 Open URL A", key="url_a"):
                        st.markdown(f'<a href="{url_a}" target="_blank">Click here if the link doesn\'t open automatically</a>', unsafe_allow_html=True)
                        st.balloons()
                
                with col2:
                    st.subheader("URL B (Second Half)")
                    st.code(url_b, language=None)
                    
                    # Button to open URL B
                    if st.button("🔗 Open URL B", key="url_b"):
                        st.markdown(f'<a href="{url_b}" target="_blank">Click here if the link doesn\'t open automatically</a>', unsafe_allow_html=True)
                        st.balloons()
                
                # Instructions
                st.markdown("---")
                st.subheader("📋 Instructions")
                st.markdown("""
                1. Click on the **"Open URL A"** button to open the first URL in a new tab
                2. Export the CSV file from that page
                3. Click on the **"Open URL B"** button to open the second URL in a new tab
                4. Export the CSV file from that page
                5. You now have two CSV files with split player data!
                """)
                
                # Additional info
                st.info("💡 **Tip:** The URLs will open in new browser tabs. Make sure your browser allows pop-ups for this site.")
        else:
            st.warning("⚠️ Please enter a URL")
    
    # Example section
    st.markdown("---")
    st.subheader("📖 Example")
    st.markdown("**Original URL format should look like:**")
    st.code("https://example.com/data?playerIDs=player1%2Cplayer2%2Cplayer3%2Cplayer4&other=params")
    
    st.markdown("**Will be split into:**")
    st.code("URL A: https://example.com/data?playerIDs=player1%2Cplayer2&other=params")
    st.code("URL B: https://example.com/data?playerIDs=player3%2Cplayer4&other=params")

if __name__ == "__main__":
    main()