# #here doing is: using PyPDF2, want to convert pdf to text, and that text getting and 
# #and hit to the Gemini Pro API with respect to some prompt template, and get response


# import streamlit as st
# import google.generativeai as genai
# import os
# import PyPDF2 as pdf
# import io
# from dotenv import load_dotenv

# load_dotenv() #load all the environment variables

# # Configure Gemini Pro API
# genai.configure(api_key=os.getenv("Google_API_KEY"))

# #Gemini Pro response
# def get_gemini_response(input):
#     model=genai.GenerativeModel('gemini-pro') # gemini-pro uses to convert pdf to text
#     response=model.generate_content(input) 
#     return response.text


# from PyPDF2 import PdfReader

# def input_pdf_text(uploaded_file):
#     # Open the uploaded file using PdfReader
#     reader = PdfReader(uploaded_file)
#     # Initialize a variable to store extracted text
#     extracted_text = ""
#     # Loop through each page and extract text
#     for page in reader.pages:
#         extracted_text += page.extract_text()
#     return extracted_text

# # Streamlit app setup
# st.set_page_config(page_title="ATS Resume Analyzer")
# st.header("✨ RecruitTrack - ATS Analytics Hub 📊🚀")

# # User inputs
# jd=st.text_area("Paste the Job Description: ", help="Provide the job description for evaluation.")
# uploaded_file=st.file_uploader("Drop Your Candidate Resume as a PDF",type="pdf",help="Please upload the candidate's resume")


# # Prompts for different actions
# input_prompt1 = """
# You are an experienced HR with tech expertise in various job roles, including Data Science, Data Analytics, Full Stack, Web Development, 
# Big Data Engineer, DevOps, Data Engineering, QE, Machine Learning Engineer, Business Intelligence Analyst,Quality Assurance,AI/ML engineer
# Database Engineer, Cloud Infrastructure Engineer, Database Engineer, PowerBI developer, Python Developer and Quantitative Analyst. 
# Your task is to review the provided resume against the job description. Please share a professional evaluation on whether the candidate's profile
# aligns with the role. Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
# Resume: {resume_text}
# Job Description: {job_description}
# """

# input_prompt3 = """
# As an expert ATS, identify the missing keywords in the candidate's resume based on the provided job description. Provide a detailed list of the
# missing keywords and explain their relevance.
# Resume: {resume_text}
# Job Description: {job_description}
# """

# input_prompt4 = """
# You are a skilled ATS scanner. Evaluate the resume against the provided job description. Provide the percentage match between the resume 
# and the job description, followed by missing keywords and final thoughts.
# Resume: {resume_text}
# Job Description: {job_description}
# """

# if st.button("Review Candidate Details"):
#     if uploaded_file and jd:
#         resume_text = input_pdf_text(uploaded_file)
#         input_prompt = input_prompt1.format(resume_text=resume_text, job_description=jd)
#         response = get_gemini_response(input_prompt)
#         st.subheader("Candidate Review")
#         st.write(response)
#     else:
#         st.error("Please upload the candidate resume and provide a job description.")

# if st.button("Identify Missing Keywords"):
#     if uploaded_file and jd:
#         resume_text = input_pdf_text(uploaded_file)
#         input_prompt = input_prompt3.format(resume_text=resume_text, job_description=jd)
#         response = get_gemini_response(input_prompt)
#         st.subheader("Missing Keywords")
#         st.write(response)
#     else:
#         st.error("Please upload the candidate resume and provide a job description.")

# if st.button("Similarity Analysis"):
#     if uploaded_file and jd:
#         resume_text = input_pdf_text(uploaded_file)
#         input_prompt = input_prompt4.format(resume_text=resume_text, job_description=jd)
#         response = get_gemini_response(input_prompt)
#         st.subheader("Similarity Analysis")
#         st.write(response)
#     else:
#         st.error("Please upload the candidate resume and provide a job description.")

# #custom styling
# st.markdown("""
#     <style>
#     .stButton>button {
#         background-color:rgb(64, 101, 134);
#         color: white;
#         border-radius: 10px;
#     }
#     .block-container {
#         padding-top: 4rem;
#     }
#     input, select, textarea, .stTextInput, .stSelectbox, .stSlider {
#         background-color:#10F5F1 !important;
#         color:#03116e !important;
#     }
#     label {
#         color: #F60582  !important;
#         margin-top: 10px;  /* Adds space above the label */
#         display: block; 
#         font-size: 20px !important;  /* Increase font size */
#     }
#     </style>
# """, unsafe_allow_html=True)

import streamlit as st
from google import genai
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("Google_API_KEY")

# Create GenAI client
client = genai.Client(api_key=GOOGLE_API_KEY)

# Function to call Gemini
def get_gemini_response(input_text):
    # Call generate_content correctly
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # or another available model
        contents=input_text
    )
    return response.text

# Extract text from PDF
def input_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted_text += page_text + "\n"
    return extracted_text

# Streamlit UI
st.set_page_config(page_title="ATS Resume Analyzer")
st.header("✨ RecruitTrack - ATS Analytics Hub 📊🚀")

jd = st.text_area(
    "Paste the Job Description:",
    help="Provide the job description for evaluation."
)

uploaded_file = st.file_uploader(
    "Drop Your Candidate Resume as a PDF",
    type="pdf"
)

# Prompt templates
input_prompt1 = """
You are an experienced HR with tech expertise in various job roles, including Data Science, Data Analytics, Full Stack, Web Development, 
Big Data Engineer, DevOps, Data Engineering, QE, Machine Learning Engineer, Business Intelligence Analyst,Quality Assurance,AI/ML engineer
Database Engineer, Cloud Infrastructure Engineer, Database Engineer, PowerBI developer, Python Developer and Quantitative Analyst. 
Your task is to review the provided resume against the job description. Please share a professional evaluation on whether the candidate's profile
aligns with the role. Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
Resume: {resume_text}
Job Description: {job_description}
"""

input_prompt3 = """
As an expert ATS, identify the missing keywords in the candidate's resume based on the provided job description. Provide a detailed list of the
missing keywords and explain their relevance.
Resume: {resume_text}
Job Description: {job_description}
"""

input_prompt4 = """
You are a skilled ATS scanner. Evaluate the resume against the provided job description. Provide the percentage match between the resume 
and the job description, followed by missing keywords and final thoughts.
Resume: {resume_text}
Job Description: {job_description}
"""

# Actions
if st.button("Review Candidate Details"):
    if uploaded_file and jd:
        resume_text = input_pdf_text(uploaded_file)
        prompt = input_prompt1.format(
            resume_text=resume_text,
            job_description=jd
        )
        response = get_gemini_response(prompt)
        st.subheader("Candidate Review")
        st.write(response)
    else:
        st.error("Please upload the resume and provide a job description.")

if st.button("Identify Missing Keywords"):
    if uploaded_file and jd:
        resume_text = input_pdf_text(uploaded_file)
        prompt = input_prompt3.format(
            resume_text=resume_text,
            job_description=jd
        )
        response = get_gemini_response(prompt)
        st.subheader("Missing Keywords")
        st.write(response)
    else:
        st.error("Please upload the resume and provide a job description.")

if st.button("Similarity Analysis"):
    if uploaded_file and jd:
        resume_text = input_pdf_text(uploaded_file)
        prompt = input_prompt4.format(
            resume_text=resume_text,
            job_description=jd
        )
        response = get_gemini_response(prompt)
        st.subheader("Similarity Analysis")
        st.write(response)
    else:
        st.error("Please upload the resume and provide a job description.")

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: rgb(64, 101, 134);
        color: white;
        border-radius: 10px;
    }
    .block-container {
        padding-top: 4rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    input, select, textarea {
        background-color: #10F5F1 !important;
        color: #03116e !important;
    }
    </style>
""", unsafe_allow_html=True)

