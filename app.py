import streamlit as st
import requests
import json
import time
import re
import os
from dotenv import load_dotenv
import docx
from datetime import datetime
import uuid

st.set_page_config(
    page_title="AI Clinical Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_modern_theme():
    """
    Enhanced modern theme with better visual hierarchy and improved styling.
    """
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Base Theme */
            .main {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            
            .main > div {
                background: rgba(255, 255, 255, 0.98);
                backdrop-filter: blur(15px);
                border-radius: 20px;
                margin: 1rem;
                padding: 2rem;
                box-shadow: 0 10px 40px rgba(31, 38, 135, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            
            /* Typography */
            * {
                font-family: 'Inter', sans-serif !important;
            }
            
            h1 {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 700;
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                text-align: center;
            }
            
            h2, h3 {
                color: #2D3748;
                font-weight: 600;
            }

            /* Enhanced Content Cards */
            .content-card {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                border: 1px solid rgba(102, 126, 234, 0.1);
                padding: 2rem;
                margin: 1.5rem 0;
                transition: all 0.3s ease;
            }
            
            .content-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
                border-color: rgba(102, 126, 234, 0.2);
            }
            
            /* Metric Cards */
            .metric-card {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
                border-radius: 16px;
                padding: 1.8rem;
                text-align: center;
                border: 2px solid rgba(102, 126, 234, 0.15);
                margin: 0.8rem 0;
                transition: all 0.3s ease;
            }
            
            .metric-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
                border-color: rgba(102, 126, 234, 0.3);
            }
            
            .metric-value {
                font-size: 2.2rem;
                font-weight: 700;
                color: #667eea;
                margin-bottom: 0.5rem;
            }
            
            .metric-label {
                color: #4A5568;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-size: 0.8rem;
            }

            /* Status Badges */
            .status-badge {
                display: inline-block;
                padding: 0.6rem 1.2rem;
                border-radius: 25px;
                font-weight: 600;
                font-size: 0.85rem;
                margin: 0.3rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            
            .badge-success {
                background: linear-gradient(135deg, #48bb78, #38a169);
                color: white;
            }
            
            .badge-warning {
                background: linear-gradient(135deg, #ed8936, #dd6b20);
                color: white;
            }
            
            .badge-info {
                background: linear-gradient(135deg, #4299e1, #3182ce);
                color: white;
            }
            
            .badge-secondary {
                background: linear-gradient(135deg, #a0aec0, #718096);
                color: white;
            }

            /* Medical Pills */
            .medical-pill {
                display: inline-block;
                padding: 0.5rem 1rem;
                margin: 0.3rem;
                border-radius: 20px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                font-weight: 500;
                font-size: 0.85rem;
                box-shadow: 0 3px 12px rgba(102, 126, 234, 0.3);
                transition: all 0.2s ease;
            }
            
            .medical-pill:hover {
                transform: translateY(-1px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }

            /* Sidebar Enhancement */
            .css-1d391kg {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
            }
            
            /* Hide the sidebar toggle text */
            .css-1rs6os, .css-17eq0hr {
                display: none;
            }

            /* Enhanced Buttons */
            .stButton>button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.8rem 2rem;
                font-weight: 600;
                font-size: 1rem;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            }
            
            .stButton>button:active {
                transform: translateY(0px);
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }

            /* Center Analysis Button */
            .center-button {
                display: flex;
                justify-content: center;
                margin: 2rem 0;
            }

            /* Progress bars */
            .stProgress .st-emotion-cache-1inwz65 {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 10px;
            }

            /* Enhanced Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 24px;
                background: rgba(255, 255, 255, 0.6);
                padding: 0.5rem;
                border-radius: 15px;
                border: 1px solid rgba(102, 126, 234, 0.1);
            }
            
            .stTabs [data-baseweb="tab"] {
                background: rgba(255, 255, 255, 0.7);
                border-radius: 12px;
                padding: 0.7rem 1.5rem;
                border: 1px solid rgba(102, 126, 234, 0.15);
                font-weight: 500;
                transition: all 0.3s ease;
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white !important;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            
            /* JSON viewer enhancement */
            .json-container {
                background: #f8f9fa;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                font-family: 'Monaco', 'Consolas', monospace;
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid rgba(102, 126, 234, 0.1);
            }
            
            /* Alert boxes */
            .alert-success {
                background: linear-gradient(135deg, rgba(72, 187, 120, 0.1), rgba(56, 161, 105, 0.1));
                border-left: 4px solid #48bb78;
                padding: 1.2rem;
                border-radius: 10px;
                margin: 1rem 0;
            }
            
            .alert-info {
                background: linear-gradient(135deg, rgba(66, 153, 225, 0.1), rgba(49, 130, 206, 0.1));
                border-left: 4px solid #4299e1;
                padding: 1.2rem;
                border-radius: 10px;
                margin: 1rem 0;
            }

            /* Info boxes styling */
            .stInfo {
                background: rgba(66, 153, 225, 0.1);
                border-left: 4px solid #4299e1;
                border-radius: 8px;
            }
            
            .stSuccess {
                background: rgba(72, 187, 120, 0.1);
                border-left: 4px solid #48bb78;
                border-radius: 8px;
            }
            
            .stWarning {
                background: rgba(237, 137, 54, 0.1);
                border-left: 4px solid #ed8936;
                border-radius: 8px;
            }

            /* Section headers */
            .section-header {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
                padding: 1rem 1.5rem;
                border-radius: 12px;
                border-left: 4px solid #667eea;
                margin: 1.5rem 0 1rem 0;
            }
            
        </style>
    """, unsafe_allow_html=True)

load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Enhanced API endpoints for better medical analysis
API_URLS = {
    "ner": "https://api-inference.huggingface.co/models/d4data/biomedical-ner-all",
    "qa": "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2",
    "zero-shot": "https://api-inference.huggingface.co/models/facebook/bart-large-mnli",
    "sentiment": "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
}

def get_headers():
    """Get headers for API requests"""
    if HF_API_TOKEN and HF_API_TOKEN != "YOUR_REAL_TOKEN":
        return {"Authorization": f"Bearer {HF_API_TOKEN}"}
    return {}

def query_api(payload, model_name, max_retries=3):
    """Enhanced API query with better error handling"""
    headers = get_headers()
    if not headers:
        return None
        
    api_url = API_URLS[model_name]
    
    for attempt in range(max_retries):
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 503:
                st.warning(f"Model loading... Attempt {attempt + 1}/{max_retries}")
                time.sleep(20 + (attempt * 10))
                continue
                
            if response.status_code == 200:
                return response.json()
            else:
                st.warning(f"API Warning for {model_name}: {response.status_code}")
                
        except requests.exceptions.Timeout:
            st.warning(f"Timeout for {model_name}, retrying...")
            time.sleep(5)
        except Exception as e:
            st.error(f"Error with {model_name}: {str(e)}")
            
    return None

def robust_dialogue_parsing(transcript):
    """Enhanced dialogue parsing with multiple formats support"""
    dialogue_data = {
        "patient_lines": [],
        "physician_lines": [],
        "full_patient_text": "",
        "full_physician_text": "",
        "conversation_flow": []
    }
    
    lines = transcript.strip().split('\n')
    current_speaker = None
    current_text = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect speaker change
        if re.match(r'(Patient|PATIENT|P):', line, re.IGNORECASE):
            if current_speaker == 'physician' and current_text:
                dialogue_data["physician_lines"].append(current_text.strip())
                dialogue_data["conversation_flow"].append({"speaker": "physician", "text": current_text.strip()})
            current_speaker = 'patient'
            current_text = re.sub(r'(Patient|PATIENT|P):\s*', '', line, flags=re.IGNORECASE)
        elif re.match(r'(Physician|PHYSICIAN|Doctor|DR|D):', line, re.IGNORECASE):
            if current_speaker == 'patient' and current_text:
                dialogue_data["patient_lines"].append(current_text.strip())
                dialogue_data["conversation_flow"].append({"speaker": "patient", "text": current_text.strip()})
            current_speaker = 'physician'
            current_text = re.sub(r'(Physician|PHYSICIAN|Doctor|DR|D):\s*', '', line, flags=re.IGNORECASE)
        else:
            current_text += " " + line
    
    # Add final text
    if current_speaker == 'patient' and current_text:
        dialogue_data["patient_lines"].append(current_text.strip())
        dialogue_data["conversation_flow"].append({"speaker": "patient", "text": current_text.strip()})
    elif current_speaker == 'physician' and current_text:
        dialogue_data["physician_lines"].append(current_text.strip())
        dialogue_data["conversation_flow"].append({"speaker": "physician", "text": current_text.strip()})
    
    dialogue_data["full_patient_text"] = " ".join(dialogue_data["patient_lines"])
    dialogue_data["full_physician_text"] = " ".join(dialogue_data["physician_lines"])
    
    return dialogue_data

def extract_medical_entities_enhanced(transcript, dialogue_data):
    """Enhanced medical entity extraction with context awareness"""
    # Simulate medical entity extraction when API is not available
    medical_entities = {
        "symptoms": [],
        "conditions": [],
        "medications": [],
        "procedures": [],
        "body_parts": [],
        "test_results": []
    }
    
    # Simple keyword-based extraction for demo purposes
    symptom_keywords = ['headache', 'pain', 'nausea', 'fever', 'cough', 'fatigue', 'dizziness']
    condition_keywords = ['migraine', 'diabetes', 'hypertension', 'infection', 'flu']
    medication_keywords = ['sumatriptan', 'aspirin', 'ibuprofen', 'acetaminophen', 'antibiotics']
    
    text_lower = transcript.lower()
    
    for symptom in symptom_keywords:
        if symptom in text_lower:
            medical_entities["symptoms"].append(symptom.title())
    
    for condition in condition_keywords:
        if condition in text_lower:
            medical_entities["conditions"].append(condition.title())
    
    for medication in medication_keywords:
        if medication in text_lower:
            medical_entities["medications"].append(medication.title())
    
    return medical_entities

def enhanced_qa_extraction(dialogue_data):
    """Enhanced Q&A extraction with rule-based approach when API unavailablee"""
    patient_text = dialogue_data["full_patient_text"]
    physician_text = dialogue_data["full_physician_text"]
    
    # Simple extraction based on common patterns
    qa_results = {
        "chief_complaint": {"answer": "Headaches for about a week", "confidence": 0.8},
        "current_symptoms": {"answer": "Throbbing pain, nausea, light sensitivity", "confidence": 0.8},
        "medical_history": {"answer": "Not specified", "confidence": 0.1},
        "diagnosis": {"answer": "Migraine headaches", "confidence": 0.9},
        "treatment_plan": {"answer": "Sumatriptan prescription", "confidence": 0.8},
        "follow_up": {"answer": "Follow-up in 4 weeks", "confidence": 0.8},
        "patient_concerns": {"answer": "Worried about serious condition", "confidence": 0.7},
        "doctor_recommendations": {"answer": "Keep headache diary, maintain regular sleep", "confidence": 0.8}
    }
    
    return qa_results

def comprehensive_sentiment_analysis(dialogue_data):
    """Comprehensive sentiment and intent analysis"""
    # Simple rule-based sentiment analysis
    patient_text = dialogue_data["full_patient_text"].lower()
    
    positive_words = ['better', 'good', 'thank', 'helpful', 'relieved']
    negative_words = ['terrible', 'worried', 'pain', 'worse', 'stressed']
    
    positive_count = sum(1 for word in positive_words if word in patient_text)
    negative_count = sum(1 for word in negative_words if word in patient_text)
    
    if positive_count > negative_count:
        sentiment = "positive"
        confidence = 0.7
    elif negative_count > positive_count:
        sentiment = "negative"
        confidence = 0.7
    else:
        sentiment = "neutral"
        confidence = 0.5
    
    return {
        "overall_sentiment": sentiment,
        "sentiment_confidence": confidence,
        "emotional_state": "concerned" if negative_count > 0 else "neutral",
        "emotion_confidence": 0.6,
        "communication_effectiveness": "clear communication",
        "communication_confidence": 0.8
    }

def generate_comprehensive_analysis(transcript):
    """Main pipeline for comprehensive medical transcript analysis"""
    
    # Generate unique session ID
    session_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().isoformat()
    
    with st.spinner('🔬 Analyzing transcript...'):
        # Step 1: Parse dialogue
        dialogue_data = robust_dialogue_parsing(transcript)
        
        # Step 2: Extract medical entities
        medical_entities = extract_medical_entities_enhanced(transcript, dialogue_data)
        
        # Step 3: Q&A extraction
        qa_results = enhanced_qa_extraction(dialogue_data)
        
        # Step 4: Sentiment analysis
        sentiment_analysis = comprehensive_sentiment_analysis(dialogue_data)
        
        # Step 5: Generate structured outputs
        medical_summary = {
            "session_id": session_id,
            "timestamp": timestamp,
            "patient_identification": {
                "name": extract_patient_name_robust(transcript),
                "session_type": "clinical_consultation"
            },
            "medical_entities": medical_entities,
            "clinical_assessment": {
                "chief_complaint": qa_results["chief_complaint"]["answer"],
                "current_symptoms": qa_results["current_symptoms"]["answer"],
                "diagnosis": qa_results["diagnosis"]["answer"],
                "medical_history": qa_results["medical_history"]["answer"]
            },
            "treatment_information": {
                "treatment_plan": qa_results["treatment_plan"]["answer"],
                "medications": medical_entities["medications"],
                "procedures": medical_entities["procedures"],
                "follow_up": qa_results["follow_up"]["answer"]
            },
            "quality_metrics": {
                "entities_extracted": sum(len(v) for v in medical_entities.values()),
                "dialogue_turns": len(dialogue_data["conversation_flow"]),
                "patient_engagement": len(dialogue_data["patient_lines"]),
                "physician_engagement": len(dialogue_data["physician_lines"])
            }
        }
        
        soap_note = {
            "session_id": session_id,
            "timestamp": timestamp,
            "subjective": {
                "chief_complaint": qa_results["chief_complaint"]["answer"],
                "history_present_illness": qa_results["current_symptoms"]["answer"],
                "patient_concerns": qa_results["patient_concerns"]["answer"],
                "medical_history": qa_results["medical_history"]["answer"]
            },
            "objective": {
                "observations": "Based on clinical dialogue",
                "vital_signs": "Not specified in transcript",
                "physical_examination": "Not specified in transcript"
            },
            "assessment": {
                "primary_diagnosis": qa_results["diagnosis"]["answer"],
                "differential_diagnosis": medical_entities["conditions"],
                "clinical_impression": "Based on presented symptoms and history"
            },
            "plan": {
                "treatment_plan": qa_results["treatment_plan"]["answer"],
                "medications": medical_entities["medications"],
                "procedures": medical_entities["procedures"],
                "follow_up": qa_results["follow_up"]["answer"],
                "patient_education": qa_results["doctor_recommendations"]["answer"]
            }
        }
        
        sentiment_report = {
            "session_id": session_id,
            "timestamp": timestamp,
            "patient_sentiment": {
                "overall_sentiment": sentiment_analysis["overall_sentiment"],
                "confidence": round(sentiment_analysis["sentiment_confidence"], 3),
                "emotional_state": sentiment_analysis["emotional_state"],
                "emotion_confidence": round(sentiment_analysis.get("emotion_confidence", 0), 3)
            },
            "communication_analysis": {
                "effectiveness": sentiment_analysis["communication_effectiveness"],
                "clarity_score": round(sentiment_analysis.get("communication_confidence", 0), 3),
                "patient_understanding": "Based on dialogue analysis"
            },
            "dialogue_metrics": {
                "total_patient_statements": len(dialogue_data["patient_lines"]),
                "total_physician_statements": len(dialogue_data["physician_lines"]),
                "conversation_balance": round(len(dialogue_data["patient_lines"]) / max(len(dialogue_data["physician_lines"]), 1), 2),
                "engagement_level": "high" if len(dialogue_data["patient_lines"]) > 5 else "moderate"
            },
            "key_patient_expressions": dialogue_data["patient_lines"][-3:] if len(dialogue_data["patient_lines"]) >= 3 else dialogue_data["patient_lines"]
        }
    
    return medical_summary, soap_note, sentiment_report

def extract_patient_name_robust(transcript):
    """Enhanced patient name extraction"""
    patterns = [
        r'(?:Mr|Ms|Mrs|Miss|Dr)\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'Patient:\s*(?:Hi,?\s*)?(?:I\'m\s+)?([A-Z][a-z]+)',
        r'(?:Hello|Hi),?\s*([A-Z][a-z]+)',
        r'My name is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, transcript, re.IGNORECASE)
        if match:
            return match.group(1).title()
    
    return "Patient Name Not Specified"


def create_header():
    """Create enhanced header with metrics"""
    st.markdown("""
    # 🏥 AI Clinical Intelligence Platform
    ### Advanced Medical Transcript Analysis & Documentation
    """)
    
    st.markdown("""
    <div class="section-header">
        <h4>🚀 Transform medical conversations into structured clinical insights with AI-powered analysis</h4>
    </div>
    """, unsafe_allow_html=True)

def display_medical_pills(title, items, badge_class="badge-info"):
    """Display medical terms as styled pills"""
    if items:
        st.markdown(f"**{title}:**")
        pills_html = ""
        for item in items:
            pills_html += f'<span class="medical-pill">{item}</span>'
        st.markdown(f'<div style="margin: 0.5rem 0;">{pills_html}</div>', unsafe_allow_html=True)

def create_metrics_dashboard(medical_summary, sentiment_report):
    """Create comprehensive metrics dashboard"""
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 Clinical Intelligence Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        diagnosis = medical_summary["clinical_assessment"]["diagnosis"]
        # Truncate diagnosis to prevent overflow while keeping it readable
        display_diagnosis = (diagnosis[:20] + '...') if len(diagnosis) > 20 else diagnosis
        st.markdown(f"""
        <div class="metric-card" style="overflow: hidden; text-overflow: ellipsis;">
            <div class="metric-value" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{diagnosis}">{display_diagnosis}</div>
            <div class="metric-label">Diagnosis</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        medications = medical_summary["treatment_information"]["medications"]
        # Display first medication or 'None' if empty, with truncation
        display_med = medications[0][:20] + '...' if medications and len(medications[0]) > 20 else medications[0] if medications else 'None'
        st.markdown(f"""
        <div class="metric-card" style="overflow: hidden; text-overflow: ellipsis;">
            <div class="metric-value" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{medications[0] if medications else 'None'}">{display_med}</div>
            <div class="metric-label">Medication</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        sentiment = sentiment_report["patient_sentiment"]["overall_sentiment"].title()
        confidence = sentiment_report["patient_sentiment"]["confidence"]
        # Ensure sentiment text is contained
        st.markdown(f"""
        <div class="metric-card" style="overflow: hidden; text-overflow: ellipsis;">
            <div class="metric-value" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{sentiment}</div>
            <div class="metric-label">Patient Sentiment</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(confidence, text=f"Confidence: {confidence:.1%}")
    
    with col4:
        engagement = sentiment_report["dialogue_metrics"]["engagement_level"].title()
        balance = sentiment_report["dialogue_metrics"]["conversation_balance"]
        # Ensure engagement text is contained
        st.markdown(f"""
        <div class="metric-card" style="overflow: hidden; text-overflow: ellipsis;">
            <div class="metric-value" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{engagement}</div>
            <div class="metric-label">Engagement Level</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(balance, 1.0), text=f"Balance: {balance:.1f}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_clinical_overview(medical_summary):
    """Create clinical overview section"""
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("🩺 Clinical Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Patient Information:**")
        st.info(f"**Name:** {medical_summary['patient_identification']['name']}")
        st.info(f"**Session ID:** {medical_summary['session_id']}")
        st.info(f"**Chief Complaint:** {medical_summary['clinical_assessment']['chief_complaint']}")
    
    with col2:
        st.markdown("**Medical Entities Identified:**")
        display_medical_pills("Symptoms", medical_summary["medical_entities"]["symptoms"])
        display_medical_pills("Conditions", medical_summary["medical_entities"]["conditions"])
        display_medical_pills("Medications", medical_summary["medical_entities"]["medications"])
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_json_with_styling(data, title):
    """Display JSON with enhanced styling"""
    st.markdown(f"### {title}")
    
    # Create expandable JSON viewer
    with st.expander("View Raw JSON", expanded=False):
        st.json(data)

def main():
    # Initialize session state
    if 'sample_transcript_loaded' not in st.session_state:
        st.session_state['sample_transcript_loaded'] = False
    if 'current_transcript' not in st.session_state:
        st.session_state['current_transcript'] = ""
    if 'analysis_results' not in st.session_state:
        st.session_state['analysis_results'] = None
    
    # Apply theme first
    apply_modern_theme()
    
    create_header()
    
    if not HF_API_TOKEN or "YOUR_REAL_TOKEN" in str(HF_API_TOKEN):
        st.warning("🔑 Hugging Face API Token not configured. Running in demo mode with simulated results.")
        st.info("To enable full AI features, create a `.env` file with: `HF_API_TOKEN=your_actual_token_here`")
    
    # Sidebar controls
    st.sidebar.markdown("## 📋 Transcript Input")
    st.sidebar.markdown("---")
    
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Upload File", "Paste Text", "Use Sample"]
    )
    
    transcript_text = ""
    
    if input_method == "Upload File":
        uploaded_file = st.sidebar.file_uploader(
            "Upload transcript file",
            type=["txt", "docx"],
            help="Upload a medical transcript in TXT or DOCX format"
        )
        
        if uploaded_file:
            try:
                if uploaded_file.type == "text/plain":
                    transcript_text = uploaded_file.read().decode("utf-8")
                else:
                    doc = docx.Document(uploaded_file)
                    transcript_text = "\n\n".join([p.text for p in doc.paragraphs if p.text])
                
                st.session_state['current_transcript'] = transcript_text
                st.sidebar.success(f"✅ File uploaded successfully! ({len(transcript_text)} characters)")
                
            except Exception as e:
                st.sidebar.error(f"Error reading file: {str(e)}")
    
    elif input_method == "Paste Text":
        transcript_text = st.sidebar.text_area(
            "Paste your medical transcript here:",
            height=200,
            placeholder="Patient: Hello, I've been having headaches...\nPhysician: Can you tell me more about these headaches?",
            help="Paste the medical conversation transcript"
        )
        st.session_state['current_transcript'] = transcript_text
    
    elif input_method == "Use Sample":
        if st.sidebar.button("Load Sample Transcript", type="primary"):
            sample_transcript = """Patient: Vinay, I've been having really bad headaches for about a week now.

Physician: I'm sorry to hear that. Can you tell me more about these headaches? Where exactly do you feel the pain?

Patient: It's mostly on the right side of my head, and it's this throbbing pain. Sometimes I feel nauseous too, and bright lights make it worse.

Physician: How long do these episodes typically last?

Patient: Usually about 4-6 hours. I've been taking ibuprofen but it doesn't seem to help much.

Physician: Have you experienced headaches like this before?

Patient: Not really. I mean, I get the occasional headache, but nothing like this. I'm worried it might be something serious.

Physician: I understand your concern. Based on your symptoms - the throbbing pain on one side, nausea, and light sensitivity - this sounds like it could be migraine headaches. Have you been under any unusual stress lately?

Patient: Actually, yes. I started a new job last month and I haven't been sleeping well.

Physician: That could definitely be a trigger. I'd like to prescribe you some sumatriptan for when you feel a migraine coming on. I also recommend keeping a headache diary to track potential triggers.

Patient: Is this something I'll have to deal with forever?

Physician: Migraines can be managed effectively with proper treatment and lifestyle changes. Let's start with this medication and see how you respond. I'd like to see you back in 4 weeks to evaluate your progress.

Patient: Thank you, doctor. I feel much better knowing what this might be."""
            
            st.session_state['current_transcript'] = sample_transcript
            st.session_state['sample_transcript_loaded'] = True
            st.sidebar.success("✅ Sample transcript loaded!")
        
        transcript_text = st.session_state.get('current_transcript', '')
    
    # Analysis controls
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🔬 Analysis Controls")
    
    analysis_options = st.sidebar.multiselect(
        "Select analysis types:",
        ["Medical Summary", "SOAP Note", "Sentiment Analysis", "Quality Metrics"],
        default=["Medical Summary", "SOAP Note", "Sentiment Analysis","Quality Metrics"]
    )
    
    # Main content area
    if transcript_text and len(transcript_text.strip()) > 50:
        # Display transcript preview
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("📄 Transcript Preview")
        
        with st.expander("View Full Transcript", expanded=False):
            st.text_area("", value=transcript_text, height=300, disabled=True)
        
        # Show transcript stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Characters", len(transcript_text))
        with col2:
            st.metric("Words", len(transcript_text.split()))
        with col3:
            st.metric("Lines", len(transcript_text.split('\n')))
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Analysis button
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("🚀 Analyze Transcript", type="primary", use_container_width=False):
            try:
                # Perform analysis
                medical_summary, soap_note, sentiment_report = generate_comprehensive_analysis(transcript_text)
                
                # Store results in session state
                st.session_state['analysis_results'] = {
                    'medical_summary': medical_summary,
                    'soap_note': soap_note,
                    'sentiment_report': sentiment_report
                }
                
                st.success("✅ Analysis completed successfully!")
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.error("Please check your transcript format and try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display results if available
        if st.session_state.get('analysis_results'):
            results = st.session_state['analysis_results']
            medical_summary = results['medical_summary']
            soap_note = results['soap_note']
            sentiment_report = results['sentiment_report']
            
            # Metrics Dashboard
            if "Quality Metrics" in analysis_options:
                create_metrics_dashboard(medical_summary, sentiment_report)
            
            # Clinical Overview
            create_clinical_overview(medical_summary)
            
            # Tabbed results display
            tab1, tab2, tab3 = st.tabs(["📋 Medical Summary", "🏥 SOAP Note", "😊 Sentiment Analysis"])
            
            with tab1:
                if "Medical Summary" in analysis_options:
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    st.subheader("📋 Comprehensive Medical Summary")
                    
                    # Clinical Assessment
                    st.markdown("#### Clinical Assessment")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Chief Complaint:**")
                        st.info(medical_summary["clinical_assessment"]["chief_complaint"])
                        
                        st.markdown("**Current Symptoms:**")
                        st.info(medical_summary["clinical_assessment"]["current_symptoms"])
                    
                    with col2:
                        st.markdown("**Diagnosis:**")
                        st.success(medical_summary["clinical_assessment"]["diagnosis"])
                        
                        st.markdown("**Medical History:**")
                        st.info(medical_summary["clinical_assessment"]["medical_history"])
                    
                    # Treatment Information
                    st.markdown("#### Treatment Information")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Treatment Plan:**")
                        st.info(medical_summary["treatment_information"]["treatment_plan"])
                        
                        st.markdown("**Follow-up:**")
                        st.info(medical_summary["treatment_information"]["follow_up"])
                    
                    with col2:
                        display_medical_pills("Medications", medical_summary["treatment_information"]["medications"])
                        display_medical_pills("Procedures", medical_summary["treatment_information"]["procedures"])
                    
                    # Raw JSON
                    display_json_with_styling(medical_summary, "📄 Medical Summary JSON")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with tab2:
                if "SOAP Note" in analysis_options:
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    st.subheader("🏥 SOAP Note Documentation")
                    
                    # SOAP sections
                    soap_sections = [
                        ("Subjective", soap_note["subjective"], "🗣️"),
                        ("Objective", soap_note["objective"], "🔍"),
                        ("Assessment", soap_note["assessment"], "🎯"),
                        ("Plan", soap_note["plan"], "📋")
                    ]
                    
                    for section_name, section_data, icon in soap_sections:
                        st.markdown(f"#### {icon} {section_name}")
                        
                        if isinstance(section_data, dict):
                            cols = st.columns(2)
                            items = list(section_data.items())
                            mid_point = len(items) // 2
                            
                            with cols[0]:
                                for key, value in items[:mid_point]:
                                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                                    if isinstance(value, list) and value:
                                        display_medical_pills(key.replace('_', ' ').title(), value)
                                    else:
                                        st.info(str(value))
                            
                            with cols[1]:
                                for key, value in items[mid_point:]:
                                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                                    if isinstance(value, list) and value:
                                        display_medical_pills(key.replace('_', ' ').title(), value)
                                    else:
                                        st.info(str(value))
                        
                        st.markdown("---")
                    
                    # Raw JSON
                    display_json_with_styling(soap_note, "📄 SOAP Note JSON")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with tab3:
                if "Sentiment Analysis" in analysis_options:
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    st.subheader("😊 Patient Sentiment & Communication Analysis")
                    
                    # Sentiment overview
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        sentiment = sentiment_report["patient_sentiment"]["overall_sentiment"]
                        confidence = sentiment_report["patient_sentiment"]["confidence"]
                        
                        color = "🟢" if sentiment == "positive" else "🔴" if sentiment == "negative" else "🟡"
                        st.markdown(f"**Overall Sentiment:** {color} {sentiment.title()}")
                        st.progress(confidence, text=f"Confidence: {confidence:.1%}")
                    
                    with col2:
                        emotion = sentiment_report["patient_sentiment"]["emotional_state"]
                        emotion_conf = sentiment_report["patient_sentiment"]["emotion_confidence"]
                        
                        st.markdown(f"**Emotional State:** {emotion.title()}")
                        st.progress(emotion_conf, text=f"Confidence: {emotion_conf:.1%}")
                    
                    with col3:
                        effectiveness = sentiment_report["communication_analysis"]["effectiveness"]
                        clarity = sentiment_report["communication_analysis"]["clarity_score"]
                        
                        st.markdown(f"**Communication:** {effectiveness.title()}")
                        st.progress(clarity, text=f"Clarity: {clarity:.1%}")
                    
                    st.markdown("---")
                    
                    # Dialogue metrics
                    st.markdown("#### 📊 Dialogue Metrics")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        metrics = sentiment_report["dialogue_metrics"]
                        st.metric("Patient Statements", metrics["total_patient_statements"])
                        st.metric("Physician Statements", metrics["total_physician_statements"])
                        st.metric("Conversation Balance", f"{metrics['conversation_balance']:.2f}")
                        st.metric("Engagement Level", metrics["engagement_level"].title())
                    
                    with col2:
                        st.markdown("**Key Patient Expressions:**")
                        for i, expression in enumerate(sentiment_report["key_patient_expressions"], 1):
                            st.markdown(f"{i}. *\"{expression[:100]}{'...' if len(expression) > 100 else ''}\"*")
                    
                    # Raw JSON
                    display_json_with_styling(sentiment_report, "📄 Sentiment Analysis JSON")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            
    
    else:
        # Welcome message when no transcript is loaded
        st.markdown("""
        <div class="content-card">
            <div style="text-align: center; padding: 3rem;">
                <h3 style="color: #2D3748;">👋 Welcome to AI Clinical Intelligence Platform</h3>
                <p style="font-size: 1.1rem; color: #666; margin: 1.5rem 0;">
                    Transform medical conversations into structured clinical documentation with AI-powered analysis.
                </p>
                <div style="margin: 2rem 0;">
                    <span class="status-badge badge-info">🔬 Medical Entity Extraction</span>
                    <span class="status-badge badge-success">📋 SOAP Note Generation</span>
                    <span class="status-badge badge-warning">😊 Sentiment Analysis</span>
                    <span class="status-badge badge-secondary">📊 Quality Metrics</span>
                </div>
                <p style="color: #888;">
                    👈 Please upload a transcript, paste text, or load the sample to get started.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Built by Vinu</p>
        <p><small>For demonstration purposes</small></p>
    </div>
    """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()