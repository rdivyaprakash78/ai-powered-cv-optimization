import streamlit as st
#from structured_output import get_structured_output
from Fair.resources import cv3

sample = {'name': 'Vikram Elappakkam Lakshmipathi',
 'email': 'lvikram12g@gmail.com',
 'phone': '+44 7909320339',
 'location': 'London',
 'education': [{'degree': 'Master of Science in Data Science',
   'institute': 'Kingston University, London',
   'year': 'Jan 2023 - Jan 2024'},
  {'degree': 'Bachelor of Engineering in Computer Science',
   'institute': 'Amrita Vishwa Vidyapeetham, Kerala, India',
   'year': 'Jul 2017 - Jun 2021'}],
 'work_experience': [{'company': 'Tata Consultancy Services',
   'role': 'Business Analyst',
   'description': "Analyzed financial and operational data to identify key trends and provided actionable insights, driving resource allocation optimization and improving process efficiency by 40%. Created and maintained over 50+ reports in Power BI and Excel, enhancing data accessibility and financial reporting for senior management and key stakeholders. Created recurring and ad-hoc weekly, monthly, and quarterly Excel reports using PowerBi with the required visualisations by pulling the relevant data from the client's database to provide insights that support with the client's business strategies and decision-making. Collaborated with cross-functional teams to understand business data requirements, delivering tailored data solutions that aligned with strategic goals and increased client satisfaction by 25%. Enhanced data collection procedures to improve data accuracy and support data-driven decision-making in high-priority finance and resource management projects. Played a pivotal role in profit/loss analysis, ensuring the accuracy of key financial metrics, and supporting senior management in shaping business strategy.",
   'start_date': 'May 2021',
   'end_date': 'Dec 2022'},
  {'company': 'Omdena (UEFA Euro 2024 Project)',
   'role': 'Intern - Data Analyst',
   'description': 'Collaborated with a global team on a project analyzing investment opportunities and operational performance for the UEFA Euro 2024 tournament, applying advanced data analysis techniques to derive actionable insights. Developed and maintained interactive dashboards using Power BI and Excel, providing clear visualizations of key metrics that improved data-driven decision-making for stakeholders. Applied statistical techniques and machine learning algorithms in Python to assess trends in team performance, ticket sales, and financial investments, contributing to the optimization of event planning strategies. Provided data-driven recommendations to improve resource allocation and boost event profitability by 15%. Ensured data integrity and compliance throughout the project by validating datasets and automating data extraction processes, leading to a 20% improvement in reporting accuracy and efficiency.',
   'start_date': 'Apr 2023',
   'end_date': 'Aug 2023'}],
 'skills': ['Data Analysis & Financial Reporting',
  'Data Visualization',
  'Programming & Statistical Analysis',
  'Data Quality & Integrity',
  'Stakeholder Collaboration',
  'Machine Learning & Statistical Techniques'],
 'projects': ['Driver Drowsiness Detection (Dissertation)',
  'Medical Image Classification',
  'UK Airport Punctuality Analysis',
  'Crime Statistics Analysis']}

data = sample.items()

def create_fields(data, child_flag=False):
    form_data = {}

    for key, value in data:
        if isinstance(value, dict):
            form_data[key] = create_fields(value) 
        elif isinstance(value,list):
            form_data[key] = []
            st.write(key)
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    create_fields(item.items(), child_flag=True)
                else:
                    form_data[key].append(st.text_input("", value=item))
        else:
            form_data[key] = st.text_input(key, value=value)

st.title("CV Parser")
st.write("Upload your CV here.")

user_cv = st.file_uploader("")

if user_cv :
    if user_cv.name.endswith(".pdf"):
        st.success("File uploaded successfully")
        create_fields(data)
            
    else:
        st.error("Only PDF files are allowed")
        user_cv = None
        



            
        
