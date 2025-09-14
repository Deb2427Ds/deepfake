# streamlit_app.py
import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import io
import matplotlib.pyplot as plt
import base64
from detector import analyze_bytes, make_heatmap_image_bytes

st.set_page_config(page_title="Deepfake Defender — Demo", layout="wide")

st.title("🛡️ Deepfake Defender — Explainable Demo")
st.write("Upload an image or short video file (video preview supported). This is a demo with a mocked detector for hackathon presentation.")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded = st.file_uploader("Upload image / short video", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"])
    run_btn = st.button("Analyze")

with col2:
    st.markdown("**Demo tips**")
    st.markdown("- Use small videos (<=10s) for smooth demo.")
    st.markdown("- This demo uses a deterministic mocked detector (no heavy models) so it's fast to run locally.")

if uploaded:
    file_bytes = uploaded.read()
    mime = uploaded.type or ""
    if mime.startswith("image") or uploaded.name.lower().endswith((".jpg", ".jpeg", ".png")):
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        st.image(image, caption="Uploaded image", use_column_width=True)
    else:
        # show video preview for browsers that support it
        st.video(file_bytes)

if run_btn and uploaded:
    with st.spinner("Analyzing..."):
        # Use the mocked detector to produce a result dictionary
        result = analyze_bytes(file_bytes, uploaded.name)
        # Create / fetch a heatmap image bytes for overlay demonstration
        heatmap_bytes = make_heatmap_image_bytes(file_bytes)

    # Display results
    st.subheader("🔍 Detection Result")
    verdict = result.get("status", "unknown").upper()
    confidence = result.get("confidence", 0.0)
    reasons = result.get("reasons", [])
    timeline = result.get("timeline", [])

    # verdict badge
    if verdict == "REAL":
        badge_color = "background-color: #10B981; color: white; padding: 8px; border-radius: 8px;"
    elif verdict == "SUSPICIOUS":
        badge_color = "background-color: #F59E0B; color: black; padding: 8px; border-radius: 8px;"
    else:
        badge_color = "background-color: #EF4444; color: white; padding: 8px; border-radius: 8px;"

    st.markdown(f"<div style='{badge_color}'><strong>{verdict}</strong> — Confidence: {(confidence*100):.1f}%</div>", unsafe_allow_html=True)

    st.markdown("**Reasons:**")
    for r in reasons:
        st.write(f"- {r}")

    # Heatmap visualization (side-by-side with input preview)
    st.subheader("🔎 Forensic Heatmap (simulated)")
    heatmap_img = Image.open(io.BytesIO(heatmap_bytes)).convert("RGBA")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("Input (small preview)")
        if mime.startswith("image") or uploaded.name.lower().endswith((".jpg", ".jpeg", ".png")):
            st.image(ImageOps.fit(Image.open(io.BytesIO(file_bytes)).convert("RGB"), (512, 320)), use_column_width=False)
        else:
            st.write("Video preview shown above.")
    with col_b:
        st.image(heatmap_img, caption="Heatmap overlay (simulated)", use_column_width=False)

    # Timeline chart
    st.subheader("📈 Timeline: per-segment anomaly scores")
    if timeline:
        fig, ax = plt.subplots(figsize=(8, 2.2))
        ax.plot(timeline, marker="o", linewidth=2)
        ax.set_ylim(0, 1.05)
        ax.set_xlabel("Segment")
        ax.set_ylabel("Suspicion score")
        ax.grid(alpha=0.2)
        st.pyplot(fig)
    else:
        st.write("No timeline data available.")

    st.markdown("---")
    st.caption("This demo produces simulated explainability outputs (heatmap + timeline + textual reasons). Replace the mocked detector with real models for production.")

else:
    if not uploaded:
        st.info("Upload a file and press 'Analyze' to run the demo.")
