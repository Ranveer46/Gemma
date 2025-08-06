import streamlit as st
import os
import tempfile
from typing import Optional, List, Dict, Any
import json
from datetime import datetime

def create_temp_file(content: str, suffix: str = '.txt') -> str:
    """
    Create a temporary file with given content
    
    Args:
        content: Content to write to file
        suffix: File extension
        
    Returns:
        Path to temporary file
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode='w', encoding='utf-8')
    temp_file.write(content)
    temp_file.close()
    return temp_file.name

def cleanup_temp_files(file_paths: List[str]):
    """
    Clean up temporary files
    
    Args:
        file_paths: List of file paths to delete
    """
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            st.warning(f"Could not delete temporary file {file_path}: {e}")

def detect_language_simple(text: str) -> str:
    """
    Simple language detection based on character patterns
    
    Args:
        text: Text to analyze
        
    Returns:
        Language code
    """
    if not text:
        return 'en'
    
    # Count non-ASCII characters
    non_ascii_count = sum(1 for char in text if ord(char) > 127)
    total_chars = len(text)
    
    if total_chars == 0:
        return 'en'
    
    non_ascii_ratio = non_ascii_count / total_chars
    
    # Simple heuristics for language detection
    if non_ascii_ratio > 0.3:
        # Check for specific language patterns
        if any(char in text for char in 'ñáéíóúü'):
            return 'es'  # Spanish
        elif any(char in text for char in 'àâäéèêëïîôöùûüÿç'):
            return 'fr'  # French
        elif any(char in text for char in 'äöüß'):
            return 'de'  # German
        else:
            return 'es'  # Default to Spanish for non-English
    else:
        return 'en'

def get_language_name(code: str) -> str:
    """
    Get language name from language code
    
    Args:
        code: Language code
        
    Returns:
        Language name
    """
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese'
    }
    return languages.get(code, 'Unknown')

def format_timestamp() -> str:
    """
    Get formatted timestamp for logging
    
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_session_data(key: str, data: Any):
    """
    Save data to Streamlit session state
    
    Args:
        key: Session state key
        data: Data to save
    """
    st.session_state[key] = data

def load_session_data(key: str, default: Any = None) -> Any:
    """
    Load data from Streamlit session state
    
    Args:
        key: Session state key
        default: Default value if key doesn't exist
        
    Returns:
        Data from session state or default value
    """
    return st.session_state.get(key, default)

def create_download_button(content: str, filename: str, label: str = "Download"):
    """
    Create a download button for text content
    
    Args:
        content: Content to download
        filename: Name of the file
        label: Button label
    """
    if content:
        st.download_button(
            label=label,
            data=content,
            file_name=filename,
            mime="text/plain"
        )

def display_confidence_bar(confidence: float):
    """
    Display confidence score as a progress bar
    
    Args:
        confidence: Confidence score (0-100)
    """
    if confidence > 0:
        st.progress(confidence / 100)
        st.caption(f"Confidence: {confidence:.1f}%")

def create_info_box(title: str, content: str, icon: str = "ℹ️"):
    """
    Create a styled info box
    
    Args:
        title: Box title
        content: Box content
        icon: Icon to display
    """
    st.markdown(f"""
    <div style="
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    ">
        <h4 style="margin: 0 0 0.5rem 0; color: #1f77b4;">
            {icon} {title}
        </h4>
        <p style="margin: 0; color: #333;">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_success_box(title: str, content: str, icon: str = "✅"):
    """
    Create a styled success box
    
    Args:
        title: Box title
        content: Box content
        icon: Icon to display
    """
    st.markdown(f"""
    <div style="
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    ">
        <h4 style="margin: 0 0 0.5rem 0; color: #155724;">
            {icon} {title}
        </h4>
        <p style="margin: 0; color: #155724;">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_warning_box(title: str, content: str, icon: str = "⚠️"):
    """
    Create a styled warning box
    
    Args:
        title: Box title
        content: Box content
        icon: Icon to display
    """
    st.markdown(f"""
    <div style="
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    ">
        <h4 style="margin: 0 0 0.5rem 0; color: #856404;">
            {icon} {title}
        </h4>
        <p style="margin: 0; color: #856404;">
            {content}
        </p>
    </div>
    """, unsafe_allow_html=True)

def validate_image_file(uploaded_file) -> bool:
    """
    Validate uploaded image file
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        True if valid image file, False otherwise
    """
    if uploaded_file is None:
        return False
    
    # Check file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff']
    if uploaded_file.type not in allowed_types:
        st.error("Please upload a valid image file (JPEG, PNG, BMP, or TIFF)")
        return False
    
    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if uploaded_file.size > max_size:
        st.error("File size too large. Please upload an image smaller than 10MB")
        return False
    
    return True

def get_file_size_mb(file_size_bytes: int) -> float:
    """
    Convert file size from bytes to MB
    
    Args:
        file_size_bytes: File size in bytes
        
    Returns:
        File size in MB
    """
    return file_size_bytes / (1024 * 1024)

def create_model_status_display(model_info: Dict[str, Any]):
    """
    Display model status information
    
    Args:
        model_info: Model information dictionary
    """
    if model_info.get("status") == "Loaded":
        create_success_box(
            "Model Status",
            f"Model: {model_info.get('model_name', 'Unknown')}<br>"
            f"Device: {model_info.get('device', 'Unknown')}<br>"
            f"Temperature: {model_info.get('temperature', 0.7)}<br>"
            f"Max Length: {model_info.get('max_length', 2048)}",
            "🤖"
        )
    else:
        create_warning_box(
            "Model Status",
            "AI model is not loaded. Please load the model to use the application.",
            "⚠️"
        )

def log_interaction(interaction_type: str, details: Dict[str, Any]):
    """
    Log user interactions for analytics
    
    Args:
        interaction_type: Type of interaction
        details: Interaction details
    """
    log_entry = {
        "timestamp": format_timestamp(),
        "type": interaction_type,
        "details": details
    }
    
    # Save to session state for this session
    logs = load_session_data("interaction_logs", [])
    logs.append(log_entry)
    save_session_data("interaction_logs", logs)

def get_system_info() -> Dict[str, Any]:
    """
    Get system information for debugging
    
    Returns:
        System information dictionary
    """
    import platform
    import psutil
    
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version(),
        "cpu_count": psutil.cpu_count(),
        "memory_total": f"{psutil.virtual_memory().total / (1024**3):.1f} GB",
        "memory_available": f"{psutil.virtual_memory().available / (1024**3):.1f} GB"
    } 