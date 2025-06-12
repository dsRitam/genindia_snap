import streamlit as st

st.set_page_config(
    page_title="GenIndia Snap",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page content
st.title("🎵 Welcome to GenIndia Snap App")
st.markdown("""
### A Creative Music Generation and Analysis Tool

**GenIndia Snap App** is a powerful tool built to help you generate music from text prompts and analyze the results with detailed metrics. Whether you're a music enthusiast, a creator, or someone exploring AI-generated music, this app offers a seamless experience to:
- Generate music based on descriptive prompts (e.g., "classical Indian sitar").
- Analyze the generated music with metrics like tool performance, Indian-context compatibility, and prompt impact.
- Manage your music library with options to play, download, or delete tracks.

This app leverages **MusicGen** by Meta AudioCraft to create music. All processing is optimized to run on CPU-only systems, ensuring accessibility.

---

### How to Use This App
1. **Navigate Using the Sidebar**:
   - **Generate Music**: Create new music tracks by providing a text prompt and selecting a duration.
   - **Analytics**: View your music library, play tracks, delete records, and analyze performance metrics.

2. **Generate Music**:
   - Go to the "Generate Music" page.
   - Enter a prompt (e.g., "upbeat pop indian music") and choose a duration (10-60 seconds).
   - Click "Generate Music" to create and save your track.

3. **Analyze Results**:
   - Switch to the "Analytics" page to see all generated tracks.
   - Play or download tracks, delete unwanted records, and click "Analyze Metrics" to view insights like:
     - Tool performance (time taken, CPU usage).
     - Prompt impact (sentiment alignment).
     - Sound quality (Harmonic To Noise Ratio).

---


*Built with ❤️. Start creating now!*
            
""")

