import cv2
import numpy as np
import pytesseract
from PIL import Image
import streamlit as st
from typing import Tuple, Optional

class OCRProcessor:
    """Handles OCR processing for textbook images"""
    
    def __init__(self):
        """Initialize OCR processor with Tesseract configuration"""
        # Configure Tesseract for better text extraction
        self.custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;:()[]{}"\'-_+=/\\|@#$%^&*~`<>'
        
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR results
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply thresholding to get binary image
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Apply morphological operations to clean up the image
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text(self, image: np.ndarray) -> str:
        """
        Extract text from image using Tesseract OCR
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Extracted text
        """
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(
                processed_image, 
                config=self.custom_config
            )
            
            # Clean up the extracted text
            cleaned_text = self.clean_text(text)
            
            return cleaned_text
            
        except Exception as e:
            st.error(f"Error in OCR processing: {str(e)}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """
        Clean and format extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace and normalize
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove excessive whitespace
            line = ' '.join(line.split())
            
            # Skip empty lines
            if line.strip():
                cleaned_lines.append(line)
        
        # Join lines with proper spacing
        cleaned_text = '\n'.join(cleaned_lines)
        
        return cleaned_text
    
    def get_text_confidence(self, image: np.ndarray) -> float:
        """
        Get confidence score for OCR extraction
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Confidence score (0-100)
        """
        try:
            processed_image = self.preprocess_image(image)
            
            # Get OCR data with confidence scores
            data = pytesseract.image_to_data(
                processed_image, 
                config=self.custom_config,
                output_type=pytesseract.Output.DICT
            )
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            
            if confidences:
                return sum(confidences) / len(confidences)
            else:
                return 0.0
                
        except Exception as e:
            st.warning(f"Could not calculate confidence: {str(e)}")
            return 0.0
    
    def detect_language(self, text: str) -> str:
        """
        Simple language detection based on character patterns
        
        Args:
            text: Extracted text
            
        Returns:
            Detected language code
        """
        # Simple heuristic-based language detection
        # This is a basic implementation - for production, use proper language detection libraries
        
        # Count non-ASCII characters (indicating non-English)
        non_ascii_count = sum(1 for char in text if ord(char) > 127)
        total_chars = len(text)
        
        if total_chars == 0:
            return 'en'
        
        non_ascii_ratio = non_ascii_count / total_chars
        
        # Simple thresholds for language detection
        if non_ascii_ratio > 0.3:
            # Could be Spanish, French, German, etc.
            return 'es'  # Default to Spanish for demo
        else:
            return 'en'
    
    def process_uploaded_image(self, uploaded_file) -> Tuple[str, float, str]:
        """
        Process uploaded image file and extract text
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (extracted_text, confidence, detected_language)
        """
        try:
            # Read image
            image = Image.open(uploaded_file)
            image_array = np.array(image)
            
            # Extract text
            text = self.extract_text(image_array)
            
            # Get confidence
            confidence = self.get_text_confidence(image_array)
            
            # Detect language
            language = self.detect_language(text)
            
            return text, confidence, language
            
        except Exception as e:
            st.error(f"Error processing uploaded image: {str(e)}")
            return "", 0.0, "en" 