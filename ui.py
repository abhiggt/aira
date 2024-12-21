import streamlit as st
import google.generativeai as genai
import PyPDF2

# Set page config
st.set_page_config(page_title="AIRA - Resume Enhancer", page_icon="📄")

# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def generate_resume_improvements(resume_text, experience, domain, job_role, specific_info):
    """Use Gemini to generate resume improvement suggestions."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Analyze the following resume and provide targeted improvements:

    Resume Content:
    {resume_text}

    Context:
    - Years of Experience: {experience}
    - Target Domain: {domain}
    - Target Job Role: {job_role}
    - Specific Additional Information: {specific_info}

    Please provide specific, actionable suggestions to enhance the resume, focusing on:
    1. Content Improvements
    2. Personalised Recommendations
    3. Skill Alignment
    4. Achievement Highlighting
    5. Keywords Optimization
    """
    try:
        response = model.generate_content(prompt)
        return response.text.split("##")  # Split into sections
    except Exception as e:
        st.error(f"Error generating improvements: {e}")
        return ["Unable to generate improvements at this time."]

def beautify_suggestions(suggestions):
    """Format suggestions for better readability with custom font and size."""
    cleaned_suggestions = []
    for idx, suggestion in enumerate(suggestions, 1):
        suggestion = suggestion.replace("**", "").strip()  # Clean unnecessary symbols
        # Add styled HTML for each suggestion
        cleaned_suggestions.append(f"""
        <div class="suggestion-text">
            <b>Key Suggestions:</b> {suggestion}
        </div>
        """)
    return cleaned_suggestions

def main():
    # Add custom CSS for the suggestions and hover effect
    st.markdown("""
    <style>
    .suggestion-text {
        font-family: 'Product Sans', sans-serif; /* Set font to Product Sans */
        font-size: 22 px; /* Increased text size */
        line-height: 1.5; /* Adjust line height for readability */
        color: black;
        margin-bottom: 15px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        backdrop-filter: blur(30px);
        transition: background 0.3s ease-in-out, color 0.3s ease-in-out;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .suggestion-text:hover {
        background: #171717; /* Dark background with custom color on hover */
        color: white; /* Text turns white on hover */
        border: 1px solid rgba(255, 255, 255, 0.6); /* Emphasized border */
    }
    </style>
    """, unsafe_allow_html=True)

   # Custom CSS for liquid animated gradient
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Product+Sans&display=swap');
    
    body {
        background: linear-gradient(120deg, #ece9e6, #ffffff); /* Soft background gradient */
      font-family: 'Product Sans', sans-serif;
    }

    .animated-gradient-text {
        font-size: 120px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        background: linear-gradient(90deg, #ff6f61, #ffcc33, #1ecbe1, #941ee1, #1D062D, #ff6f61);
        background-size: 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientFlow 7s infinite linear;
    }

    @keyframes gradientFlow {
        0% { background-position: 0%; }
        100% { background-position: 100%; }
    }

    .stButton>button {
        font-family: 'Product Sans', sans-serif;
        font-weight: bold;
        color: white;
        background: linear-gradient(45deg, aqua ,blue);
        width: 300px;
        height: 60px;
        border-radius: 30px;
        font-size: 1.2rem;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        color: aqua;
        background: #111111;
        border: 2px solid aqua;
    }

    .stButton>button:active {
        /* Keep same gradient when the button is clicked */
        color: #ffffff;
        background: linear-gradient(45deg, aqua ,blue);
        border: 2px solid aqua;
    }

    .upload-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }

    /* Center the Enhance My Resume button */
    .stButton {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title with Animated Gradient
    st.markdown("""
    <div class="animated-gradient-text">
        Aira
    </div>
    """, unsafe_allow_html=True)
    
    # Subtitle
    st.markdown("<h3 style='text-align: center; color: #6c757d;'>Enhance your Resume, Advance your Career</h3>", unsafe_allow_html=True)

    # Resume Upload Section
    st.markdown("<div class='upload-container'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=['pdf'])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Additional Information Section
        col1, col2, col3 = st.columns(3)
        
        with col1:
            experience = st.selectbox(
                "Years of Experience", 
                ["0-2", "2-5", "5-8","8-10","10+"]
            )
        
        with col2:
            domain = st.selectbox(
                "Target Domain", 
                ["IT", "Finance", "Marketing", "Sales", "Engineering","Design", "Operations", "Others"]
            )
        
        with col3:
            job_role = st.text_input("Specific Job Role", placeholder="e.g., Software Engineer")
        
        # Specific Information Section
        specific_info = st.text_area(
            "Any Specific Information", 
            placeholder="Company details, special requirements, etc.",
            height=100
        )

        # Animated Button
        st.markdown("""
        <style>
        div.stButton > button {
            animation: gradientFlow 5s infinite linear;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.button("Enhance My Resume"):
            with st.spinner('Analyzing & Suggesting Improvements...'):
                # Extract text from PDF
                resume_text = extract_text_from_pdf(uploaded_file)
                if resume_text:
                    raw_suggestions = generate_resume_improvements(resume_text, experience, domain, job_role, specific_info)
                    suggestions = beautify_suggestions(raw_suggestions)

                    # Display suggestions
                    st.subheader("")
                    for suggestion in suggestions:
                        st.markdown(suggestion, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown(""""""
        "Created by Abhijeet, Divyanshu & Lakshya",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    
