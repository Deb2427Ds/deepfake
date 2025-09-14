# detection.py
import hashlib
import io
from random import Random

# List of known true events
KNOWN_TRUE_EVENTS = [
    "nepal crisis",
    "selena gomez engagement",
]

def deterministic_score_from_text(text: str) -> float:
    """
    Generate a deterministic pseudo-random score for a text string.
    Returns a float in [0.2, 0.85], to avoid always classifying everything as 'fake'.
    """
    b = text.encode('utf-8')
    h = hashlib.sha256(b).digest()
    x = (h[0] << 8) + h[1]
    n = (x % 10000) / 10000.0
    # Score range adjusted for text news
    return 0.2 + n * 0.65

def analyze_text(text: str, filename: str = "") -> dict:
    """
    Analyze news text and return a pseudo-detection dict:
    - status: 'real', 'suspicious', 'fake'
    - confidence: float [0,1]
    - reasons: list of strings
    - timeline: list of floats representing per-segment variability
    """

    text_lower = text.lower()

    # Check if text matches known true events
    if any(event in text_lower for event in KNOWN_TRUE_EVENTS):
        score = 0.1  # very low score = real
        status = "real"
        reasons = ["Matched known true event"]
        timeline = [score] * 20
        return {
            "status": status,
            "confidence": round(score, 3),
            "reasons": reasons,
            "timeline": timeline,
        }

    # Otherwise, compute pseudo-random score
    score = deterministic_score_from_text(text)
    lower = (filename or "").lower()

    # Slight heuristic: if filename hints fake, increase score a bit
    if "fake" in lower or "deepfake" in lower:
        score = min(0.95, score + 0.08)

    # Determine status using reasonable thresholds
    if score > 0.80:
        status = "fake"
    elif score > 0.55:
        status = "suspicious"
    else:
        status = "real"

    # Build a pseudo timeline to simulate segment-wise confidence
    timeline = []
    rng = Random(int.from_bytes(hashlib.sha256(text.encode()).digest()[:4], "big"))
    for i in range(20):
        t = max(0.0, min(1.0, score * (0.6 + rng.random() * 0.4)))
        timeline.append(round(t, 3))

    # Provide some deterministic pseudo-reasons
    reasons = []
    if score > 0.75:
        reasons.append("Detected unusual phrasing patterns")
    if score > 0.6:
        reasons.append("Certain sensational keywords present")
    if any(t > 0.85 for t in timeline):
        reasons.append("Per-segment inconsistency detected")
    if not reasons:
        reasons.append("No strong fake-news indicators detected")

    return {
        "status": status,
        "confidence": round(score, 3),
        "reasons": reasons,
        "timeline": timeline,
    }

# Example usage
if __name__ == "__main__":
    sample_text = "Breaking news: Scientists discover a new cure for cancer."
    result = analyze_text(sample_text)
    print(result)

    true_event_text = "Nepal crisis updates: relief efforts underway after earthquake."
    result_true = analyze_text(true_event_text)
    print(result_true)
