import streamlit as st

# Adding custom CSS with unique IDs
custom_css = """
<style>
    #form-title {
        font-size: 36px;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    #address-section {
        font-size: 24px;
        color: #2196F3;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    #contact-section {
        font-size: 24px;
        color: #2196F3;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    #submit-button button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    #submit-button button:hover {
        background-color: #45a049;
    }
    #output {
        background-color: #e8f5e9;
        border-radius: 5px;
        padding: 10px;
        font-size: 14px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Title with unique ID
st.markdown('<div id="form-title">Custom Form with Mixed Layout</div>', unsafe_allow_html=True)

# Horizontal layout for small input fields
col1, col2, col3 = st.columns(3)

with col1:
    first_name = st.text_input("First Name", placeholder="Enter first name", key="first_name")

with col2:
    last_name = st.text_input("Last Name", placeholder="Enter last name", key="last_name")

with col3:
    age = st.number_input("Age", min_value=0, max_value=120, step=1, key="age")

# Vertical layout for wide text boxes
st.markdown('<div id="address-section">Address Details</div>', unsafe_allow_html=True)

street_address = st.text_area("Street Address", placeholder="Enter your street address", key="street_address")
city = st.text_input("City", placeholder="Enter your city", key="city")
state = st.text_input("State", placeholder="Enter your state", key="state")
zip_code = st.text_input("ZIP Code", placeholder="Enter your ZIP code", key="zip_code")

# Adding another horizontal section for smaller fields
st.markdown('<div id="contact-section">Contact Information</div>', unsafe_allow_html=True)

col4, col5 = st.columns([2, 1])

with col4:
    email = st.text_input("Email Address", placeholder="Enter your email", key="email")

with col5:
    phone = st.text_input("Phone Number", placeholder="Enter your phone number", key="phone")

# Add a button at the bottom
st.markdown('<div id="submit-button">', unsafe_allow_html=True)
if st.button("Submit"):
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div id="output">', unsafe_allow_html=True)
    st.success("Form Submitted Successfully!")
    st.json({
        "First Name": first_name,
        "Last Name": last_name,
        "Age": age,
        "Street Address": street_address,
        "City": city,
        "State": state,
        "ZIP Code": zip_code,
        "Email": email,
        "Phone": phone
    })
    st.markdown('</div>', unsafe_allow_html=True)
