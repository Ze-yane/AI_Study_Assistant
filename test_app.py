import streamlit as st
from study import StudyAssistant
from budget import BudgetTracker
from cv_builder import CVBuilder

st.set_page_config(
    page_title="AI Study Suite - TEST",
    page_icon="🚀",
    layout="wide"
)

st.title("AI Study Suite - Diagnostic Test")

# Simple sidebar navigation
page = st.sidebar.radio("Select Page:", ["Home", "Study", "Budget", "CV", "Test"])

if page == "Home":
    st.write("# Home Page")
    st.write("Select a tool from the sidebar")

elif page == "Study":
    st.write("# Study Assistant")
    try:
        sa = StudyAssistant()
        sa.ui()
    except Exception as e:
        st.error(f"Error: {e}")
        import traceback
        st.write(traceback.format_exc())

elif page == "Budget":
    st.write("# Budget Tracker")
    try:
        bt = BudgetTracker(db_path="budget.db")
        bt.ui()
    except Exception as e:
        st.error(f"Error: {e}")
        import traceback
        st.write(traceback.format_exc())

elif page == "CV":
    st.write("# CV Builder")
    try:
        cb = CVBuilder()
        cb.ui()
    except Exception as e:
        st.error(f"Error: {e}")
        import traceback
        st.write(traceback.format_exc())

else:  # Test
    st.write("# Diagnostic Test")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("StudyAssistant")
        try:
            sa = StudyAssistant()
            st.success("✓ Created")
            st.write(f"Stats: {len(sa.stats)} fields")
        except Exception as e:
            st.error(f"✗ {e}")
    
    with col2:
        st.subheader("BudgetTracker")
        try:
            bt = BudgetTracker(db_path="budget.db")
            st.success("✓ Created")
        except Exception as e:
            st.error(f"✗ {e}")
    
    with col3:
        st.subheader("CVBuilder")
        try:
            cb = CVBuilder()
            st.success("✓ Created")
        except Exception as e:
            st.error(f"✗ {e}")
