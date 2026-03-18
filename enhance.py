from http.server import BaseHTTPRequestHandler
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer

job_data = {
    "data scientist": "python machine learning pandas numpy statistics deep learning",
    "web developer": "html css javascript react node api frontend backend",
    "software engineer": "java c++ algorithms data structures system design",
    "data engineer": "python sql spark hadoop etl pipelines aws airflow"
}

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def extract_keywords(resume_text, job_text):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, job_text])
    feature_names = vectorizer.get_feature_names_out()
    job_vector = vectors.toarray()[1]

    top_indices = job_vector.argsort()[-10:]
    return [feature_names[i] for i in top_indices]

def enhance_resume(resume_text, job_role):
    resume_clean = preprocess(resume_text)
    job_text = job_data.get(job_role.lower(), "")

    if not job_text:
        return {"error": "Invalid role. Try: data scientist, web developer, software engineer"}

    job_clean = preprocess(job_text)

    keywords = extract_keywords(resume_clean, job_clean)
    missing = [kw for kw in keywords if kw not in resume_clean]

    score = round((len(keywords) - len(missing)) / len(keywords) * 100, 2)

    return {
        "summary": f"Strong {job_role} with skills in {', '.join(keywords[:5])}",
        "keywords": keywords,
        "missing": missing,
        "score": f"{score}%"
    }

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            resume = data.get("resume", "")
            role = data.get("role", "")

            result = enhance_resume(resume, role)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps({"error": str(e)}).encode())
