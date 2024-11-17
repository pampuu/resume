import streamlit as st
from fpdf import FPDF
import os
import random

# Directory for generated resumes
GENERATED_DIR = "Generated_Resumes"
if not os.path.exists(GENERATED_DIR):
    os.makedirs(GENERATED_DIR)

# Dictionary of predefined skills based on profession
profession_skills = {
    "Software Developer": ["Python", "JavaScript", "SQL", "Git"],
    "Data Scientist": ["Python", "Machine Learning", "Data Analysis", "SQL"],
    "Product Manager": ["Project Management", "Market Research", "Agile", "Communication"]
}

# Skill proficiency suggestions
proficiency_suggestions = {
    "Software Developer": {"Python": "Advanced", "JavaScript": "Intermediate", "SQL": "Intermediate"},
    "Data Scientist": {"Python": "Advanced", "Data Analysis": "Advanced", "SQL": "Intermediate"},
}

# Generate description without AI dependency
def generate_description(profession, skills, skill_proficiency, education, work_experiences):
    templates = [
        "As a {profession} with a background in {education}, I have developed expertise in {skills_list}. My key strength lies in {key_skill}, which I have demonstrated in my work at {latest_company}, where I {latest_experience}.",
        "With a strong foundation in {education} and hands-on experience in {skills_list}, I am a committed {profession}. My proficiency in {key_skill} has enabled me to excel at {latest_company}, where I {latest_experience}.",
        "I am an experienced {profession}, skilled in {skills_list}, with proven success in leveraging {key_skill} to deliver impactful results at {latest_company}. My education in {education} has further reinforced my capabilities."
    ]

    # Choose a random template
    template = random.choice(templates)

    # Process skills and skill proficiency
    skills_list = ', '.join([f"{skill} ({level})" for skill, level in skill_proficiency.items()])
    key_skill, key_skill_level = list(skill_proficiency.items())[0] if skill_proficiency else ("N/A", "N/A")

    # Get the latest work experience
    latest_experience = "worked on critical projects"
    latest_company = "my previous employer"
    if work_experiences:
        latest_experience = work_experiences[-1].get("description", latest_experience)
        latest_company = work_experiences[-1].get("company", latest_company)

    # Fill the template with provided information
    description = template.format(
        profession=profession,
        education=education['Level'],
        skills_list=skills_list,
        key_skill=key_skill,
        latest_company=latest_company,
        latest_experience=latest_experience
    )

    return description

# Generate PDF resume
def generate_pdf(resume_data):
    pdf = FPDF()
    pdf.add_page()

    # Define Colors
    header_color = (0, 102, 204)  # Blue for headers
    body_color = (50, 50, 50)     # Dark Gray for body text
    section_bg = (230, 230, 230)  # Light Gray for section background

    # Title Section with Background Color
    pdf.set_fill_color(*header_color)  # Header background
    pdf.set_text_color(255, 255, 255)  # White text
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 15, txt="Resume", ln=True, align="C", fill=True)
    pdf.ln(10)

    # Personal Information Section with Background
    pdf.set_fill_color(*section_bg)  # Light Gray Background
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 0, 0)  # Set text color to black
    pdf.cell(0, 10, txt="Personal Information", ln=True, fill=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, txt=f"Name: {resume_data['Personal Information']['Name']}", ln=True)
    pdf.cell(0, 8, txt=f"Email: {resume_data['Personal Information']['Email']}", ln=True)
    pdf.cell(0, 8, txt=f"Phone: {resume_data['Personal Information']['Phone']}", ln=True)
    pdf.ln(10)

    # Profession Section with Background
    pdf.set_fill_color(*section_bg)  # Light Gray Background
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt="Profession", ln=True, fill=True)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(*body_color)
    pdf.cell(0, 8, txt=f"{resume_data['Profession']}", ln=True)
    pdf.ln(10)

    # Professional Summary Section
    if "Description" in resume_data:
        pdf.set_fill_color(*section_bg)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, txt="Professional Summary", ln=True, fill=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, resume_data["Description"])
        pdf.ln(10)

    # Skills Section with Grid Formatting
    pdf.set_fill_color(*section_bg)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt="Skills and Proficiency", ln=True, fill=True)
    pdf.set_font("Arial", "", 12)
    for skill, level in resume_data['Skills'].items():
        pdf.cell(95, 8, txt=f"{skill}: {level}", ln=False)
        pdf.cell(95, 8, txt="", ln=True)  # Two-column layout
    pdf.ln(10)

    # Education Section
    pdf.set_fill_color(*section_bg)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt="Education", ln=True, fill=True)
    pdf.set_font("Arial", "", 12)
    education = resume_data['Education']
    pdf.multi_cell(0, 8, f"{education['Level']} from {education['Institution']} - Graduated in {education['Graduation Year']}")
    pdf.ln(10)

    # Work Experience Section
    pdf.set_fill_color(*section_bg)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt="Work Experience", ln=True, fill=True)
    pdf.set_font("Arial", "", 12)
    for exp in resume_data['Work Experience']:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, txt=f"{exp['position']} at {exp['company']}", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, txt=f"{exp['start_date']} to {exp['end_date']}", ln=True)
        pdf.multi_cell(0, 8, txt=exp['description'])
        pdf.ln(5)

    # Certifications Section
    if 'Certifications' in resume_data and resume_data['Certifications']:
        pdf.set_fill_color(*section_bg)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, txt="Certifications", ln=True, fill=True)
        pdf.set_font("Arial", "", 12)
        for cert in resume_data['Certifications']:
            pdf.cell(0, 8, txt=cert, ln=True)
        pdf.ln(10)

    # Footer Design
    pdf.set_y(-20)
    pdf.set_draw_color(*header_color)  # Footer Line Color
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Add a footer line
    pdf.set_font("Arial", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 10, "Generated using AI Resume Builder", 0, 0, "C")

    # Save the PDF
    pdf_output = os.path.join(GENERATED_DIR, "professional_resume.pdf")
    pdf.output(pdf_output)
    return pdf_output


# Streamlit App Logic
def run():
    st.title("AI Resume Builder")

    # Personal Information
    st.header("Personal Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    # Profession
    st.header("Profession")
    profession = st.selectbox("Select your profession", list(profession_skills.keys()) + ["Other"])
    if profession == "Other":
        profession = st.text_input("Specify your profession")

    # Skills and Proficiency
    st.header("Skills")
    skills = profession_skills.get(profession, [""])
    selected_skills = st.multiselect("Select or add your skills", skills, default=skills)

    st.subheader("Skill Proficiency")
    skill_proficiency = {}
    for skill in selected_skills:
        default_level = proficiency_suggestions.get(profession, {}).get(skill, "Beginner")
        skill_proficiency[skill] = st.select_slider(f"Proficiency in {skill}", options=['Beginner', 'Intermediate', 'Advanced', 'Expert'], value=default_level)

    # Education
    st.header("Education")
    education_level = st.selectbox("Highest Education Level", ["High School", "Bachelor's", "Master's", "PhD"])
    institution = st.text_input("Institution Name")
    graduation_year = st.number_input("Graduation Year", min_value=1950, max_value=2030, value=2020)

    # Work Experience
    st.header("Work Experience")
    num_experiences = st.number_input("Number of work experiences", min_value=0, max_value=10, value=1)
    experiences = []
    for i in range(int(num_experiences)):
        st.subheader(f"Experience {i+1}")
        company = st.text_input(f"Company Name", key=f"company_{i}")
        position = st.text_input(f"Position", key=f"position_{i}")
        start_date = st.date_input(f"Start Date", key=f"start_date_{i}")
        end_date = st.date_input(f"End Date", key=f"end_date_{i}")
        description = st.text_area(f"Description", key=f"description_{i}", height=100)

        experiences.append({
            "company": company,
            "position": position,
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "description": description or "Worked on various projects contributing to company goals."
        })

    # Certifications
    st.header("Certifications")
    cert_count = st.number_input("Number of certifications", min_value=0, max_value=10, value=1)
    certifications = []
    for i in range(int(cert_count)):
        cert = st.text_input(f"Certification {i+1}", key=f"cert_{i}")
        certifications.append(cert)

    # Generate Resume
    st.header("Generate Resume")
    if st.button("Generate Resume"):
        resume_data = {
            "Personal Information": {"Name": name, "Email": email, "Phone": phone},
            "Profession": profession,
            "Skills": skill_proficiency,
            "Education": {"Level": education_level, "Institution": institution, "Graduation Year": graduation_year},
            "Work Experience": experiences,
            "Certifications": certifications,
        }

        # Generate AI-based description
        description = generate_description(profession, selected_skills, skill_proficiency, resume_data['Education'], experiences)
        st.write(description)  # Display the generated description for preview
        resume_data["Description"] = description  # Add the description to the resume data

        # Generate and download PDF
        pdf_path = generate_pdf(resume_data)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(label="Download Resume", data=pdf_file, file_name="resume.pdf", mime="application/pdf")

# Run the app
run()
