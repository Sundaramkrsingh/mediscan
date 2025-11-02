"""
Advanced Image Preprocessing for OCR and Barcode Detection
Implements multiple preprocessing techniques to improve accuracy
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum


class PreprocessingMode(Enum):
    """Different preprocessing modes for various image types"""
    BARCODE = "barcode"
    TEXT_OCR = "text_ocr"
    LABEL = "label"
    GENERAL = "general"


class ImageProcessor:
    """Advanced image preprocessing for medicine packaging analysis"""

    def __init__(self):
        self.debug_mode = False

    def preprocess_for_barcode(self, image: np.ndarray) -> List[np.ndarray]:
        """
        Preprocess image optimized for barcode/QR code detection
        Returns multiple variations to increase detection rate

        Args:
            image: Input image (BGR format from OpenCV)

        Returns:
            List of preprocessed image variations
        """
        variations = []

        # Original grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        variations.append(gray)

        # High contrast version
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        variations.append(enhanced)

        # Binary threshold
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        variations.append(binary)

        # Adaptive threshold
        adaptive = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        variations.append(adaptive)

        return variations

    def preprocess_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image optimized for text OCR
        Applies advanced techniques to improve text recognition

        Args:
            image: Input image (BGR format)

        Returns:
            Preprocessed image optimized for OCR
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

        # Increase contrast with CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        contrast = clahe.apply(denoised)

        # Deskew (correct rotation)
        deskewed = self._deskew_image(contrast)

        # Sharpen
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        sharpened = cv2.filter2D(deskewed, -1, kernel)

        # Adaptive threshold for better text separation
        processed = cv2.adaptiveThreshold(
            sharpened,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            9
        )

        # Morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)

        return processed

    def _deskew_image(self, image: np.ndarray) -> np.ndarray:
        """
        Detect and correct skew in image

        Args:
            image: Grayscale image

        Returns:
            Deskewed image
        """
        # Calculate skew angle
        coords = np.column_stack(np.where(image > 0))
        if len(coords) == 0:
            return image

        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        # Rotate only if skew is significant (more than 0.5 degrees)
        if abs(angle) > 0.5:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(
                image,
                M,
                (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )
            return rotated

        return image

    def enhance_for_expiry_date(self, image: np.ndarray, roi: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """
        Special preprocessing for expiry date detection
        Focuses on small text areas

        Args:
            image: Input image
            roi: Optional region of interest (x, y, w, h)

        Returns:
            Enhanced image for date detection
        """
        # Extract ROI if provided
        if roi:
            x, y, w, h = roi
            image = image[y:y+h, x:x+w]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

        # Upscale small images for better OCR
        if min(gray.shape) < 100:
            scale_factor = 2
            gray = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

        # Strong denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, h=15, templateWindowSize=7, searchWindowSize=21)

        # High contrast
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(4, 4))
        enhanced = clahe.apply(denoised)

        # Binary threshold
        _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Clean up small artifacts
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        return cleaned

    def detect_text_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect potential text regions in image using MSER or contours

        Args:
            image: Input image

        Returns:
            List of bounding boxes (x, y, w, h) for text regions
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

        # Use morphological operations to find text regions
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
        dilated = cv2.morphologyEx(gray, cv2.MORPH_DILATE, kernel)

        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Filter out very small or very large regions
            if w > 50 and h > 20 and w < gray.shape[1] * 0.9 and h < gray.shape[0] * 0.5:
                regions.append((x, y, w, h))

        return regions

    def combine_images_for_analysis(self, images: List[np.ndarray]) -> np.ndarray:
        """
        Combine multiple images of the same product for comprehensive analysis

        Args:
            images: List of images

        Returns:
            Combined/stitched image or best quality image
        """
        if not images:
            return None

        if len(images) == 1:
            return images[0]

        # For now, return the largest/highest quality image
        # In future, can implement image stitching
        largest = max(images, key=lambda x: x.shape[0] * x.shape[1])
        return largest

    def assess_image_quality(self, image: np.ndarray) -> Dict[str, float]:
        """
        Assess image quality metrics

        Args:
            image: Input image

        Returns:
            Dictionary with quality metrics
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

        # Blur detection (Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        # Brightness
        brightness = np.mean(gray)

        # Contrast
        contrast = gray.std()

        return {
            "sharpness": laplacian_var,
            "brightness": brightness,
            "contrast": contrast,
            "quality_score": min(100, (laplacian_var / 100) * 50 + (contrast / 128) * 50)
        }

    def auto_rotate_upright(self, image: np.ndarray) -> np.ndarray:
        """
        Automatically rotate image to upright orientation using text detection

        Args:
            image: Input image

        Returns:
            Rotated image
        """
        # Try different rotations and pick the one with best text detection score
        best_score = 0
        best_rotation = 0

        for angle in [0, 90, 180, 270]:
            rotated = self._rotate_image(image, angle)
            score = self._score_text_orientation(rotated)

            if score > best_score:
                best_score = score
                best_rotation = angle

        return self._rotate_image(image, best_rotation)

    def _rotate_image(self, image: np.ndarray, angle: int) -> np.ndarray:
        """Rotate image by specific angle"""
        if angle == 0:
            return image

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)

        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

        return rotated

    def _score_text_orientation(self, image: np.ndarray) -> float:
        """Score text orientation quality"""
        # Simple heuristic: count horizontal edges vs vertical edges
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image

        # Sobel edge detection
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        # Horizontal text typically has more horizontal edges
        horizontal_score = np.sum(np.abs(sobelx))
        vertical_score = np.sum(np.abs(sobely))

        return horizontal_score / (vertical_score + 1)


def preprocess_image(image: np.ndarray, mode: PreprocessingMode = PreprocessingMode.GENERAL) -> np.ndarray:
    """
    Convenience function to preprocess image based on mode

    Args:
        image: Input image
        mode: Preprocessing mode

    Returns:
        Preprocessed image
    """
    processor = ImageProcessor()

    if mode == PreprocessingMode.BARCODE:
        return processor.preprocess_for_barcode(image)[0]
    elif mode == PreprocessingMode.TEXT_OCR:
        return processor.preprocess_for_ocr(image)
    else:
        return processor.preprocess_for_ocr(image)


if __name__ == "__main__":
    print("Image processor module loaded successfully")
