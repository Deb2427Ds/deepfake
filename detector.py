# detector.py
import hashlib
import math
import io
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def deterministic_score_from_bytes(b: bytes) -> float:
    """Produce a deterministic pseudo-random score in [0.35, 0.99] from file bytes."""
    h = hashlib.sha256(b).digest()
    # take few bytes to create a deterministic float
    x = (h[0] << 8) + h[1]
    n = (x % 10000) / 10000.0
    return 0.35 + n * 0.64  # range approx [0.35, 0.99]

def analyze_bytes(file_bytes: bytes, filename: str) -> dict:
    """Return mocked analysis dict:
       - status ('real','suspicious','fake')
       - confidence float [0,1]
       - reasons list
       - timeline list floats
    """
    score = deterministic_score_from_bytes(file_bytes)

    # slight heuristic on filename
    lower = (filename or "").lower()
    if "fake" in lower or "deepfake" in lower:
        score = min(0.995, score + 0.12)

    # status thresholds
    if score > 0.94:
        status = "fake"
    elif score > 0.78:
        status = "suspicious"
    else:
        status = "real"

    # build timeline: deterministic per-segment jitter
    timeline = []
    for i in range(20):
        h2 = hashlib.sha256(file_bytes + bytes([i])).digest()
        jitter = (h2[0] / 255.0) * 0.25
        t = max(0.0, min(1.0, score * (0.6 + jitter)))
        timeline.append(round(t, 3))

    reasons = []
    if score > 0.85:
        reasons.append("High-frequency blending artifacts")
    if score > 0.7:
        reasons.append("Skin-tone inconsistencies")
    if any(t > 0.9 for t in timeline):
        reasons.append("Temporal flicker / per-segment inconsistency")
    if not reasons:
        reasons.append("Low-confidence (no strong artifacts detected)")

    return {
        "status": status,
        "confidence": round(score, 3),
        "reasons": reasons,
        "timeline": timeline,
    }

def make_heatmap_image_bytes(file_bytes: bytes, out_w=512, out_h=320) -> bytes:
    """Create a synthetic heatmap image (RGBA) as bytes for demo visualization."""
    # seed deterministic from file hash
    seed = int.from_bytes(hashlib.sha256(file_bytes).digest()[:4], "big")
    rng = np.random.default_rng(seed)

    # base heatmap as smooth noise blobs
    heat = np.zeros((out_h, out_w), dtype=float)
    num_blobs = rng.integers(3, 7)
    for _ in range(num_blobs):
        cx = rng.integers(0, out_w)
        cy = rng.integers(0, out_h)
        rx = rng.integers(int(out_w*0.08), int(out_w*0.3))
        ry = rng.integers(int(out_h*0.08), int(out_h*0.3))
        y, x = np.ogrid[0:out_h, 0:out_w]
        mask = np.exp(-(((x - cx) ** 2) / (2 * rx * rx) + ((y - cy) ** 2) / (2 * ry * ry)))
        heat += mask * rng.uniform(0.6, 1.0)

    # normalize and colorize to RGBA
    heat = (heat - heat.min()) / max(1e-6, heat.max() - heat.min())
    heat = (heat * 255).astype("uint8")

    # convert to PIL image then colorize with a colormap-like scheme
    img = Image.fromarray(heat, mode="L").resize((out_w, out_h)).convert("RGBA")
    # apply simple colormap: map L to (r,g,b,a)
    pix = img.load()
    for y in range(out_h):
        for x in range(out_w):
            v = pix[x, y][0]
            # infer colors - blue->yellow->red progression
            r = int(min(255, v * 1.5))
            g = int(min(255, v))
            b = int(min(255, 255 - v // 2))
            alpha = int(100 + (v * 0.6))  # semi-transparent overlay
            pix[x, y] = (r, g, b, alpha)

    # soft blur
    img = img.filter(ImageFilter.GaussianBlur(radius=6))

    # return bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
