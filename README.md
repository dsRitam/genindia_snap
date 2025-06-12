# GenIndia Snap App 🎵

**GenIndia Snap** is a web application designed to generate Indian-inspired music from text prompts and provide detailed analytics on the generated tracks. This app allows users to create music clips (10-60 seconds) and analyze their quality using metrics like Harmonic-to-Noise Ratio (HNR), Prompt Sentiment Alignment, and CPU Usage, categorized by prompt types (`VAGUE`, `DESCRIPTIVE`, `LENGTHY`, `CONCISE`, `LESS INSTRUMENTS`, `MORE INSTRUMENTS`).

The app leverages **MusicGen** by Meta AudioCraft for music generation and uses libraries like `librosa` and `TextBlob` for audio and text analysis. It’s optimized to run on CPU-only systems, ensuring accessibility for users without GPUs.

## Features

- **Music Generation**:

  - Generate Indian-inspired music based on text prompts (e.g., "A soulful Qawwali piece with harmonium and tabla").
  - Select prompt types to control the style of input (`VAGUE`, `DESCRIPTIVE`, `LENGTHY`, `CONCISE`, `LESS INSTRUMENTS`, `MORE INSTRUMENTS`).
  - Customize track duration (10-60 seconds).
  - Download generated audio files.

- **Analytics**:

  - View and manage a library of generated tracks (play, download, delete).
  - Analyze metrics such as:
    - **Time Taken vs Duration**: Scatter plot to assess generation speed.
    - **CPU Usage Distribution**: Histogram of CPU usage across generations.
    - **CPU Usage by Prompt Type**: Bar chart to compare resource usage across prompt types.
    - **Prompt Sentiment Alignment and HNR by Prompt Type**: Bar chart showing the proportion of alignment and HNR for each prompt type.
    - **HNR vs Prompt Sentiment Alignment**: Scatter plot with legends for prompt types.
    - **HNR Distribution**: Histogram of HNR values to assess melodic clarity.

- **Indian Music Focus**:

  - Supports diverse Indian music styles, including Qawwali, Carnatic classical, Bollywood retro, tribal folk from Nagaland, and Indo-Western fusion.

## Prerequisites

Before running the app, ensure you have the following installed:

- **Python 3.8+**
- **pip** (Python package manager)
- A compatible operating system (Windows, macOS, Linux)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/genindia_snap.git
   cd genindia_snap
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**: Install the required Python packages using the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `app.py`: Main Streamlit app file with the homepage and navigation instructions.
- `pages/Generate_Music.py`: Page for generating music from text prompts, calculating metrics, and saving tracks to the database.
- `pages/Analytics.py`: Page for managing the music library and visualizing metrics.
- `audio_files/`: Directory where generated audio files are stored (created automatically).
- `music_data.db`: SQLite database to store music records (created automatically).

## Usage

1. **Run the App**: Start the Streamlit app by running the following command:

   ```bash
   streamlit run app.py
   ```

2. **Generate Music**:

   - Navigate to the "Generate Music" page using the sidebar.
   - Select a prompt type from the dropdown (`VAGUE`, `DESCRIPTIVE`, `LENGTHY`, `CONCISE`, `LESS INSTRUMENTS`, `MORE INSTRUMENTS`).
   - Enter a prompt (e.g., "A soulful Qawwali piece with harmonium and tabla, medium tempo").
   - Choose a duration (10-60 seconds) using the slider.
   - Click "Generate Music" to create the track.
   - View metrics like Time Taken, CPU Usage, Prompt Sentiment Alignment, and Harmonic-to-Noise Ratio (HNR).
   - Download the generated audio file.

3. **Analyze Metrics**:

   - Go to the "Analytics" page.
   - View your music library with options to play, download, or delete tracks.
   - Click "Analyze Metrics" to see visualizations:
     - **Time Taken vs Duration**: Scatter plot.
     - **CPU Usage Distribution**: Histogram.
     - **CPU Usage by Prompt Type**: Bar chart.
     - **Prompt Sentiment Alignment and HNR by Prompt Type**: Stacked bar chart.
     - **HNR vs Prompt Sentiment Alignment**: Scatter plot with legends.
     - **HNR Distribution**: Histogram.

## Example Prompts

Here are some example prompts for generating diverse Indian music styles, categorized by prompt type:

| **Prompt Type** | **Prompt** |
| --- | --- |
| VAGUE | "An Indian fusion track, fast tempo" |
| DESCRIPTIVE | "A soulful Qawwali piece with harmonium and tabla, medium tempo, evoking the devotion of a Sufi shrine in Delhi during a moonlit evening with the faint sound of clapping devotees" |
| LENGTHY | "A vibrant Carnatic classical composition in Raga Hamsadhwani with violin, mridangam, and ghatam, fast-paced, capturing the festive energy of a South Indian temple festival during Navratri with the sound of temple bells ringing, the chatter of devotees, the rhythmic chants of a priest, and the aroma of jasmine flowers in the air" |
| CONCISE | "A retro Bollywood melody with sitar and dholak, medium tempo" |
| LESS INSTRUMENTS | "A haunting tribal folk tune from Nagaland with a bamboo flute, slow tempo, reflecting the stillness of a misty forest at dawn" |
| MORE INSTRUMENTS | "An upbeat Indo-Western fusion track with tabla, sitar, electric guitar, and synthesizer, fast-paced, capturing the energy of a Mumbai nightlife scene" |

## Metrics Explained

- **Time Taken**: Duration (in seconds) to generate the music track.
- **CPU Usage**: Average CPU usage (%) during generation, measured using `psutil`.
- **Prompt Sentiment Alignment**: Measures how well the generated music’s tempo aligns with the prompt’s sentiment (positive prompts expect faster tempo, negative ones expect slower).
- **Harmonic-to-Noise Ratio (HNR)**: Assesses melodic clarity (0 to 1), with higher values indicating clearer, more harmonic music.

## Visualizations

- **Time Taken vs Duration**: Scatter plot to analyze generation speed.
- **CPU Usage Distribution**: Histogram to see the spread of CPU usage.
- **CPU Usage by Prompt Type**: Bar chart to compare resource usage across prompt types.
- **Prompt Sentiment Alignment and HNR by Prompt Type**: Bar chart showing the proportion of alignment and HNR for each prompt type.
- **HNR vs Prompt Sentiment Alignment**: Scatter plot with legends for prompt types to see their correlation.
- **HNR Distribution**: Histogram to assess overall melodic clarity of generated tracks.

## Notes

- The app is optimized for CPU-only systems, using `torch` and `torchaudio` with CPU support.
- Generated audio files are stored in the `audio_files/` directory, and records are saved in `music_data.db`.

## Limitations

- Music generation quality depends on the `facebook/musicgen-small` model, which may struggle with very complex prompts.
- The app is CPU-only, so generation might be slower compared to GPU setups.

---

*Built for music lovers and creators.*