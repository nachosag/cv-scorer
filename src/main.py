from flask import Flask, request, render_template
import utils
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "src/uploads/"


@app.route("/")
def match_resume():
    return render_template("index.html")


@app.route("/matcher", methods=["POST"])
def matcher():
    if request.method == "POST":
        job_description = request.form["job_description"]
        resume_files = request.files.getlist("resumes")

        resumes = []
        for resume_file in resume_files:
            filename = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
            resume_file.save(filename)
            resumes.append(utils.extract_text(filename))

        if not resumes or not job_description:
            return render_template(
                "index.html",
                message="Please upload resumes and enter a job description.",
            )

        vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
        vectors = vectorizer.toarray()

        job_vector = vectors[0]
        resume_vectors = vectors[1:]
        similarities = cosine_similarity([job_vector], resume_vectors)[0]

        top_indices = similarities.argsort()[-5:][::-1]
        top_resumes = [resume_files[i].filename for i in top_indices]
        similarity_scores = [round(similarities[i], 2) for i in top_indices]

        return render_template(
            "index.html",
            message="Top matching resumes:",
            top_resumes=top_resumes,
            similarity_scores=similarity_scores,
        )


if __name__ == "__main__":
    app.run(debug=True)
