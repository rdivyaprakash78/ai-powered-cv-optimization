const file = document.getElementById("fileInput");
const valid_type = "application/pdf";
const error_message = document.getElementById("remark");
const file_data = document.getElementById("cv");
let parsed_cv = "";
const currentPage = window.location.pathname;

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
          parsed_cv = data.cv;
          localStorage.setItem("parsed_cv", parsed_cv);
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
  parsed_cv = localStorage.getItem("parsed_cv");
  let structured_cv = JSON.parse(parsed_cv);
  file_data.innerHTML = structured_cv.name;
}
