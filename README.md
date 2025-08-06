# 🤖 AI Educational Assistant

An intelligent educational assistant powered by Google Gemma that helps students learn through multiple modalities:

- 📷 **Textbook Image Analysis**: Extract and summarize textbook content
- 💬 **Text Q&A**: Ask questions and get instant answers
- 📖 **Concept Explanation**: Get clear explanations of complex topics
- 🌍 **Multi-language Support**: Works in multiple languages
- 🔊 **Audio Output**: Hear responses spoken back to you

## ✨ Features

### 📷 Textbook Image → Summary
- Upload images of textbook pages
- OCR text extraction using Tesseract
- AI-powered summarization for 12-year-old comprehension level
- Clean, easy-to-understand explanations

### 💬 Text Q&A
- Type educational questions
- Get instant AI-powered answers
- Context-aware responses suitable for students
- Optional text-to-speech output

### 📖 Concept Explanation
- Enter any educational concept
- Get student-friendly explanations
- Examples and analogies included
- Download explanations as text files

### 🌍 Multi-language Support
- English, Spanish, French, German
- Automatic language detection
- AI-powered translation
- Multi-language audio output

## 🚀 Quick Deploy

### Free Cloud Deployment Options

#### Option 1: Streamlit Cloud (Recommended) ⭐
1. **Rename files**:
   ```bash
   mv app_cloud.py app.py
   mv requirements_cloud.txt requirements.txt
   ```

2. **Deploy**:
   - Go to: https://share.streamlit.io/
   - Sign in with GitHub
   - Connect your repository
   - Deploy in 2 minutes!

#### Option 2: Hugging Face Spaces
1. Create a new Space on Hugging Face
2. Upload all project files
3. Deploy automatically

#### Option 3: Railway
1. Connect your GitHub repository
2. Auto-deploy with Procfile
3. Free tier available

## 🏗️ Project Structure

```
ai-educational-assistant/
├── app_cloud.py              # Main Streamlit application
├── requirements_cloud.txt    # Python dependencies
├── packages.txt              # System dependencies (Tesseract)
├── ocr_processor.py          # OCR and image processing
├── ai_engine.py              # AI model integration
├── utils.py                  # Utility functions
├── Procfile                  # Railway deployment
├── runtime.txt               # Python version
├── .streamlit/config.toml    # Streamlit configuration
├── DEPLOYMENT_GUIDE.md       # Deployment instructions
└── README.md                 # This file
```

## 🔧 Technical Details

### AI Models Used
- **Google Gemma 3n**: For text generation and summarization
- **Tesseract OCR**: For text extraction from images
- **gTTS**: For online text-to-speech

### Key Technologies
- **Streamlit**: Web interface
- **Transformers**: HuggingFace model loading
- **OpenCV**: Image processing
- **PyTorch**: Deep learning framework

## 🎯 Usage

1. **Textbook Analysis**:
   - Upload an image of a textbook page
   - Click "Analyze Image"
   - Get a student-friendly summary

2. **Text Q&A**:
   - Type your question
   - Click "Get Answer"
   - Get instant AI response

3. **Concept Explanation**:
   - Enter a concept to explain
   - Get clear, educational explanation
   - Download as text file

4. **Language Settings**:
   - Select your preferred language
   - Enable/disable audio output
   - Choose voice settings

## 💰 Cost

**FREE Forever!**
- No credit card required
- No hidden fees
- Works on free cloud platforms

## 🎉 Benefits

- **Accessible**: Works on any device with internet
- **Educational**: Designed specifically for students
- **Multi-modal**: Text, images, and audio
- **Multi-language**: Global accessibility
- **Free**: No cost to use or deploy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google for Gemma 3n
- HuggingFace for transformers
- Tesseract OCR team
- Streamlit for the web framework

---

**Built with ❤️ for students everywhere** 