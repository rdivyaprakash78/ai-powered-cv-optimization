from flask import Flask, render_template,request, jsonify, redirect, url_for, session, Response
import json
from pdf_handling import extract_text
from structured_output import get_structured_output
from langchain_openai import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = str(os.environ.get("OPENAI_API_KEY"))
llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

app = Flask(__name__, template_folder= "Templates")
app.secret_key = "project-secret-key"

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/parser', methods=['GET', 'POST'])
def parser():
    return render_template('parser.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        cv = request.files["file"]
        cv.save("cv.pdf")
        file_path = os.path.join("./cv.pdf")
        content = extract_text(file_path)
        print(content)
        #data = get_structured_output(content, llm)
        #print(data)
        return_dict = {
            "redirect" : url_for("parser"),
            #"cv" : json.dumps(data["args"])
        }
        return jsonify(return_dict)


if __name__ == '__main__':
    app.run(debug=True)