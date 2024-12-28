import streamlit as st
from resources import data
import time



if "data" not in st.session_state:
    st.session_state.data = data


if "page" not in st.session_state:
    st.session_state.page = "home"

if "cv" not in st.session_state:
    st.session_state.cv = None

# Function to handle updating the data in session state
def general_info(data):
    st.markdown("### General Info")
    c1, c2, c3 = st.columns(3)
    with c1:
        data["name"] = st.text_input(label="Name", value=data["name"], key="name")
        data["location"] = st.text_input(label="Location", value=data["location"], key="location")
    with c2:
        data["email"] = st.text_input(label="Email", value=data["email"], key="email")
    with c3:
        data["phone"] = st.text_input(label="Phone", value=data["phone"], key="phone")

def education(data):
    st.markdown("### Education")

    # Display existing fields
    for i, edu_field in enumerate(data['education']):
        st.markdown(f"#### Education {i+1}")
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

        with col1:
            edu_field['degree'] = st.text_input(label="Degree", value=edu_field['degree'], key=f"degree_{i}")
            edu_field['institute'] = st.text_input(label="Institute", value=edu_field['institute'], key=f"institute_{i}")

        with col3:
            edu_field['year']['year'] = st.text_input(label="Year of Graduation", value=edu_field['year']['year'], key=f"year_{i}")

        with col4:
            edu_field['year']['month'] = st.text_input(label="Month of Graduation", value=edu_field['year']['month'], key=f"month_{i}")
    
    # Add button for Education

    add_education = st.button("Add Education")

    if add_education:
        
        new_education = {
            'degree': st.text_input(label="degree"),
            'institute': st.text_input(label="institute"),
            'year': {'year': st.text_input("Year of graduation"), 'month': st.text_input("Month of graduation")},
        }
        
        data['education'].append(new_education)
        st.rerun()

def experience(data):
    st.markdown("### Experience")
    for i, exp in enumerate(data['work_experience']):
        st.markdown(f"#### Experience {i+1}")
        c1, c2, c3, c4 = st.columns([2, 0.75, 1, 1])

        with c1:
            exp["company"] = st.text_input(label="Company", value=exp["company"], key=f"company_{i}")
            exp["role"] = st.text_input(label="Role", value=exp["role"], key=f"role_{i}")
        with c3:
            exp["start_date"]["month"] = st.text_input(label="Start Month", value=exp['start_date']['month'], key=f"start_month_{i}")
            exp["start_date"]["year"] = st.text_input(label="Start Year", value=exp['start_date']['year'], key=f"start_year_{i}")
        with c4:
            exp["end_date"]["month"] = st.text_input(label="End Month", value=exp['end_date']['month'], key=f"end_month_{i}")
            exp["end_date"]["year"] = st.text_input(label="End Year", value=exp['end_date']['year'], key=f"end_year_{i}")

        exp["description"] = st.text_area(label="Description", value=exp["description"], height=150, key=f"description_{i}")
    
    # Add button for Experience

    add_experience = st.button("Add Experience")

    if add_experience:
        new_experience = {
            'company': '',
            'role': '',
            'start_date': {'month': '', 'year': ''},
            'end_date': {'month': '', 'year': ''},
            'description': '',
        }
        data['work_experience'].append(new_experience)

def skills(data):
    st.markdown("### Skills")
    for i, skill in enumerate(data['skills']):
        data['skills'][i] = st.text_input(label="Skill", value=skill, key=f"skill_{i}")
    
    # Add button for Skills
    add_skill = st.button("Add Skill")

    if add_skill:
        data['skills'].append('')

def courses(data):
    st.markdown("### Courses")
    for i, course in enumerate(data['courses']):
        data['courses'][i] = st.text_input(label="Course", value=course, key=f"course_{i}")
    
    # Add button for Courses

    add_course = st.button("Add Course")

    if add_course:
        data['courses'].append('')

def certifications(data):
    st.markdown("### Certifications")
    for i, cert in enumerate(data['certifications']):
        data['certifications'][i] = st.text_input(label="Certification", value=cert, key=f"cert_{i}")
    
    # Add button for Certifications
    if st.button("Add Certification"):
        data['certifications'].append('')

def handle_submission(data):
    st.write("Form Submitted!")
    st.write(data)

def parse_cv(data):
    st.markdown("## Parsing Area")

    general_info(data)
    education(data)
    experience(data)
    skills(data)
    courses(data)
    certifications(data)

    # Final submit button
    submit_button = st.button("Submit", on_click=handle_submission, args=(data,))

# Run the app logic
if st.session_state.page == "home":
    st.title("CV Optimizer")
    cv = st.file_uploader("Upload your CV here.", type="pdf")

    if cv:
        if cv.name.endswith(".pdf"):
            st.session_state.page = "parsing_page"
            st.rerun()

if st.session_state.page == "parsing_page":
    with st.spinner("Parsing your CV..."):
        time.sleep(2)
        parse_cv(st.session_state.data)
