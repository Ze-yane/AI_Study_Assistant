import streamlit as st
import os
import warnings
import logging

# Suppress GCP/gRPC warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
warnings.filterwarnings('ignore')
logging.getLogger("grpc").setLevel(logging.ERROR)
logging.getLogger("google.auth").setLevel(logging.ERROR)

from study import StudyAssistant
from budget import BudgetTracker
from cv_builder import CVBuilder

# Page config
st.set_page_config(
    page_title="ZinAI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Enhanced Design
st.markdown("""
    <style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hero section - LARGER */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 3rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
    }
    
    .hero h1 {
        font-size: 4rem;
        margin-bottom: 1rem;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    .hero p {
        font-size: 1.5rem;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Feature cards - BIGGER AND BOLDER */
    .feature-card {
        background: white;
        padding: 2.5rem;
        border-radius: 15px;
        border-left: 6px solid #667eea;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 48px rgba(102, 126, 234, 0.3);
    }
    
    .feature-card h3 {
        color: #667eea;
        margin-top: 0;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .feature-card p {
        font-size: 1.05rem;
        line-height: 1.8;
        color: #333;
    }
    
    /* Sidebar styling - ENHANCED */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e8eef7 100%);
        padding: 2rem 1.5rem;
    }
    
    /* Radio button styling */
    .stRadio > label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        margin: 0.5rem 0 !important;
        transition: all 0.2s ease !important;
    }
    
    .stRadio > label:hover {
        background-color: rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Button styling - LARGER */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
    }
    
    /* Headings */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #2d3748 !important;
        margin-bottom: 1.5rem !important;
    }
    
    h2 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #667eea !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #2d3748 !important;
    }
    
    /* Text styling */
    p, li {
        font-size: 1.05rem !important;
        line-height: 1.8 !important;
        color: #4a5568 !important;
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #667eea30;
    }
    
    /* Info box styling */
    .stAlert {
        padding: 1.5rem;
        font-size: 1.05rem;
        border-radius: 10px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar - navigation
with st.sidebar:
    page = st.radio(
        "Select a Tool:",
        ["🏠 Home", "📚 Study Assistant", "💰 Budget Tracker", "📄 CV Builder", "ℹ️ About"],
        label_visibility="collapsed"
    )

# Main content
if page == "🏠 Home":
    st.markdown("""
        <div class='hero'>
            <h1>🚀 ZinAI</h1>
            <p>Master your studies, manage your finances, and build your career</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Welcome! 👋")
    st.write("""
    Your all-in-one productivity platform. Choose a tool from the sidebar to get started:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='feature-card'>
            <h3>📚 Study Assistant</h3>
            <p>Generate flashcards and quizzes from your notes. Upload PDFs or paste text.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='feature-card'>
            <h3>💰 Budget Tracker</h3>
            <p>Track expenses, import/export data, and visualize spending patterns with charts.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='feature-card'>
            <h3>📄 CV Builder</h3>
            <p>Create professional CVs and export as PDF or DOCX with one click.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 🎯 Quick Tips")
    st.info("""
    ✨ **Study Assistant**: Upload a PDF textbook or paste lecture notes to auto-generate study materials\n
    💡 **Budget Tracker**: Categorize spending and export reports for analysis\n
    🎓 **CV Builder**: Keep your resume up-to-date with live preview and exports
    """)

elif page == "📚 Study Assistant":
    st.header("📚 Study Assistant")
    sa = StudyAssistant()
    sa.ui()

elif page == "💰 Budget Tracker":
    st.header("💰 Budget Tracker")
    bt = BudgetTracker(db_path="budget.db")
    bt.ui()

elif page == "📄 CV Builder":
    st.header("📄 CV Builder")
    cb = CVBuilder()
    cb.ui()

else:  # About
    st.header("ℹ️ About AI Study Suite")
    st.markdown("""
    ### Project Overview
    AI Study Suite is a comprehensive Streamlit application designed to boost your productivity across three key areas:
    
    **📚 Study Assistant**
    - Generate interactive flashcards from any text
    - Create multiple-choice quizzes
    - Upload PDFs and TXT files
    - Save study sessions for later review
    - Optional AI integration for smarter question generation
    
    **💰 Budget Tracker**
    - Track daily expenses with categories
    - Import/export transaction data as CSV
    - Visualize spending patterns with pie charts
    - Get spending summaries by category
    
    **📄 CV Builder**
    - Build professional resumes
    - Export as PDF or DOCX
    - Live preview functionality
    - Customizable sections
    
    ### Technology Stack
    - **Frontend**: Streamlit (Python)
    - **Database**: SQLite
    - **Data Analysis**: Pandas, Matplotlib
    - **Document Export**: FPDF, python-docx
    - **PDF Parsing**: PyPDF2
    
    ### Version
    **v2.0 - Advanced Edition**
    
    ### Features
    ✅ PDF/TXT file uploads\n
    ✅ CSV import/export\n
    ✅ Data visualization\n
    ✅ Multi-format CV export\n
    ✅ Session management\n
    ✅ Responsive UI\n
    
    ### Getting Started
    1. Choose a tool from the sidebar
    2. Follow the on-screen instructions
    3. Export or save your results
    
    ### Support
    For issues or feature requests, please contact the development team.
    """)
    
    st.divider()
    st.markdown("### 📊 Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Features", "15+")
    with col2:
        st.metric("Supported Formats", "PDF, DOCX, CSV, TXT")
    with col3:
        st.metric("Database Entries", "Unlimited")
