import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Optional, Dict, Any
import time

class AIEngine:
    """Handles AI model operations with Gemma 3n for educational content"""
    
    def __init__(self):
        """Initialize AI engine with model settings"""
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_loaded = False
        
        # Model configuration
        self.model_name = "google/gemma-2-9b-it"  # Using Gemma 2 9B as fallback
        self.max_length = 2048
        self.temperature = 0.7
        self.top_p = 0.9
        
        # Educational prompts
        self.prompts = {
            'summarize': {
                'en': "You are a helpful educational assistant. Summarize the following textbook content in simple terms that a 12-year-old student can understand. Focus on the main concepts and explain them clearly:\n\n{text}\n\nSummary:",
                'es': "Eres un asistente educativo útil. Resume el siguiente contenido del libro de texto en términos simples que un estudiante de 12 años pueda entender. Enfócate en los conceptos principales y explícalos claramente:\n\n{text}\n\nResumen:",
                'fr': "Vous êtes un assistant éducatif utile. Résumez le contenu suivant du manuel en termes simples qu'un étudiant de 12 ans peut comprendre. Concentrez-vous sur les concepts principaux et expliquez-les clairement:\n\n{text}\n\nRésumé:",
                'de': "Sie sind ein hilfreicher Bildungsassistent. Fassen Sie den folgenden Lehrbuchinhalt in einfachen Begriffen zusammen, die ein 12-jähriger Schüler verstehen kann. Konzentrieren Sie sich auf die Hauptkonzepte und erklären Sie sie klar:\n\n{text}\n\nZusammenfassung:"
            },
            'answer_question': {
                'en': "You are a helpful educational assistant. Answer the following question in a way that a school student can understand. Provide a clear, accurate, and educational response:\n\nQuestion: {question}\n\nAnswer:",
                'es': "Eres un asistente educativo útil. Responde la siguiente pregunta de una manera que un estudiante escolar pueda entender. Proporciona una respuesta clara, precisa y educativa:\n\nPregunta: {question}\n\nRespuesta:",
                'fr': "Vous êtes un assistant éducatif utile. Répondez à la question suivante d'une manière qu'un étudiant peut comprendre. Fournissez une réponse claire, précise et éducative:\n\nQuestion: {question}\n\nRéponse:",
                'de': "Sie sind ein hilfreicher Bildungsassistent. Beantworten Sie die folgende Frage so, dass ein Schüler sie verstehen kann. Geben Sie eine klare, genaue und lehrreiche Antwort:\n\nFrage: {question}\n\nAntwort:"
            },
            'explain_concept': {
                'en': "You are a helpful educational assistant. Explain the following concept in simple terms that a student can understand. Use examples and analogies if helpful:\n\nConcept: {concept}\n\nExplanation:",
                'es': "Eres un asistente educativo útil. Explica el siguiente concepto en términos simples que un estudiante pueda entender. Usa ejemplos y analogías si es útil:\n\nConcepto: {concept}\n\nExplicación:",
                'fr': "Vous êtes un assistant éducatif utile. Expliquez le concept suivant en termes simples qu'un étudiant peut comprendre. Utilisez des exemples et des analogies si c'est utile:\n\nConcept: {concept}\n\nExplication:",
                'de': "Sie sind ein hilfreicher Bildungsassistent. Erklären Sie das folgende Konzept in einfachen Begriffen, die ein Schüler verstehen kann. Verwenden Sie Beispiele und Analogien, wenn es hilfreich ist:\n\nKonzept: {concept}\n\nErklärung:"
            }
        }
    
    def load_model(self, model_name: Optional[str] = None) -> bool:
        """
        Load the AI model and tokenizer
        
        Args:
            model_name: Optional custom model name
            
        Returns:
            True if model loaded successfully, False otherwise
        """
        if model_name:
            self.model_name = model_name
            
        try:
            with st.spinner("Loading AI model... This may take a few minutes."):
                # Load tokenizer
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name,
                    trust_remote_code=True
                )
                
                # Load model
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None,
                    trust_remote_code=True
                )
                
                # Set pad token if not present
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
                self.model_loaded = True
                st.success("AI model loaded successfully!")
                return True
                
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            st.info("Trying to load a smaller model...")
            
            # Fallback to a smaller model
            try:
                fallback_model = "microsoft/DialoGPT-medium"
                with st.spinner("Loading fallback model..."):
                    self.tokenizer = AutoTokenizer.from_pretrained(fallback_model)
                    self.model = AutoModelForCausalLM.from_pretrained(fallback_model)
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                    self.model_loaded = True
                    st.success("Fallback model loaded successfully!")
                    return True
            except Exception as e2:
                st.error(f"Error loading fallback model: {str(e2)}")
                return False
    
    def generate_response(self, prompt: str, max_length: Optional[int] = None) -> str:
        """
        Generate response using the loaded model
        
        Args:
            prompt: Input prompt for the model
            max_length: Maximum length of generated response
            
        Returns:
            Generated response text
        """
        if not self.model_loaded:
            st.error("Model not loaded. Please load the model first.")
            return ""
        
        try:
            with st.spinner("Generating response..."):
                # Tokenize input
                inputs = self.tokenizer.encode(
                    prompt, 
                    return_tensors="pt",
                    truncation=True,
                    max_length=self.max_length
                )
                
                # Move to device
                if self.device == "cuda":
                    inputs = inputs.to(self.device)
                
                # Generate response
                with torch.no_grad():
                    outputs = self.model.generate(
                        inputs,
                        max_length=max_length or self.max_length,
                        temperature=self.temperature,
                        top_p=self.top_p,
                        do_sample=True,
                        pad_token_id=self.tokenizer.eos_token_id,
                        eos_token_id=self.tokenizer.eos_token_id
                    )
                
                # Decode response
                response = self.tokenizer.decode(
                    outputs[0], 
                    skip_special_tokens=True
                )
                
                # Extract only the generated part (remove input prompt)
                generated_text = response[len(prompt):].strip()
                
                return generated_text
                
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return ""
    
    def summarize_text(self, text: str, language: str = 'en') -> str:
        """
        Summarize text content for educational purposes
        
        Args:
            text: Text to summarize
            language: Language code for the prompt
            
        Returns:
            Summarized text
        """
        if not text.strip():
            return "No text provided for summarization."
        
        # Get appropriate prompt
        prompt_template = self.prompts['summarize'].get(language, self.prompts['summarize']['en'])
        prompt = prompt_template.format(text=text)
        
        # Generate summary
        summary = self.generate_response(prompt, max_length=500)
        
        if not summary:
            return "Unable to generate summary at this time."
        
        return summary
    
    def answer_question(self, question: str, language: str = 'en') -> str:
        """
        Answer educational questions
        
        Args:
            question: Question to answer
            language: Language code for the prompt
            
        Returns:
            Answer to the question
        """
        if not question.strip():
            return "No question provided."
        
        # Get appropriate prompt
        prompt_template = self.prompts['answer_question'].get(language, self.prompts['answer_question']['en'])
        prompt = prompt_template.format(question=question)
        
        # Generate answer
        answer = self.generate_response(prompt, max_length=800)
        
        if not answer:
            return "Unable to generate answer at this time."
        
        return answer
    
    def explain_concept(self, concept: str, language: str = 'en') -> str:
        """
        Explain educational concepts
        
        Args:
            concept: Concept to explain
            language: Language code for the prompt
            
        Returns:
            Explanation of the concept
        """
        if not concept.strip():
            return "No concept provided for explanation."
        
        # Get appropriate prompt
        prompt_template = self.prompts['explain_concept'].get(language, self.prompts['explain_concept']['en'])
        prompt = prompt_template.format(concept=concept)
        
        # Generate explanation
        explanation = self.generate_response(prompt, max_length=600)
        
        if not explanation:
            return "Unable to generate explanation at this time."
        
        return explanation
    
    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translate text to target language (basic implementation)
        
        Args:
            text: Text to translate
            target_language: Target language code
            
        Returns:
            Translated text
        """
        if not text.strip():
            return ""
        
        # Simple translation prompt
        translation_prompts = {
            'es': f"Translate the following text to Spanish:\n\n{text}\n\nTranslation:",
            'fr': f"Translate the following text to French:\n\n{text}\n\nTranslation:",
            'de': f"Translate the following text to German:\n\n{text}\n\nTranslation:",
            'en': f"Translate the following text to English:\n\n{text}\n\nTranslation:"
        }
        
        prompt = translation_prompts.get(target_language, translation_prompts['en'])
        translation = self.generate_response(prompt, max_length=400)
        
        return translation if translation else text
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model
        
        Returns:
            Dictionary with model information
        """
        if not self.model_loaded:
            return {"status": "Not loaded"}
        
        return {
            "model_name": self.model_name,
            "device": self.device,
            "max_length": self.max_length,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "status": "Loaded"
        }
    
    def update_settings(self, temperature: float = None, top_p: float = None, max_length: int = None):
        """
        Update model generation settings
        
        Args:
            temperature: New temperature value
            top_p: New top_p value
            max_length: New max_length value
        """
        if temperature is not None:
            self.temperature = max(0.1, min(2.0, temperature))
        if top_p is not None:
            self.top_p = max(0.1, min(1.0, top_p))
        if max_length is not None:
            self.max_length = max(100, min(4096, max_length)) 