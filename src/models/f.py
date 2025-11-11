import cv2
import numpy as np


def filter_img(img):
    # --- Convert to float for better color math ---
    img = img.astype(np.float32) / 255.0

    # 🔹 Layer 1 – Base Smooth Denoise (preserve edges)
    layer1 = cv2.bilateralFilter(img, 9, 75, 75)

    # 🔹 Layer 2 – RGB Channel Boost (individual enhancement)
    b, g, r = cv2.split(layer1)
    r = cv2.pow(r, 0.9) * 1.1   # brighten reds
    g = cv2.pow(g, 0.95) * 1.05 # balance greens
    b = cv2.pow(b, 0.9) * 1.1   # brighten blues
    layer2 = cv2.merge((b, g, r))
    layer2 = np.clip(layer2, 0, 1)

    # 🔹 Layer 3 – Sharpness Filter (RGB-space)
    kernel = np.array([
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ], dtype=np.float32)
    layer3 = cv2.filter2D(layer2, -1, kernel)

    # 🔹 Layer 4 – RGB Contrast Enhancement
    mean_color = np.mean(layer3, axis=(0,1))
    contrast = np.clip((layer3 - mean_color) * 1.4 + mean_color, 0, 1)

    # 🔹 Layer 5 – Glow + Brightness Balance
    bright = cv2.GaussianBlur(contrast, (0, 0), 2)
    layer5 = cv2.addWeighted(contrast, 1.2, bright, -0.2, 0)

    # --- Convert back to 8-bit and save ---
    final = np.clip(layer5 * 255, 0, 255).astype(np.uint8)
    return final
