import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. AI SETUP (Gemini 2.5 Flash)
# ==========================================
# Replace with your actual key from Google AI Studio
genai.configure(api_key="YOUR_API_KEY_HERE")

MATH_SYSTEM_PROMPT = """
You are the 'HFS Math Specialist', an elite tutor for ICSE Class 8 and 9. 

YOUR CORE PROTOCOL:
1. MATH ONLY: Solve only Mathematics problems. 
2. STEP-BY-STEP: Show clear calculations for step-marking.
3. LOGICAL STRUCTURE: Use 'Given', 'Formula', 'Calculation', and 'Final Answer'.
4. LaTeX: Use $$ for block equations and $ for inline math. 
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
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🔍 AI Doubt Solver", "📸 Homework Snap", "📝 Practice Generator"])

    # --- TAB 1: DOUBT SOLVER (Text) ---
    with tab1:
        st.header("Instant Doubt Solver")
        user_doubt = st.text_area("Type your math doubt here...")
        
        if st.button("Explain to Me"):
            if user_doubt:
                with st.spinner("Analyzing math logic..."):
                    response = model.generate_content(f"Explain this ICSE math concept: {user_doubt}")
                    st.markdown(response.text)

    # --- TAB 2: HOMEWORK SNAP (No PIL Version) ---
    with tab2:
        st.header("📸 Photo Homework Helper")
        img_file = st.file_uploader("Upload a photo of the math problem", type=["jpg", "jpeg", "png"])
        
        if img_file:
            # Display image without PIL
            st.image(img_file, caption="Uploaded Problem", width=400)
            
            if st.button("Solve Step-by-Step"):
                with st.spinner("Processing image..."):
                    # We pass the file bytes and mime type directly to Gemini
                    img_data = {
                        "mime_type": img_file.type,
                        "data": img_file.getvalue()
                    }
                    response = model.generate_content([
                        "Provide a formal ICSE step-by-step solution for this math problem:", 
                        img_data
                    ])
                    st.subheader("Solution:")
                    st.markdown(response.text)

    # --- TAB 3: PRACTICE GENERATOR ---
    with tab3:
        st.header("📝 Personalized Practice")
        grade = st.radio("Select Grade", ["Class 8", "Class 9"])
        topics = ["Rational Numbers", "Compound Interest", "Expansions", "Factorisation", "Trigonometry", "Statistics"]
        selected_topic = st.selectbox("Topic", topics)
        
        if st.button("Generate 3 Sums"):
            with st.spinner("Generating questions..."):
                response = model.generate_content(f"Generate 3 tricky ICSE {grade} math problems for: {selected_topic}")
                st.markdown(response.text)

else:
    st.info("Enter the code in the sidebar to begin.")

st.markdown("---")
st.caption("© 2026 HFS Math Mastery")
