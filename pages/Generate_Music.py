import streamlit as st
import os
import torch
import torchaudio
import numpy as np
import base64
import sqlite3
import time
import psutil
from audiocraft.models import MusicGen
import librosa
from textblob import TextBlob
from datetime import datetime

AUDIO_DIR = os.path.join(".", "audio_files")
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

DB_PATH = os.path.join(".", "music_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS music_records
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  prompt TEXT,
                  prompt_type TEXT,
                  duration INTEGER,
                  time_taken REAL,
                  cpu_usage REAL,
                  raga_similarity REAL,
                  prompt_alignment REAL,
                  harmonic_to_noise_ratio REAL,
                  audio_path TEXT,
                  created_at TEXT)''')
    conn.commit()
    conn.close()

def compute_raga_similarity(audio_path):
    # y, sr = librosa.load(audio_path)
    # pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    # pitch_profile = np.mean(pitches[pitches > 0])
    # yaman_range = 261.63  # Middle C (Sa) for Raga Yaman
    # if pitch_profile > 0:
    #     similarity = 1 - abs(pitch_profile - yaman_range) / yaman_range
    #     similarity = max(0, min(1, similarity))
    #     if isinstance(similarity, np.ndarray):
    #         similarity = similarity.item()
    #     return float(similarity)
    return 0.0

def compute_prompt_alignment(prompt, audio_path):
    blob = TextBlob(prompt)
    sentiment = blob.sentiment.polarity
    y, sr = librosa.load(audio_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    if isinstance(tempo, np.ndarray):
        tempo = tempo.item()
    expected_tempo = 120 if sentiment > 0 else 80
    alignment = 1 - abs(tempo - expected_tempo) / expected_tempo
    alignment = max(0, min(1, alignment))
    if isinstance(alignment, np.ndarray):
        alignment = alignment.item()
    return float(alignment)

def compute_harmonic_to_noise_ratio(audio_path):
    y, sr = librosa.load(audio_path)
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    harmonic_energy = np.mean(y_harmonic**2)
    noise_energy = np.mean(y_percussive**2)
    if noise_energy == 0:
        return 1.0
    hnr = harmonic_energy / (harmonic_energy + noise_energy)
    return float(max(0, min(1, hnr)))

@st.cache_resource
def load_model():
    model = MusicGen.get_pretrained("facebook/musicgen-small")
    return model

init_db()
st.title("Text2Music Generation")

prompt_type = st.selectbox(
    "Select Prompt Type",
    ["VAGUE", "DESCRIPTIVE", "LENGTHY", "CONCISE", "LESS INSTRUMENTS", "MORE INSTRUMENTS"]
)
prompt = st.text_area("Write a music description (e.g., 'upbeat pop music')")
duration = st.slider("Duration in seconds", min_value=10, max_value=60, value=30)

if st.button("Generate Music"):
    if prompt and duration:
        st.subheader("Your Music")
        with st.spinner("Generating music..."):
            model = load_model()
            model.set_generation_params(duration=duration)

            start_time = time.time()
            cpu_usages = []
            for _ in range(10):
                cpu_usages.append(psutil.cpu_percent(interval=0.1))
            wav = model.generate([prompt], progress=True)
            wav = wav.squeeze(0).cpu()
            end_time = time.time()

            time_taken = end_time - start_time
            avg_cpu_usage = sum(cpu_usages) / len(cpu_usages)

            audio_id = int(time.time())
            output_path = os.path.join(AUDIO_DIR, f"audio_{audio_id}.wav")
            torchaudio.save(output_path, wav, sample_rate=32000)

            raga_similarity = compute_raga_similarity(output_path)
            print(f'DEBUG: {raga_similarity}')
            prompt_alignment = compute_prompt_alignment(prompt, output_path)
            print(f'DEBUG: {prompt_alignment}')
            harmonic_to_noise_ratio = compute_harmonic_to_noise_ratio(output_path)
            print(f'DEBUG: {harmonic_to_noise_ratio}')

            prompt_alignment_stored = round(prompt_alignment, 4)

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('''INSERT INTO music_records (prompt, prompt_type, duration, time_taken, cpu_usage, raga_similarity, prompt_alignment, harmonic_to_noise_ratio, audio_path, created_at)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (prompt, prompt_type, duration, time_taken, avg_cpu_usage, raga_similarity, prompt_alignment_stored, harmonic_to_noise_ratio, output_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()

            st.audio(output_path)

            with open(output_path, "rb") as file:
                audio_bytes = file.read()
                b64 = base64.b64encode(audio_bytes).decode()
                href = f'<a href="data:audio/wav;base64,{b64}" download="generated_music.wav">Download Music</a>'
                st.markdown(href, unsafe_allow_html=True)

            st.subheader("Metrics")
            st.write(f"Time Taken: {time_taken:.2f} seconds")
            st.write(f"Average CPU Usage: {avg_cpu_usage:.2f}%")
            # st.write(f"Indian Raga Similarity: {float(raga_similarity):.2f}")
            st.write(f"Prompt Sentiment Alignment: {float(prompt_alignment):.2f}")
            st.write(f"Harmonic-to-Noise Ratio (Melodic Clarity): {float(harmonic_to_noise_ratio):.2f}")