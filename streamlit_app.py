import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Title & description
st.set_page_config(page_title="Deepfake Defender", page_icon="🛡️", layout="wide")
st.title("🛡️ Deepfake Defender – AI-powered Fake News & Deepfake Detector")
st.markdown("Upload an **image, video, or article screenshot** to analyze authenticity.")

# Upload input
uploaded_file = st.file_uploader("Upload file (JPG, PNG, MP4, MOV, PDF, TXT)", type=["jpg","jpeg","png","mp4","mov","avi","pdf","txt"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")
    st.info("Analyzing for deepfake or misinformation patterns...")

    # --- Mocked model output (replace with real model later) ---
    suspicion_scores = np.random.uniform(0.25, 0.45, size=20)  # 20 timeline points
    avg_confidence = 1 - suspicion_scores.mean()  # Higher = more real
    confidence_percent = int(avg_confidence * 100)

    # --- Verdict ---
    if confidence_percent > 70:
        verdict = f"✅ Likely Real (Confidence: {confidence_percent}%)"
        color = "green"
    elif confidence_percent > 40:
        verdict = f"⚠️ Suspicious (Confidence: {confidence_percent}%)"
        color = "orange"
    else:
        verdict = f"❌ Likely Fake (Confidence: {confidence_percent}%)"
        color = "red"

    st.markdown(f"<h3 style='color:{color};text-align:center'>{verdict}</h3>", unsafe_allow_html=True)

    # --- Suspicion Timeline Graph ---
    fig, ax = plt.subplots()
    ax.plot(suspicion_scores, marker='o')
    ax.set_title("📊 Timeline Suspicion Score")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Suspicion Score (0 = Real, 1 = Fake)")
    st.pyplot(fig)

    # --- Explanation ---
    st.subheader("🔍 Explainability")
    st.write("""
    - **Suspicion Score per Segment**: Breaks the input into chunks (video frames / text segments).  
    - **Confidence Score**: Overall authenticity likelihood.  
    - **Why it matters**: Even if some parts are suspicious, the overall verdict reflects average reliability.  
    """)
