from flask import Flask, request, render_template
import utils
from matcher import load_spanish_model, find_words
import os


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "src/uploads/"


@app.route("/")
def match_resume():
    return render_template("index.html")


@app.route("/matcher", methods=["POST"])
def matcher():
    if request.method == "POST":
        raw_labels = request.form.get("labels", "")
        resumes = request.files.getlist("resumes")

        if not resumes or not raw_labels:
            return render_template(
                "index.html",
                message="Please upload resumes and enter a job description.",
            )

        labels = [label.strip() for label in raw_labels.split(",") if label.strip()]
        model = load_spanish_model()

        results = []
        for resume in resumes:
            filename = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
            resume.save(filename)
            text = utils.extract_text_from_pdf(filename)
            found = find_words(text, labels, model)
            results.append(found)

        return render_template(
            "index.html", message="Results:", resumes=resumes, results=results
        )


if __name__ == "__main__":
    app.run(debug=True)
