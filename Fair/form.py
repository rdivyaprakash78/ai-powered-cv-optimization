import streamlit as st
from resources import data
import time

def handleClick():
    st.write(st.session_state["data"])

def general_info(data):
    
    st.markdown("### General Info")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state["data"]["name"] = st.text_input(label = "Name", value= data["name"])
        st.session_state["data"]["location"] = st.text_input(label = "Location", value= data["location"])
    with c2:
        st.session_state["data"]["email"] = st.text_input(label = "Email", value= data["email"])
    with c3:
        st.session_state["data"]["phone"] = st.text_input(label = "Phone", value= data["phone"])

def education(data):
    st.markdown("### Education")

    for i, institute in enumerate(data["education"]):
        st.markdown(f"###### Education {i+1}")

        c1, c2, c3,c4 = st.columns([2,0.75,1,1])

        with c1:
            st.session_state["data"]["education"][i]["degree"] = st.text_input(label = "Degree", value= institute["degree"])
            st.text_input(label = "Institute", value= institute["institute"])
        with c3:
            st.session_state["data"]["education"][i]["year"]["year"] = st.text_input(label = "Year of graduation", value= institute['year']['year'])
        with c4:
            st.session_state["data"]["education"][i]["year"]["month"] = st.text_input(label = "Month of graduation", value= institute['year']['month'])

    add = True
    while add:
        add_more = st.checkbox("Add more education")
        if add_more:
            degree = st.text_input("Degree")
            institute= st.text_input("Institute")
            year = st.text_input("Year of graduation")
            month = st.text_input("Month of graduation")
            st.session_state["data"]["education"].append({"degree": degree, "institute": institute, "year": {"year": year, "month": month}})
        add = False
        

def experience(data):
    st.markdown("### Experience")
    for i, experience in enumerate(data["work_experience"]):
        st.markdown(f"###### Experience {i+1}")

        c1, c2, c3,c4= st.columns([2,0.75,1,1])

        with c1:
            st.session_state["data"]["work_experience"][i]["company"] = st.text_input(label = "Company", value= experience["company"])
            st.session_state["data"]["work_experience"][i]["role"] = st.text_input(label = "Role", value= experience["role"])
        with c3:
            st.session_state["data"]["work_experience"][i]["start_date"]["month"] = st.text_input(label = "Start Month", value= experience['start_date']['month'])
            st.session_state["data"]["work_experience"][i]["start_date"]["year"] = st.text_input(label = "Start Year", value= experience['start_date']['year'])
        with c4:
            st.session_state["data"]["work_experience"][i]["end_date"]["month"] = st.text_input(label = "End Month", value= experience['end_date']['month'])
            st.session_state["data"]["work_experience"][i]["end_date"]["year"] = st.text_input(label = "End Year", value= experience['end_date']['year'])

        st.session_state["data"]["work_experience"][i]["description"] = st.text_area(label = "Description", value= experience["description"],height = 300)
    add_more_experience = st.checkbox("Add more")

def skills(data):
    st.markdown(f"### Skills")

    for i, skill in enumerate(data["skills"]):
        st.text_input(label = "", value=skill)
    add_more_skills = st.checkbox("Add more skills")

def courses(data):
    st.markdown(f"### Courses")

    for i, course in enumerate(data["courses"]):
        st.session_state["data"]["courses"][i]["name"] = st.text_area(label="name", value = data["courses"]["name"])
        st.session_state["data"]["courses"][i]["description"] = st.text_area(label="institution", value = data["courses"]["description"])
    add_more_courses = st.checkbox("Add more courses")

def certifications(data):
    st.markdown(f"### Certifications")

    for i, certificate in enumerate(data["certifications"]):
        st.session_state["data"]["certifications"][i]["name"] = st.text_input(label="name", value = certificate["name"])
        st.session_state["data"]["certifications"][i]["description"] = st.text_input(label="description", value = certificate["institution"])

    add_more_certifications = st.checkbox("Add more certifications")

def parse_cv(cv):
    data = st.session_state.data
    st.markdown("## Parsing Area")

    with st.form(key ="CV"):
        general_info(data)
        education(data)
        experience(data)
        skills(data)
        courses(data)
        certifications(data)
        st.form_submit_button("submit", on_click=handleClick)

if "data" not in st.session_state:
    st.session_state.data = data 

if "page" not in st.session_state:
    st.session_state.page = "home"

if "cv" not in st.session_state:
    st.session_state.cv = None

if st.session_state.page == "home":
    st.title("CV Optimizer")
    cv = st.file_uploader("Upload your CV here.", type = "pdf")

    if cv:
        if cv.name.endswith(".pdf"):
            st.session_state.cv = cv
            st.session_state.page = "parsing_page"
            st.rerun()

if st.session_state.page == "parsing_page":
    with st.spinner("Parsing your CV..."):
        st.write("")
        time.sleep(2)
        parse_cv(st.session_state.cv)

