# detection.py
import os
import cv2
import pytesseract

# 🔹 Update this path to where you moved Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract\tesseract.exe"

def validate_image(path):
    valid_types = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(path)[1]
    return ext.lower() in valid_types

def detect_blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance < 100

def detect_edges(image):
    edges = cv2.Canny(image, 100, 200)
    return edges.mean()

def extract_text(image):
    try:
        text = pytesseract.image_to_string(image)
    except Exception as e:
        print("⚠️ Tesseract OCR failed:", e)
        text = ""
    return text

def analyze_image(path):
    if not validate_image(path):
        return {"error": "Invalid image type"}

    image = cv2.imread(path)
    if image is None:
        return {"error": "Cannot read image"}

    # Step 1: Blur
    blur = detect_blur(image)

    # Step 2: Edges
    edge_score = detect_edges(image)

    # Step 3: OCR
    text = extract_text(image)

    # Step 4: Risk Calculation
    risk = 0
    if blur:
        risk += 30
    if edge_score < 20:
        risk += 30
    if len(text.strip()) < 10:
        risk += 40

    # Final confidence and status
    confidence = max(0, 100 - risk)
    status = "Suspicious Document" if risk > 50 else "Likely Genuine"

    # Return report
    report = {
        "blur_detected": blur,
        "edge_score": round(edge_score, 2),
        "text_length": len(text.strip()),
        "risk_score": risk,
        "confidence": confidence,
        "final_status": status
    }

    return report