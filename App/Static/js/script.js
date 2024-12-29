const file = document.getElementById("fileInput");
const valid_type = "application/pdf";
const error_message = document.getElementById("remark");
const file_data = document.getElementById("cv");
let parsed_cv = "";
const currentPage = window.location.pathname;
const form_data = document.getElementById("parsedForm");

const json_data = {
  name: "Divyaprakash Rathinasabapathy",
  email: "rdivyaprakash78@gmail.com",
  phone: "+44 7818337189",
  location: "London, UK",
  education: [
    {
      degree: "Data Science, M.Sc.",
      institute: "Kingston University, U.K.",
      year: {
        month: "January",
        year: "2023",
      },
    },
    {
      degree: "Electronics and Communication Engineering, B.Tech.",
      institute: "Amrita School of Engineering, India",
      year: {
        month: "July",
        year: "2017",
      },
    },
  ],
  work_experience: [
    {
      company: "Navi Promotions",
      role: "AI Engineer Intern",
      description:
        "Developed Retrieval-Augmented Generation (RAG) based prototypes for chatbots, tailored to client specifications, incorporating advanced NLP models to enhance user interactions and meet business objectives. Engineered multi-agent flow architectures using frameworks such as Autogen and LangGraph, enabling the creation of dynamic, scalable AI systems that can handle complex, multi-step user interactions. Worked with backend frameworks like Flask to design and implement server-side architectures for AI solutions, ensuring smooth integration with client systems and services. Built and optimized robust Generative AI systems, focusing on improving the reliability and responsiveness of large language model (LLM) outputs, ensuring accurate and contextually appropriate results. Implemented advanced parsing techniques using libraries like Pydantic and Instructor, improving the extraction and validation of structured data from natural language inputs, enhancing the chatbot's performance and reliability. Documented development processes, model specifications, and system architectures to ensure clarity and facilitate future enhancements and knowledge transfer. Worked independently on the entire project, organizing and managing all aspects of the workflow, from requirements gathering to model deployment. This autonomy enhanced my ability to prioritize tasks, meet deadlines, and deliver high-quality solutions with minimal supervision.",
      start_date: "2024-10-01",
      end_date: "2024-12-29",
    },
    {
      company: "Omdena",
      role: "Junior Machine Learning Engineer Volunteer",
      description:
        "Collaborated with senior data scientists and clients to identify and define project objectives, gathering requirements and collecting relevant data to effectively address specific business challenges. Conducted thorough data validation using standardized protocols to ensure accuracy and integrity, laying a solid foundation for subsequent analysis. Performed exploratory data analysis (EDA), including data cleaning, visualization, and documentation, to uncover insights and support informed decision-making. Actively participated in workshops and training sessions, providing guidance and support to colleagues who required assistance in unfamiliar tasks, fostering a collaborative and inclusive team environment. Developed comprehensive reports and visualizations to clearly communicate findings to stakeholders, facilitating a better understanding of data-driven insights. Engaged in continuous learning and skill development, staying updated with industry best practices to enhance analytical capabilities and contribute effectively to team projects.",
      start_date: "2024-07-15",
      end_date: "2024-04-13",
    },
    {
      company: "Cognizant Technology Solutions, India",
      role: "Programmer Analyst trainee: Data Science",
      description:
        "Developed and optimized NLP models for extracting actionable insights from large datasets, utilizing state-of-the-art text processing techniques and parameter-efficient fine-tuning methods such as LoRA, Prompt Tuning, and P-tuning to enhance business decision-making processes. Implemented Retrieval-Augmented Generation (RAG) systems, combining document retrieval and generative models to improve the accuracy and relevance of automated responses for customer-facing applications. Utilized advanced NLP frameworks, including Hugging Face (for model deployment and fine-tuning) and TensorFlow, to build, fine-tune, and deploy language models for tasks including text summarization, sentiment analysis, and question-answering. Designed and built data pipelines for the efficient processing and transformation of textual data, ensuring that NLP models received high-quality, clean data for optimal performance. Integrated NLP solutions with external systems using RESTful APIs, enabling seamless interaction between the AI models and enterprise platforms, thus enhancing user experience and operational efficiency. Collaborated with cross-functional teams to gather requirements, define business goals, and deliver NLP solutions aligned with customer needs and business objectives.",
      start_date: "2021-08-21",
      end_date: "2022-9-13",
    },
  ],
  skills: [
    "Marketing Analytics & Statistical Algorithms",
    "Machine Learning & NLP",
    "Generative AI Systems",
    "Data Engineering & Integration",
    "Digital Analytics Solutions",
    "Programming Languages & Tools",
    "Collaboration & Stakeholder Engagement",
  ],
  projects: [
    {
      name: "AI powered CV optimization tool using Langgraph",
      description:
        "Built an AI-driven CV optimization tool using Python, LangChain, Cohere LLM API, and Streamlit to enhance CV relevance based on job descriptions. Designed a StateGraph framework for iterative CV evaluation, scoring, and refinement, with automated suggestions and keyword alignment. Developed a user-friendly interface enabling real-time CV updates, leveraging Regex for precise data extraction and actionable insights.",
    },
    {
      name: "Doctor’s appointment managing Chatbot",
      description:
        "Designed and built an interactive chatbot system for managing doctor appointments, using Google’s Gemini Large Language Model for NLP tasks such as intent and entity recognition. Implemented MySQL for database management and used Streamlit for the front-end interface. The chatbot automated tasks like appointment booking, editing, and cancellations, improving operational efficiency and user experience.",
    },
    {
      name: "Supply Chain Analysis Dashboard",
      description:
        "Developed an end-to-end Power BI dashboard for supply chain analysis, helping stakeholders track performance and customer satisfaction. Used Power Query for data cleaning and DAX for advanced calculations, enabling the visualization of key metrics such as OT %, IF %, and OTIF %. Provided a comprehensive analysis that allowed stakeholders to make informed decisions, driving improvements in operational performance.",
    },
    {
      name: "Ship Performance analysis",
      description:
        "Applied statistical techniques such as ANOVA and Tukey HSD to assess ship performance over time, identifying significant differences in performance metrics. Developed a dynamic Power BI dashboard to visualize time-series data, highlighting critical trends for strategic decision-making. Used ARIMAX forecasting to predict fuel consumption, achieving a Mean Absolute Percentage Error (MAPE) of 7.42%, providing reliable insights for optimizing fuel efficiency and reducing operational costs.",
    },
  ],
  courses: [
    {
      name: "corse 1",
      description: "description 1",
    },
    {
      name: "course 2",
      description: "description 2",
    },
  ],
  certifications: [
    {
      name: "certification 1",
      description: "description 1",
    },
    {
      name: "certification 2",
      description: "description 2",
    },
  ],
};

if (currentPage === "/") {
  home();
} else if (currentPage === "/parser") {
  parser();
}

function home() {
  file.addEventListener("change", (e) => {
    const cv = file.files[0];
    remark.innerHTML = "";
    if (cv.type == valid_type) {
      remark.style.color = "rgb(6, 179, 43)";
      remark.style.fontWeight = "bold";
      remark.innerHTML = "File uploaded successfully";

      const blob = new Blob([cv], { type: file.type });
      const formData = new FormData();
      formData.append("file", blob, file.name);

      fetch("/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          //parsed_cv = data.cv;
          //localStorage.setItem("parsed_cv", parsed_cv);
          window.location.href = data.redirect;
        });
    } else {
      remark.style.color = "red";
      remark.style.fontWeight = "bold";
      remark.innerHTML = "Please upload a valid PDF file";
    }
    file.value = "";
  });
}

function parser() {
  //parsed_cv = localStorage.getItem("parsed_cv");
  //let structured_cv = JSON.parse(parsed_cv);
  let form = document.getElementById("parsedForm");

  form.elements["name"].value = json_data.name;
  form.elements["email"].value = json_data.email;
  form.elements["mobile"].value = json_data.phone;
  form.elements["location"].value = json_data.location;

  // Function to create the "Add More" button dynamically
  function createAddMoreButton() {
    const addMoreButton = document.createElement("button");

    addMoreButton.id = "addMoreButton";
    addMoreButton.textContent = "Add More";
    addMoreButton.addEventListener("click", () => addEducationForm());
    document.getElementById("educationContainer").appendChild(addMoreButton);
  }

  // Function to add a new education form dynamically
  const addEducationForm = (data = {}) => {
    // Clone the first empty fieldset as a template
    const educationTemplate = document
      .querySelector(".Education")
      .cloneNode(true);

    // Clear any pre-filled values from the cloned template
    educationTemplate.querySelector('input[name="degree"]').value =
      data.degree || "";
    educationTemplate.querySelector('input[name="institute"]').value =
      data.institute || "";
    educationTemplate.querySelector('input[name="year"]').value =
      data.year?.year || "";
    educationTemplate.querySelector('input[name="month"]').value =
      data.year?.month || "";

    // Remove the existing "Add More" button
    const addMoreButton = document.getElementById("addMoreButton");
    if (addMoreButton) {
      addMoreButton.remove();
    }

    // Append the cloned template to the container
    const container = document.getElementById("educationContainer");
    container.appendChild(educationTemplate);

    // Add the "Add More" button back at the end
    createAddMoreButton();
  };

  // Function to populate data into the first field and create new fields if needed
  const populateEducationData = () => {
    const firstEducationField = document.querySelector(".Education");
    const educationData = json_data.education;

    // Populate the first field with the first entry in the data
    if (educationData.length > 0) {
      const firstData = educationData[0];
      firstEducationField.querySelector('input[name="degree"]').value =
        firstData.degree || "";
      firstEducationField.querySelector('input[name="institute"]').value =
        firstData.institute || "";
      firstEducationField.querySelector('input[name="year"]').value =
        firstData.year?.year || "";
      firstEducationField.querySelector('input[name="month"]').value =
        firstData.year?.month || "";
    }

    // Add additional fields for the remaining data entries
    educationData.slice(1).forEach((data) => addEducationForm(data));

    // Dynamically add the "Add More" button
    //createAddMoreButton();
  };

  // Initialize the form with the given data
  populateEducationData();
  //createAddMoreButton();

  // Function to create the "Add More" button dynamically
  function createAddMoreExperienceButton() {
    const addMoreExperienceButton = document.createElement("button");
    addMoreExperienceButton.id = "addMoreExperienceButton";
    addMoreExperienceButton.textContent = "Add More";
    addMoreExperienceButton.addEventListener("click", () =>
      addExperienceForm()
    );
    document
      .getElementById("experienceContainer")
      .appendChild(addMoreExperienceButton);
  }

  // Function to add a new education form dynamically
  const addExperienceForm = (data = {}) => {
    // Clone the first empty fieldset as a template
    const experienceTemplate = document
      .querySelector(".Experience")
      .cloneNode(true);

    // Clear any pre-filled values from the cloned template
    experienceTemplate.querySelector('input[name="company"]').value =
      data.company || "";
    experienceTemplate.querySelector('input[name="role"]').value =
      data.role || "";
    experienceTemplate.querySelector('input[name="startDate"]').value =
      data.start_date || "";
    experienceTemplate.querySelector('input[name="endDate"]').value =
      data.end_date || "";
    experienceTemplate.querySelector('textarea[name="description"]').value =
      data.description || "";

    // Remove the existing "Add More" button
    const addMoreExperienceButton = document.getElementById(
      "addMoreExperienceButton"
    );
    if (addMoreExperienceButton) {
      addMoreExperienceButton.remove();
    }

    // Append the cloned template to the container
    const container = document.getElementById("experienceContainer");
    container.appendChild(experienceTemplate);

    // Add the "Add More" button back at the end
    createAddMoreExperienceButton();
  };

  // Function to populate data into the first field and create new fields if needed
  const populateExperienceData = () => {
    const firstExperienceField = document.querySelector(".Experience");
    const experienceData = json_data.work_experience;

    // Populate the first field with the first entry in the data
    if (experienceData.length > 0) {
      const firstData = experienceData[0];
      firstExperienceField.querySelector('input[name="company"]').value =
        firstData.company || "";
      firstExperienceField.querySelector('input[name="role"]').value =
        firstData.role || "";
      firstExperienceField.querySelector('input[name="startDate"]').value =
        firstData.start_date || "";
      firstExperienceField.querySelector('input[name="endDate"]').value =
        firstData.end_date || "";
      firstExperienceField.querySelector('textarea[name="description"]').value =
        firstData.description || "";
    }

    // Add additional fields for the remaining data entries
    experienceData.slice(1).forEach((data) => addExperienceForm(data));

    // Dynamically add the "Add More" button
    //createAddMoreButton();
  };

  // Initialize the form with the given data
  populateExperienceData();

  // Function to create the "Add More" button dynamically
  function createAddMoreSkillButton() {
    const addMoreSkillButton = document.createElement("button");
    addMoreSkillButton.id = "addMoreSkillButton";
    addMoreSkillButton.textContent = "Add More";
    addMoreSkillButton.addEventListener("click", () => addSkillForm());
    document.getElementById("skillsContainer").appendChild(addMoreSkillButton);
  }

  // Function to add a new education form dynamically
  const addSkillForm = (data = []) => {
    // Clone the first empty fieldset as a template
    const skillTemplate = document.querySelector(".skill").cloneNode(true);

    // Clear any pre-filled values from the cloned template
    skillTemplate.querySelector('input[name="skill"]').value = data || "";

    // Remove the existing "Add More" button
    const addMoreSkillButton = document.getElementById("addMoreSkillButton");
    if (addMoreSkillButton) {
      addMoreSkillButton.remove();
    }

    // Append the cloned template to the container
    const container = document.getElementById("skillsContainer");
    container.appendChild(skillTemplate);

    // Add the "Add More" button back at the end
    createAddMoreSkillButton();
  };

  // Function to populate data into the first field and create new fields if needed
  const populateSkillData = () => {
    const firstSkillField = document.querySelector(".skill");
    const skillData = json_data.skills;

    // Populate the first field with the first entry in the data
    if (skillData.length > 0) {
      const firstData = skillData[0];
      firstSkillField.querySelector('input[name="skill"]').value =
        firstData || "";
    }

    // Add additional fields for the remaining data entries
    skillData.slice(1).forEach((data) => addSkillForm(data));

    // Dynamically add the "Add More" button
    //createAddMoreButton();
  };

  // Initialize the form with the given data
  populateSkillData();
  //createAddMoreButton();

  function createAddMoreProjectButton() {
    const addMoreProjectButton = document.createElement("button");
    addMoreProjectButton.id = "addMoreProjectButton";
    addMoreProjectButton.textContent = "Add More";
    addMoreProjectButton.addEventListener("click", () => addProjectForm());
    document
      .getElementById("projectsContainer")
      .appendChild(addMoreProjectButton);
  }

  // Function to add a new education form dynamically
  const addProjectForm = (data = {}) => {
    // Clone the first empty fieldset as a template
    const projectTemplate = document.querySelector(".project").cloneNode(true);

    // Clear any pre-filled values from the cloned template
    projectTemplate.querySelector('input[name="projectName"]').value =
      data.name || "";
    projectTemplate.querySelector('textarea[name="projectDescription"]').value =
      data.description || "";

    // Remove the existing "Add More" button
    const addMoreProjectButton = document.getElementById(
      "addMoreProjectButton"
    );
    if (addMoreProjectButton) {
      addMoreProjectButton.remove();
    }

    // Append the cloned template to the container
    const container = document.getElementById("projectsContainer");
    container.appendChild(projectTemplate);

    // Add the "Add More" button back at the end
    createAddMoreProjectButton();
  };

  // Function to populate data into the first field and create new fields if needed
  const populateProjectData = () => {
    const firstProjectField = document.querySelector(".project");
    const projectData = json_data.projects;

    // Populate the first field with the first entry in the data
    if (projectData.length > 0) {
      const firstData = projectData[0];
      firstProjectField.querySelector('input[name="projectName"]').value =
        firstData.name || "";
      firstProjectField.querySelector(
        'textarea[name="projectDescription"]'
      ).value = firstData.description || "";
    }

    // Add additional fields for the remaining data entries
    projectData.slice(1).forEach((data) => addProjectForm(data));

    // Dynamically add the "Add More" button
    //createAddMoreButton();
  };

  // Initialize the form with the given data
  populateProjectData();

  function createAddMoreCourseButton() {
    const addMoreCourseButton = document.createElement("button");
    addMoreCourseButton.id = "addMoreCourseButton";
    addMoreCourseButton.textContent = "Add More";
    addMoreCourseButton.addEventListener("click", () => addCourseForm());
    document
      .getElementById("coursesContainer")
      .appendChild(addMoreCourseButton);
  }

  // Function to add a new education form dynamically
  const addCourseForm = (data = {}) => {
    // Clone the first empty fieldset as a template
    const courseTemplate = document.querySelector(".course").cloneNode(true);

    // Clear any pre-filled values from the cloned template
    courseTemplate.querySelector('input[name="courseName"]').value =
      data.name || "";
    courseTemplate.querySelector('textarea[name="courseDescription"]').value =
      data.description || "";

    // Remove the existing "Add More" button
    const addMoreCourseButton = document.getElementById("addMoreCourseButton");
    if (addMoreCourseButton) {
      addMoreCourseButton.remove();
    }

    // Append the cloned template to the container
    const container = document.getElementById("coursesContainer");
    container.appendChild(courseTemplate);

    // Add the "Add More" button back at the end
    createAddMoreCourseButton();
  };

  // Function to populate data into the first field and create new fields if needed
  const populateCourseData = () => {
    const firstCourseField = document.querySelector(".course");
    const courseData = json_data.courses;

    // Populate the first field with the first entry in the data
    if (courseData.length > 0) {
      const firstData = courseData[0];
      firstCourseField.querySelector('input[name="courseName"]').value =
        firstData.name || "";
      firstCourseField.querySelector(
        'textarea[name="courseDescription"]'
      ).value = firstData.description || "";
    }

    // Add additional fields for the remaining data entries
    courseData.slice(1).forEach((data) => addCourseForm(data));

    // Dynamically add the "Add More" button
    //createAddMoreButton();
  };

  // Initialize the form with the given data
  populateCourseData();

  function createAddMoreCertificationButton() {
    const addMoreCertificationButton = document.createElement("button");
    addMoreCertificationButton.id = "addMoreCertificationButton";
    addMoreCertificationButton.textContent = "Add More";
    addMoreCertificationButton.addEventListener("click", () =>
      addCertificationForm()
    );
    document
      .getElementById("certificationContainer")
      .appendChild(addMoreCertificationButton);
  }

  // Function to add a new education form dynamically
  const addCertificationForm = (data = {}) => {
    // Clone the first empty fieldset as a template
    const certificationTemplate = document
      .querySelector(".certification")
      .cloneNode(true);

    // Clear any pre-filled values from the cloned template
    certificationTemplate.querySelector(
      'input[name="certificationName"]'
    ).value = data.name || "";
    certificationTemplate.querySelector(
      'textarea[name="certificationDescription"]'
    ).value = data.description || "";

    // Remove the existing "Add More" button
    const addMoreCertificationButton = document.getElementById(
      "addMoreCertificationButton"
    );
    if (addMoreCertificationButton) {
      addMoreCertificationButton.remove();
    }

    // Append the cloned template to the container
    const container = document.getElementById("certificationContainer");
    container.appendChild(certificationTemplate);

    // Add the "Add More" button back at the end
    createAddMoreCertificationButton();
  };

  const populateCertificationData = () => {
    const firstCertificationField = document.querySelector(".certification");
    const certificationData = json_data.certifications;

    // Populate the first field with the first entry in the data
    if (certificationData.length > 0) {
      const firstData = certificationData[0];
      firstCertificationField.querySelector(
        'input[name="certificationName"]'
      ).value = firstData.name || "";
      firstCertificationField.querySelector(
        'textarea[name="certificationDescription"]'
      ).value = firstData.description || "";
    }

    // Add additional fields for the remaining data entries
    certificationData.slice(1).forEach((data) => addCertificationForm(data));

    // Dynamically add the "Add More" button
    //createAddMoreButton();
  };

  // Initialize the form with the given data
  populateCertificationData();

  document
    .getElementById("parsedForm")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the form from submitting

      const formData = {}; // Initialize the object to store form data

      // General Information Section
      formData.generalInformation = {};
      const generalFields = document.querySelectorAll(".fieldList .fieldValue");
      generalFields.forEach((field) => {
        formData.generalInformation[field.name] = field.value;
      });

      // Skill Section
      formData.skills = [];
      const skillEntries = document.querySelectorAll("#skillsContainer .skill");
      skillEntries.forEach((entry) => {
        const skillData = {};
        const skillFields = entry.querySelectorAll(".skillField");
        skillFields.forEach((field) => {
          skillData[field.name] = field.value;
        });
        formData.skills.push(skillData);
      });

      // Education Section
      formData.education = [];
      const educationEntries = document.querySelectorAll(
        "#educationContainer .Education"
      );
      educationEntries.forEach((entry) => {
        const educationData = {};
        const educationFields = entry.querySelectorAll(".educationFieldValue");
        educationFields.forEach((field) => {
          educationData[field.name] = field.value;
        });
        formData.education.push(educationData);
      });

      // Experience Section
      formData.experience = [];
      const experienceEntries = document.querySelectorAll(
        "#experienceContainer .Experience"
      );
      experienceEntries.forEach((entry) => {
        const experienceData = {};

        // Normal fields
        const experienceFields = entry.querySelectorAll(
          ".experienceFieldValue"
        );
        experienceFields.forEach((field) => {
          experienceData[field.name] = field.value;
        });

        // Special fields (e.g., textarea)
        const specialField = entry.querySelector(
          ".specialexperienceFieldValue"
        );
        if (specialField) {
          experienceData.description = specialField.value;
        }

        formData.experience.push(experienceData);
      });

      // Projects Section
      formData.projects = [];
      const projectEntries = document.querySelectorAll(
        "#projectsContainer .project"
      );
      projectEntries.forEach((entry) => {
        const projectData = {};

        // Normal fields
        const projectFields = entry.querySelectorAll(".projectField");
        projectFields.forEach((field) => {
          projectData[field.name] = field.value;
        });

        // Special fields (e.g., textarea)
        const specialField = entry.querySelector(".specialProjectField");
        if (specialField) {
          projectData.description = specialField.value;
        }

        formData.projects.push(projectData);
      });

      // Courses Section
      formData.courses = [];
      const courseEntries = document.querySelectorAll(
        "#coursesContainer .course"
      );
      courseEntries.forEach((entry) => {
        const courseData = {};

        // Normal fields
        const courseFields = entry.querySelectorAll(".courseField");
        courseFields.forEach((field) => {
          courseData[field.name] = field.value;
        });

        // Special fields (e.g., textarea)
        const specialField = entry.querySelector(".specialCourseField");
        if (specialField) {
          courseData.description = specialField.value;
        }

        formData.courses.push(courseData);
      });

      // Projects Section
      formData.certifications = [];
      const certificationEntries = document.querySelectorAll(
        "#certificationContainer .certification"
      );
      certificationEntries.forEach((entry) => {
        const certificationData = {};

        // Normal fields
        const certificationFields = entry.querySelectorAll(
          ".certificationField"
        );
        certificationFields.forEach((field) => {
          certificationData[field.name] = field.value;
        });

        // Special fields (e.g., textarea)
        const specialField = entry.querySelector(".specialCertificationField");
        if (specialField) {
          certificationData.description = specialField.value;
        }

        formData.certifications.push(certificationData);
      });

      console.log("Collected Form Data:", formData);
      // You can now use `formData` for further processing or sending to the server
    });
}
