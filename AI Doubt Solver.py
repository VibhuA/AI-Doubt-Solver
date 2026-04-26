import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. CONFIGURATION & AI SETUP
# ==========================================
# Replace 'YOUR_API_KEY_HERE' with the key you got from Google AI Studio
genai.configure(api_key="AIzaSyBmQ5hVHo2WZdK2SUvrUvHW-YNEMkDguEk")

# This is the "Specialist Tutor" Instruction
SYSTEM_INSTRUCTION = """
You are the 'HFS ICSE Mastery Bot', an elite private tutor for 8th and 9th-grade 
students at Hiranandani Foundation School (HFS). 

YOUR CORE MISSION:
1. Ground every answer in the 'Selina Concise' textbook series (Physics, Chemistry, Bio, Maths).
2. For History/Civics and Geography, follow the latest ICSE board guidelines.
3. KEYWORDS: ICSE marks are based on keywords. Always BOLD the essential technical 
   terms (e.g., 'Latent Heat', 'Electronegativity', 'Sovereign').
4. TEACHING STYLE: Do not just give the answer. 
   - Start with a 'Thinking Hint'.
   - Show the Step-by-Step logical derivation.
   - Mention which chapter/topic this belongs to.
5. FORMATTING: Use LaTeX for all mathematical equations and chemical formulas to ensure clarity.
"""

model = genai.GenerativeModel(
    model_name='gemini-3-flash',
    system_instruction=SYSTEM_INSTRUCTION
)

# ==========================================
# 2. APP LAYOUT & GATEKEEPER
# ==========================================
st.set_page_config(page_title="HFS ICSE Mastery", page_icon="🎓")

# Sidebar for Access Control
st.sidebar.title("🔐 Student Access")
access_code = st.sidebar.text_input("Enter Classroom Code:", type="password")

# Only show the app if the code is correct
if access_code == "HFS9_2026": # Change this monthly to manage payments
    st.title("🎓 HFS ICSE Mastery Suite")
    st.markdown("---")

    # Tabs for different features
    tab1, tab2, tab3 = st.tabs(["📸 Homework Helper", "📝 Practice Tests", "📖 Revision Notes"])

    # --- TAB 1: HOMEWORK HELPER (IMAGE UPLOAD) ---
    with tab1:
        st.header("Upload Homework Photo")
        st.info("Snap a photo of your Selina textbook or school worksheet.")
        
        img_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        
        if img_file is not None:
            image = Image.open(img_file)
            st.image(image, caption='Uploaded Worksheet', use_column_width=True)
            
            if st.button("Analyze & Solve"):
                with st.spinner("Analyzing based on ICSE Marking Scheme..."):
                    try:
                        # Sending image + text to Gemini
                        response = model.generate_content([
                            "Analyze this ICSE question. Provide a hint, the keywords, and the full step-by-step solution.", 
                            image
                        ])
                        st.subheader("Tutor Response:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")

    # --- TAB 2: PRACTICE TESTS ---
    with tab2:
        st.header("Generate Practice Questions")
        subject = st.selectbox("Subject", ["Physics", "Chemistry", "Biology", "Mathematics", "History/Civics"])
        topic = st.text_input("Enter Chapter Name (e.g., 'Atomic Structure')")
        num_q = st.slider("Number of questions", 1, 5, 3)

        if st.button("Generate Test"):
            with st.spinner("Creating HFS-style questions..."):
                prompt = f"Generate {num_q} ICSE 9th grade questions for {subject} on the topic '{topic}'. Include a marking scheme."
                response = model.generate_content(prompt)
                st.write(response.text)

    # --- TAB 3: REVISION ---
    with tab3:
        st.header("Quick Concept Summary")
        concept = st.text_input("What concept do you want to revise?")
        if st.button("Get Summary"):
            with st.spinner("Summarizing Selina content..."):
                response = model.generate_content(f"Give a concise, bullet-point revision summary for '{concept}' for ICSE Grade 9.")
                st.markdown(response.text)

else:
    if access_code != "":
        st.sidebar.error("Invalid Code. Please contact your teacher.")
    st.title("Welcome to the HFS Mastery Suite")
    st.info("Please enter the access code on the sidebar to begin your session.")
    st.image("https://img.icons8.com/clouds/500/education.png", width=300)

# ==========================================
# 3. FOOTER
# ==========================================
st.markdown("---")
st.caption("Powered by Gemini AI | Curated for Hiranandani Foundation School Students")
