import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. AI SETUP (Gemini 2.5 Flash)
# ==========================================
# ⚠️ SECURITY ALERT: Remove your API key before pushing to GitHub! 
# Use st.secrets instead for safety.
genai.configure(api_key="AIzaSyB2LzyTw_nzBVkj8RIQoeB5QSUcBmKpxj0")

# Updated System Prompt with strict ICSE Marking Scheme instructions
MATH_SYSTEM_PROMPT = """
You are the 'HFS Math Specialist', an elite tutor for ICSE Class 8 and 9. 

YOUR CORE PROTOCOL:
1. MATH ONLY: Solve only Mathematics problems. 
2. ICSE MARKING SCHEME: For every solution, you MUST provide a 'Marking Breakdown' at the end of the steps.
   - 1 Mark for Formula.
   - 1 Mark for Substitution.
   - 1-2 Marks for Method/Calculation.
   - 1 Mark for Final Answer with correct units.
3. LOGICAL STRUCTURE: Use bold headers: 'Given', 'Formula', 'Step-by-Step Calculation', and 'Final Answer'.
4. LaTeX: Use $$ for block equations and $ for inline math. 
5. COMMON TRAPS: Warn the student if they might forget to convert units (e.g., minutes to hours) which is a common ICSE trap.
"""

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=MATH_SYSTEM_PROMPT
)

# ==========================================
# 2. APP UI
# ==========================================
st.set_page_config(page_title="HFS Math Mastery", page_icon="📐")

# Sidebar Access
st.sidebar.title("🔐 Student Portal")
access_code = st.sidebar.text_input("Enter Classroom Code:", type="password")

if access_code == "HFS_MATH_2026":
    st.title("📐 HFS Math Mastery Suite")
    st.write("Expert ICSE Guidance with Step-Marking Insights")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🔍 AI Doubt Solver", "📸 Homework Snap", "📝 Practice Generator"])

    # --- TAB 1: DOUBT SOLVER (Text) ---
    with tab1:
        st.header("Instant Doubt Solver")
        user_doubt = st.text_area("Type your math doubt here...")
        
        if st.button("Explain to Me"):
            if user_doubt:
                with st.spinner("Analyzing math logic..."):
                    # Prompt updated to ask for marking scheme logic
                    prompt = f"Explain this concept and how marks are usually awarded for it in ICSE: {user_doubt}"
                    response = model.generate_content(prompt)
                    st.markdown(response.text)

    # --- TAB 2: HOMEWORK SNAP ---
    with tab2:
        st.header("📸 Photo Homework Helper")
        img_file = st.file_uploader("Upload a photo of the math problem", type=["jpg", "jpeg", "png"])
        
        if img_file:
            st.image(img_file, caption="Uploaded Problem", width=400)
            
            if st.button("Solve with Marking Scheme"):
                with st.spinner("Processing image and applying marking scheme..."):
                    img_data = {
                        "mime_type": img_file.type,
                        "data": img_file.getvalue()
                    }
                    response = model.generate_content([
                        "Solve this problem using formal ICSE steps and include a clear marking breakdown (1M for formula, 1M for substitution, etc.):", 
                        img_data
                    ])
                    st.subheader("Solution & Step-Marking:")
                    st.markdown(response.text)

    # --- TAB 3: PRACTICE GENERATOR ---
    with tab3:
        st.header("📝 Personalized Practice")
        grade = st.radio("Select Grade", ["Class 8", "Class 9"])
        topics = ["Rational Numbers", "Compound Interest", "Expansions", "Factorisation", "Trigonometry", "Statistics"]
        selected_topic = st.selectbox("Topic", topics)
        
        if st.button("Generate 3 Sums"):
            with st.spinner("Generating questions with marking guide..."):
                prompt = f"Generate 3 tricky ICSE {grade} math problems for: {selected_topic}. For each sum, provide the solution and a 'Marking Scheme' table."
                response = model.generate_content(prompt)
                st.markdown(response.text)

else:
    st.info("Enter the code in the sidebar to begin.")

st.markdown("---")
st.caption("© 2026 HFS Math Mastery | Teacher Verified ICSE Methodology")
