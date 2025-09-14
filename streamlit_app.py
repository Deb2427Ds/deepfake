import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Page setup
st.set_page_config(page_title="Deepfake Defender", page_icon="🛡️", layout="centered")

# Title
st.title("🛡️ Deepfake Defender")
st.markdown("AI-powered tool to detect **deepfakes & misinformation** in images, videos, and articles.")

# File uploader
uploaded_file = st.file_uploader("Upload file (JPG, PNG, MP4, MOV, TXT, PDF)", type=["jpg","jpeg","png","mp4","mov","avi","txt","pdf"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")
    st.info("Analyzing file... Please wait.")

    # --- Show image preview if image ---
    if uploaded_file.type.startswith("image/"):
        image = Image.open(uploaded_file)
        st.subheader("🖼️ Uploaded Image Preview")
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # --- Mock model output ---
    suspicion_scores = np.random.uniform(0.25, 0.45, size=20)  # Example values
    avg_confidence = 1 - suspicion_scores.mean()  
    confidence_percent = int(avg_confidence * 100)

    # --- Verdict ---
    if confidence_percent > 70:
        verdict = f"✅ Likely Real"
        color = "green"
    elif confidence_percent > 40:
        verdict = f"⚠️ Suspicious"
        color = "orange"
    else:
        verdict = f"❌ Likely Fake"
        color = "red"

    # Show verdict card
    st.markdown(f"""
    <div style="text-align:center; border-radius:15px; padding:20px; background-color:#f5f5f5">
        <h2 style="color:{color};">{verdict}</h2>
        <h4>Confidence Score: {confidence_percent}%</h4>
    </div>
    """, unsafe_allow_html=True)

    # --- Smaller Suspicion Timeline Graph ---
    st.subheader("📊 Suspicion Timeline")
    fig, ax = plt.subplots(figsize=(6,3))  # smaller figure
    ax.plot(suspicion_scores, marker='o', linewidth=2)
    ax.set_title("Suspicion Score per Segment", fontsize=12)
    ax.set_xlabel("Segment", fontsize=10)
    ax.set_ylabel("Suspicion Score", fontsize=10)
    ax.set_ylim([0,1])  # keep scale fixed
    st.pyplot(fig)

    # --- Explainability ---
    st.subheader("🔍 Explanation")
    st.write(f"""
    - **Verdict**: {verdict}  
    - **Confidence Score**: {confidence_percent}%  
    - **Suspicion Timeline**: Shows anomalies across different parts of the input.  
    """)
