import streamlit as st
import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt

DB_PATH = os.path.join(".", "music_data.db")

def fetch_records():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM music_records", conn)
    for col in ['time_taken', 'cpu_usage', 'raga_similarity', 'prompt_alignment', 'harmonic_to_noise_ratio']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    conn.close()
    return df

def delete_record(record_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM music_records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def analyze_metrics(df):
    st.subheader("Metrics Analysis")
    
    st.write("### Time Taken vs Duration")
    fig, ax = plt.subplots()
    ax.scatter(df['duration'], df['time_taken'], color='blue')
    ax.set_xlabel("Duration (seconds)")
    ax.set_ylabel("Time Taken (seconds)")
    st.pyplot(fig)

    st.write("### CPU Usage Distribution")
    fig, ax = plt.subplots()
    ax.hist(df['cpu_usage'], bins=10, color='green')
    ax.set_xlabel("CPU Usage (%)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    st.write("### CPU Usage by Prompt Type")
    avg_cpu_by_type = df.groupby('prompt_type')['cpu_usage'].mean().dropna()
    if not avg_cpu_by_type.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        avg_cpu_by_type.plot(kind='bar', ax=ax, color='blue')
        ax.set_xlabel("Prompt Type")
        ax.set_ylabel("Average CPU Usage (%)")
        ax.set_title("Average CPU Usage by Prompt Type")
        plt.xticks(rotation=45, ha='right')
        for i, v in enumerate(avg_cpu_by_type):
            ax.text(i, v + 0.5, f"{v:.2f}", ha='center', va='bottom')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write("No valid CPU usage data available to plot.")


    st.write("### Prompt Sentiment Alignment by Prompt Type")
    avg_alignments = df.groupby('prompt_type')['prompt_alignment'].mean().dropna()
    if not avg_alignments.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        avg_alignments.plot(kind='bar', ax=ax, color='purple')
        ax.set_xlabel("Prompt Type")
        ax.set_ylabel("Average Sentiment Alignment")
        ax.set_ylim(0, 1)
        ax.set_title("Average Prompt Sentiment Alignment by Prompt Type")
        plt.xticks(rotation=45, ha='right')
        for i, v in enumerate(avg_alignments):
            ax.text(i, v + 0.02, f"{v:.2f}", ha='center', va='bottom')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write("No valid sentiment alignment data available to plot.")


    st.write("### Harmonic-to-Noise Ratio vs Prompt Sentiment Alignment")
    fig, ax = plt.subplots()
    prompt_types = df['prompt_type'].unique()
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']  
    for i, prompt_type in enumerate(prompt_types):
        subset = df[df['prompt_type'] == prompt_type]
        ax.scatter(subset['prompt_alignment'].dropna(), subset['harmonic_to_noise_ratio'].dropna(), 
                   color=colors[i % len(colors)], label=prompt_type, alpha=0.6)
    ax.set_xlabel("Prompt Sentiment Alignment")
    ax.set_ylabel("Harmonic-to-Noise Ratio")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(title="Prompt Type")
    st.pyplot(fig)


    st.write("### Harmonic-to-Noise Ratio Distribution")
    fig, ax = plt.subplots()
    ax.hist(df['harmonic_to_noise_ratio'].dropna(), bins=10, color='orange')
    ax.set_xlabel("Harmonic-to-Noise Ratio")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)


    st.write("### Average Harmonic-to-Noise Ratio by Prompt Type")
    avg_hnr_by_type = df.groupby('prompt_type')['harmonic_to_noise_ratio'].mean().dropna()
    if not avg_hnr_by_type.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        avg_hnr_by_type.plot(kind='bar', ax=ax, color='teal')
        ax.set_xlabel("Prompt Type")
        ax.set_ylabel("Average Harmonic-to-Noise Ratio")
        ax.set_ylim(0, 1)
        ax.set_title("Average Harmonic-to-Noise Ratio by Prompt Type")
        plt.xticks(rotation=45, ha='right')
        for i, v in enumerate(avg_hnr_by_type):
            ax.text(i, v + 0.02, f"{v:.2f}", ha='center', va='bottom')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write("No valid harmonic-to-noise ratio data available to plot.")

st.title("Music Database Manager")

if 'playing_audio_id' not in st.session_state:
    st.session_state.playing_audio_id = None

df = fetch_records()
if df.empty:
    st.write("No records found.")
else:
    st.subheader("Music Generation Summary")
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([3, 1, 1, 1, 1, 1, 1, 1])
    with col1:
        st.markdown("**Prompt**")
    with col2:
        st.markdown("**Prompt Type**")
    with col3:
        st.markdown("**Duration (s)**")
    with col4:
        st.markdown("**Time Taken (s)**")
    with col5:
        st.markdown("**Prompt Sentiment Alignment**")
    with col6:
        st.markdown("**HNR**")
    with col7:
        st.markdown("**Play**")
    with col8:
        st.markdown("**Delete**")
    
    for index, row in df.iterrows():
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([3, 1, 1, 1, 1, 1, 1, 1])
        with col1:
            st.write(row['prompt'])
        with col2:
            st.write(row['prompt_type'])
        with col3:
            st.write(row['duration'])
        with col4:
            time_taken = row['time_taken']
            if pd.isna(time_taken):
                st.write("N/A")
            else:
                st.write(f"{time_taken:.2f}")
        with col5:
            alignment = row['prompt_alignment']
            if pd.isna(alignment):
                st.write("N/A")
            else:
                st.write(f"{alignment:.2f}")
        with col6:
            hnr = row['harmonic_to_noise_ratio']
            if pd.isna(hnr):
                st.write("N/A")
            else:
                st.write(f"{hnr:.2f}")
        with col7:
            if os.path.exists(row['audio_path']):
                if st.button("▶️", key=f"play_button_{row['id']}"):
                    if st.session_state.playing_audio_id == row['id']:
                        st.session_state.playing_audio_id = None
                    else:
                        st.session_state.playing_audio_id = row['id']
            else:
                st.write("File not found")
        
        with col8:
            if st.button("❌", key=f"summary_delete_{row['id']}"):
                delete_record(row['id'])
                if st.session_state.playing_audio_id == row['id']:
                    st.session_state.playing_audio_id = None
                st.rerun()

        if st.session_state.playing_audio_id == row['id']:
            with st.expander(f"Playing: {row['prompt']}", expanded=True):
                st.audio(row['audio_path'], start_time=0)

    if st.button("Analyze Metrics"):
        analyze_metrics(df)