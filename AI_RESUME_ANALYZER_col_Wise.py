import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
from pypdf import PdfReader
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
client=OpenAI()
st.set_page_config(page_title="AI Based Resume Analyzer",layout="wide")

# with st.sidebar:
#    st.title("📊 ResumeMetric AI")
#    file=st.file_uploader("Upload your Resume ",type=["pdf"])
#    job_r=st.text_input("What is the job role? ")
st.title("📊 ResumeMetric AI")
col1, col2 = st.columns(2)
with col1:
    file=st.file_uploader("Upload a file",type=["pdf"])
   
with col2:    
     job_r=st.text_input("Enter Job Role")
if file is not None:
    
    reader=PdfReader(file)
    pdf_text=" "
    for page in reader.pages:
        text=page.extract_text()#automatically har page nu data extract thase. iagram extract nai thay
        pdf_text=pdf_text+text+"\n"
    if st.button("Preview Analysis"):
    
      prompt=f"""
      You are a resume analyzer,
      You extract resume content including education,technical skills, experience and projects from {pdf_text},
      If either of the fields are not mentioned in the resume then clearly mention the field name not present for example:
      Experience: Not Specified
      Compare the qualities with the job role {job_r} specified and determine whether the candidate is eligible for job or not,
      Generate a compatability score for example:
      Compatability Score: 
      Then specify a seperate skills section which mentions:
      Matching Skills:
      Missing Skills:
      Underrepresented Skills:
      [Show this in a tabular form for better understanding]
      After that mention Improvements Section as follows:
      Improvements to make on Resume:
      [Here mention all the crucial improvements candidate can make, so that their resume becomes more,
      desirable for companies to select, mention it point wise and in simple language so that the candidate can make changes easily]
      Generate an ATS score as well as:
      ATS Score:
      [Provide explanation for the given ATS score]
      Structure should be as follows:
      Extracted Information:
      --------------------------
      Skills Table:
      ------------------------
      Improvements:
      -------------------------
      ATS Score:
      -------------------------
      Desirable for Job:[Along with reason]
      --------------------------
    
      """
      response=client.responses.create(model="gpt-4.1-mini",input=prompt)
      st.write(response.output_text)

else:
    st.write("No resume recieved")
