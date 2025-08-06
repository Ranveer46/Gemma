import streamlit as st
import os
import tempfile
from typing import Optional
import json

# Import our custom modules
from ocr_processor import OCRProcessor
from ai_engine import AIEngine
import utils

# Page configuration
st.set_page_config(
    page_title="AI Educational Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'ai_engine' not in st.session_state:
        st.session_state.ai_engine = AIEngine()
    if 'ocr_processor' not in st.session_state:
        st.session_state.ocr_processor = OCRProcessor()
    if 'model_loaded' not in st.session_state:
        st.session_state.model_loaded = False
    if 'current_language' not in st.session_state:
        st.session_state.current_language = 'en'
    if 'audio_output_enabled' not in st.session_state:
        st.session_state.audio_output_enabled = False

def main_header():
    """Display the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Educational Assistant</h1>
        <p>Your intelligent learning companion powered by Google Gemma</p>
    </div>
    """, unsafe_allow_html=True)

def sidebar_settings():
    """Sidebar with settings and model controls"""
    st.sidebar.title("⚙️ Settings")
    
    # Model loading section
    st.sidebar.subheader("🤖 AI Model")
    
    if not st.session_state.model_loaded:
        if st.sidebar.button("Load AI Model", type="primary"):
            with st.spinner("Loading AI model..."):
                success = st.session_state.ai_engine.load_model()
                if success:
                    st.session_state.model_loaded = True
                    st.sidebar.success("Model loaded!")
                    st.rerun()
    else:
        st.sidebar.success("✅ Model Loaded")
        if st.sidebar.button("Reload Model"):
            st.session_state.model_loaded = False
            st.rerun()
    
    # Model settings
    if st.session_state.model_loaded:
        st.sidebar.subheader("🎛️ Model Settings")
        
        temperature = st.sidebar.slider(
            "Temperature", 
            min_value=0.1, 
            max_value=2.0, 
            value=0.7, 
            step=0.1,
            help="Controls randomness in text generation"
        )
        
        top_p = st.sidebar.slider(
            "Top-p", 
            min_value=0.1, 
            max_value=1.0, 
            value=0.9, 
            step=0.1,
            help="Controls diversity in text generation"
        )
        
        st.session_state.ai_engine.update_settings(temperature=temperature, top_p=top_p)
    
    # Language settings
    st.sidebar.subheader("🌍 Language")
    languages = {
        'en': 'English',
        'es': 'Spanish', 
        'fr': 'French',
        'de': 'German'
    }
    
    selected_language = st.sidebar.selectbox(
        "Select Language",
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        index=0
    )
    st.session_state.current_language = selected_language
    
    # Audio settings
    st.sidebar.subheader("🔊 Audio")
    st.session_state.audio_output_enabled = st.sidebar.checkbox(
        "Enable Audio Output",
        value=False,
        help="Convert AI responses to speech (requires internet)"
    )
    
    # Deployment info
    st.sidebar.subheader("☁️ Deployment")
    st.sidebar.info("Running on cloud platform")
    st.sidebar.caption("Voice features use online services")

def textbook_analysis_tab():
    """Textbook image analysis functionality"""
    st.header("📷 Textbook Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Textbook Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Upload a clear image of a textbook page"
        )
        
        if uploaded_file:
            # Validate file
            if utils.validate_image_file(uploaded_file):
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                st.info(f"File size: {utils.get_file_size_mb(uploaded_file.size):.2f} MB")
                
                # Display image
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                
                # Process image button
                if st.button("🔍 Analyze Image", type="primary"):
                    if not st.session_state.model_loaded:
                        st.error("Please load the AI model first!")
                    else:
                        process_textbook_image(uploaded_file)
    
    with col2:
        st.subheader("How it works")
        utils.create_info_box(
            "Step 1: Upload",
            "Upload a clear image of a textbook page",
            "📤"
        )
        utils.create_info_box(
            "Step 2: OCR Processing", 
            "Text is extracted using advanced OCR technology",
            "🔍"
        )
        utils.create_info_box(
            "Step 3: AI Analysis",
            "Content is summarized in student-friendly language",
            "🤖"
        )

def process_textbook_image(uploaded_file):
    """Process uploaded textbook image"""
    with st.spinner("Processing image..."):
        # Extract text using OCR
        extracted_text, confidence, detected_language = st.session_state.ocr_processor.process_uploaded_image(uploaded_file)
        
        if extracted_text:
            st.success("✅ Text extracted successfully!")
            
            # Display extracted text
            with st.expander("📝 Extracted Text", expanded=False):
                st.text_area("Raw Text", extracted_text, height=200)
                utils.display_confidence_bar(confidence)
                st.caption(f"Detected language: {utils.get_language_name(detected_language)}")
            
            # Generate summary
            if st.session_state.model_loaded:
                with st.spinner("Generating summary..."):
                    summary = st.session_state.ai_engine.summarize_text(
                        extracted_text, 
                        st.session_state.current_language
                    )
                    
                    if summary:
                        st.subheader("📚 Student-Friendly Summary")
                        st.markdown(f"**{summary}**")
                        
                        # Audio output using online TTS
                        if st.session_state.audio_output_enabled:
                            try:
                                from gtts import gTTS
                                tts = gTTS(text=summary, lang=st.session_state.current_language)
                                audio_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                                tts.save(audio_path.name)
                                st.audio(audio_path.name)
                            except Exception as e:
                                st.warning(f"Audio generation failed: {e}")
                        
                        # Download options
                        col1, col2 = st.columns(2)
                        with col1:
                            utils.create_download_button(
                                summary, 
                                "summary.txt", 
                                "📥 Download Summary"
                            )
                        with col2:
                            utils.create_download_button(
                                extracted_text, 
                                "extracted_text.txt", 
                                "📥 Download Raw Text"
                            )
                        
                        # Log interaction
                        utils.log_interaction("textbook_analysis", {
                            "file_name": uploaded_file.name,
                            "confidence": confidence,
                            "language": detected_language,
                            "summary_length": len(summary)
                        })
        else:
            st.error("❌ Could not extract text from image. Please try a clearer image.")

def text_qa_tab():
    """Text question and answer functionality"""
    st.header("💬 Text Q&A")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Ask Your Question")
        
        # Text input
        text_question = st.text_area(
            "Type your educational question:",
            placeholder="Ask any educational question...",
            height=100
        )
        
        # Example questions
        st.markdown("### 💡 Example Questions")
        example_questions = [
            "What is photosynthesis?",
            "How do plants make their own food?",
            "Why is photosynthesis important for life on Earth?",
            "What is gravity and how does it work?",
            "How do fractions work in mathematics?"
        ]
        
        for question in example_questions:
            if st.button(f"💭 {question}", key=f"example_{question}"):
                st.session_state.example_question = question
                st.rerun()
        
        # Process question
        question_to_process = st.session_state.get('example_question', '') or text_question
        
        if question_to_process and st.button("🤖 Get Answer", type="primary"):
            if not st.session_state.model_loaded:
                st.error("Please load the AI model first!")
            else:
                process_text_question(question_to_process)
    
    with col2:
        st.subheader("How it works")
        utils.create_info_box(
            "Step 1: Ask Question",
            "Type your educational question",
            "💬"
        )
        utils.create_info_box(
            "Step 2: AI Processing",
            "Question is analyzed and answered by AI",
            "🤖"
        )
        utils.create_info_box(
            "Step 3: Get Answer",
            "Receive clear, educational response",
            "💡"
        )

def process_text_question(question: str):
    """Process text question and generate answer"""
    with st.spinner("Generating answer..."):
        # Generate answer
        answer = st.session_state.ai_engine.answer_question(
            question, 
            st.session_state.current_language
        )
        
        if answer:
            st.subheader("💡 AI Answer")
            st.markdown(f"**{answer}**")
            
            # Audio output using online TTS
            if st.session_state.audio_output_enabled:
                try:
                    from gtts import gTTS
                    tts = gTTS(text=answer, lang=st.session_state.current_language)
                    audio_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                    tts.save(audio_path.name)
                    st.audio(audio_path.name)
                except Exception as e:
                    st.warning(f"Audio generation failed: {e}")
            
            # Download answer
            utils.create_download_button(
                answer, 
                "ai_answer.txt", 
                "📥 Download Answer"
            )
            
            # Log interaction
            utils.log_interaction("text_qa", {
                "question": question,
                "answer_length": len(answer),
                "language": st.session_state.current_language
            })
        else:
            st.error("❌ Could not generate answer. Please try again.")

def concept_explanation_tab():
    """Concept explanation functionality"""
    st.header("📖 Concept Explanation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Explain a Concept")
        
        concept = st.text_area(
            "Enter a concept to explain:",
            placeholder="e.g., photosynthesis, gravity, democracy...",
            height=100
        )
        
        if concept and st.button("🔍 Explain Concept", type="primary"):
            if not st.session_state.model_loaded:
                st.error("Please load the AI model first!")
            else:
                with st.spinner("Generating explanation..."):
                    explanation = st.session_state.ai_engine.explain_concept(
                        concept, 
                        st.session_state.current_language
                    )
                    
                    if explanation:
                        st.subheader("📚 Explanation")
                        st.markdown(f"**{explanation}**")
                        
                        # Audio output using online TTS
                        if st.session_state.audio_output_enabled:
                            try:
                                from gtts import gTTS
                                tts = gTTS(text=explanation, lang=st.session_state.current_language)
                                audio_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                                tts.save(audio_path.name)
                                st.audio(audio_path.name)
                            except Exception as e:
                                st.warning(f"Audio generation failed: {e}")
                        
                        # Download explanation
                        utils.create_download_button(
                            explanation, 
                            f"{concept.lower().replace(' ', '_')}_explanation.txt", 
                            "📥 Download Explanation"
                        )
                        
                        # Log interaction
                        utils.log_interaction("concept_explanation", {
                            "concept": concept,
                            "explanation_length": len(explanation),
                            "language": st.session_state.current_language
                        })
                    else:
                        st.error("❌ Could not generate explanation. Please try again.")
    
    with col2:
        st.subheader("Example Concepts")
        example_concepts = [
            "Photosynthesis",
            "Gravity",
            "Democracy", 
            "Climate Change",
            "Fractions",
            "Electricity",
            "Evolution",
            "The Water Cycle"
        ]
        
        for concept in example_concepts:
            if st.button(f"💡 {concept}", key=f"concept_{concept}"):
                st.session_state.example_concept = concept
                st.rerun()

def about_tab():
    """About and help information"""
    st.header("ℹ️ About")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🤖 AI Educational Assistant (Cloud Version)
        
        This cloud-optimized version is designed for easy deployment and accessibility:
        
        - **📷 Textbook Analysis**: Extract and summarize textbook content
        - **💬 Text Q&A**: Ask questions and get instant answers  
        - **📖 Concept Explanation**: Get clear explanations of complex topics
        - **🌍 Multi-language Support**: Works in multiple languages
        - **🔊 Online Audio Output**: Hear responses spoken back to you
        
        ### 🛠️ Technology Stack
        
        - **AI Model**: Google Gemma 3n for text generation
        - **OCR**: Tesseract for text extraction from images
        - **Text-to-Speech**: gTTS for online audio output
        - **Web Interface**: Streamlit for beautiful UI
        
        ### 🎯 Educational Focus
        
        All responses are tailored for students, with:
        - Age-appropriate language (12-year-old level)
        - Clear explanations with examples
        - Educational accuracy
        - Multiple language support
        
        ### ☁️ Cloud Deployment
        
        This version is optimized for free cloud deployment on:
        - Streamlit Cloud
        - Hugging Face Spaces
        - Railway
        - Heroku
        """)
    
    with col2:
        st.subheader("📊 Usage Statistics")
        
        # Display interaction logs
        logs = utils.load_session_data("interaction_logs", [])
        if logs:
            st.metric("Total Interactions", len(logs))
            
            # Count interaction types
            interaction_types = {}
            for log in logs:
                interaction_type = log.get('type', 'unknown')
                interaction_types[interaction_type] = interaction_types.get(interaction_type, 0) + 1
            
            for interaction_type, count in interaction_types.items():
                st.metric(interaction_type.replace('_', ' ').title(), count)
        else:
            st.info("No interactions recorded yet")
        
        # Model status
        if st.session_state.model_loaded:
            model_info = st.session_state.ai_engine.get_model_info()
            utils.create_model_status_display(model_info)

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    main_header()
    
    # Sidebar
    sidebar_settings()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📷 Textbook Analysis", 
        "💬 Text Q&A", 
        "📖 Concept Explanation",
        "ℹ️ About"
    ])
    
    with tab1:
        textbook_analysis_tab()
    
    with tab2:
        text_qa_tab()
    
    with tab3:
        concept_explanation_tab()
    
    with tab4:
        about_tab()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ for students everywhere | "
        "Powered by Google Gemma 3n | "
        "Cloud Optimized"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()