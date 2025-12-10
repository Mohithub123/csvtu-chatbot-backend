from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# 🔑 Put your REAL Gemini API key here (or set ENV variable GEMINI_API_KEY)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or "AIzaSyBJ1mn36NYsz3HccY52J8nOBMRfwbrZ5x4"

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
PRIMARY_MODEL = "gemini-2.0-flash"   # or whichever model you are using


# -----------------------------------------
# Helper: function to talk to Gemini
# -----------------------------------------
def ask_gemini(model_name: str, message: str) -> str:
    url = f"{BASE_URL}/{model_name}:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": message}
                ]
            }
        ]
    }

    resp = requests.post(url, json=payload, timeout=30)
    data = resp.json()
    print(f"Gemini raw response ({model_name}):", data)

    if resp.status_code != 200 or "error" in data:
        raise RuntimeError(f"Gemini error: {data.get('error')}")

    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    text = "\n".join(p.get("text", "") for p in parts).strip()
    return text or "I could not generate a reply from the AI model."


# ------------------------------
#  Main Chat Endpoint (/chat)
# ------------------------------
@app.route("/chat", methods=["POST"])
@app.route("/api/chat", methods=["POST"])  # optional alias
def chat():
    data = request.get_json() or {}
    user_msg = (data.get("message") or "").strip()

    if not user_msg:
        return jsonify({"reply": "Please type a message before sending."}), 200

    lower = user_msg.lower()
    words = lower.split()

    # ========== SPECIAL CSVTU HANDLERS (STATIC TEXT IN ENGLISH) ==========

    # VC NAME
    ask_vc_name = (
        ("vc" in words or "vice chancellor" in lower)
        and ("name" in words or "who is" in lower)
    )
    if ask_vc_name:
        reply = """
Vice-Chancellor of CSVTU ✅

Dr. Arun Arora  
Vice-Chancellor  
Chhattisgarh Swami Vivekanand Technical University, Bhilai (C.G.)

Official Profile:
https://csvtu.ac.in/ew/honble-vice-chancellor/
""".strip()
        return jsonify({"reply": reply})

    # DIGIVARSITY / STUDENT PORTAL
    ask_digivarsity = (
        "digivarsity" in lower
        or "digi varsit" in lower
        or "digiversity" in lower
        or "digvarsity" in lower
        or "student portal" in lower
        or "exam form" in lower
        or "sem form" in lower
        or "student login" in lower
        or "csvtu login" in lower
    )
    if ask_digivarsity:
        reply = """
CSVTU Digivarsity – Student Portal (Official)

You can use this portal for:
• Exam forms  
• Student login  
• Admission / enrollment details  
• Password reset  
• Ph.D application  

Official Link:  
https://csvtu.digivarsity.online/CSVTU/index.aspx
""".strip()
        return jsonify({"reply": reply})

    # E-LIBRARY
    if (
        "e library" in lower
        or "elibrary" in lower
        or "e-library" in lower
        or "library link" in lower
        or "online library" in lower
        or "digital library" in lower
    ):
        reply = """
CSVTU E-Library (Official) 📚

• Online resources and e-books  
• E-Library login and related notices are available on this page  

Direct official link:
https://csvtu.ac.in/ew/e-library/
""".strip()
        return jsonify({"reply": reply})

    # RESULTS
    if (
        "result" in lower
        or "marksheet" in lower
        or "supply" in lower
        or "supplementary" in lower
        or "rt " in lower
        or "rv " in lower
        or "rrv" in lower
    ):
        reply = """
CSVTU Results Page (Official)

• RT / RV / RRV / Regular / Supplementary results  
• You can check results using your roll number  

👉 https://csvtu.ac.in/ew/results-rtrvrrv/
""".strip()
        return jsonify({"reply": reply})

    # TIME TABLE
    if (
        "time table" in lower
        or "timetable" in lower
        or "exam time table" in lower
        or "datesheet" in lower
        or "date sheet" in lower
        or "exam date" in lower
        or "exam schedule" in lower
    ):
        reply = """
CSVTU Examination Time Table (Official)

• Time tables for BE, B.Tech, Diploma, M.Tech, MBA, MCA, Pharmacy, etc.  
• Click on the course name (blue bar) to view semester-wise time tables  

👉 https://csvtu.ac.in/ew/examination-time-table/
""".strip()
        return jsonify({"reply": reply})

    # ACADEMIC CALENDAR
    if (
        "academic calendar" in lower
        or ("calendar" in lower and "academic" in lower)
        or "semester calendar" in lower
        or "holiday list" in lower
    ):
        reply = """
CSVTU Academic Calendar (Official)

• Semester-wise academic calendar  
• Holidays, exam periods, session dates  

👉 https://csvtu.ac.in/ew/academic-calendar/
""".strip()
        return jsonify({"reply": reply})

    # EXAM FORM
    if (
        "exam form" in lower
        or "examination form" in lower
        or "online exam form" in lower
        or "exam registration" in lower
    ):
        reply = """
CSVTU Online Examination Form (Official)

• Online exam form filling for students  
• Institute login and help manual are also available on this page  

👉 https://csvtu.ac.in/ew/examination-form-2016/
""".strip()
        return jsonify({"reply": reply})

    # NOTICES
    if (
        "notice" in lower
        or "notices" in lower
        or "latest notice" in lower
        or "corrigendum" in lower
        or "advertisement" in lower
        or "vacancy" in lower
    ):
        reply = """
CSVTU Notices (Official)

• Latest university notices  
• Exam, recruitment, corrigendum and other updates  

👉 https://csvtu.ac.in/ew/notices/
""".strip()
        return jsonify({"reply": reply})

    # TENDERS
    if (
        "tender" in lower
        or "tenders" in lower
        or "e-tender" in lower
    ):
        reply = """
CSVTU Tenders (Official)

• Active university tenders  
• Tender documents and last dates  

👉 https://csvtu.ac.in/ew/tenders/
""".strip()
        return jsonify({"reply": reply})

    # NEWSLETTER
    if (
        "newsletter" in lower
        or "pravah" in lower
    ):
        reply = """
CSVTU Newsletter – "Pravah" (Official)

👉 https://csvtu.ac.in/ew/newsletter/
""".strip()
        return jsonify({"reply": reply})

    # SENIORITY LIST
    if "seniority list" in lower:
        reply = """
CSVTU Seniority List (Teaching / Non-Teaching)

👉 https://csvtu.ac.in/ew/seniority-list/
""".strip()
        return jsonify({"reply": reply})

    # MERIT LIST
    if "merit list" in lower:
        reply = """
CSVTU Merit List (Different sessions and courses)

👉 https://csvtu.ac.in/ew/merit-list/
""".strip()
        return jsonify({"reply": reply})

    # CSDIE – SKILL DEVELOPMENT
    if (
        "csdie" in lower
        or "skill development" in lower
        or "skill centre" in lower
    ):
        reply = """
Centre for Skill Development and Informal Education (CSDIE) – CSVTU

👉 https://csvtu.ac.in/ew/centre-for-skill-development-and-informal-education-csdie/
""".strip()
        return jsonify({"reply": reply})

    # UTD MAIN PAGE
    if (
        "utd" in lower
        or "university teaching department" in lower
    ):
        reply = """
CSVTU University Teaching Department (UTD) – Main Page

👉 https://csvtu.ac.in/ew/university-teaching-department/
""".strip()
        return jsonify({"reply": reply})

    # PLACEMENT CELL (CPC)
    if (
        "cpc" in lower
        or "placement" in lower
        or "training and placement" in lower
    ):
        reply = """
CSVTU Centralized Placement Cell (CPC)

👉 https://csvtu.ac.in/ew/centralized-placement-cell-cpc/
""".strip()
        return jsonify({"reply": reply})

    # GRIEVANCE CELL
    if (
        "grievance" in lower
        or "complaint" in lower
        or "ragging" in lower
        or "problem" in lower
    ):
        reply = """
CSVTU Grievance Cell – Online Complaint Portal

👉 https://csvtu.ac.in/ew/grievance-cell/
""".strip()
        return jsonify({"reply": reply})

    # CONTACT US
    if (
        "contact" in lower
        or "helpline" in lower
        or "phone" in lower
        or "email" in lower
    ) and ("csvtu" in lower or "university" in lower):
        reply = """
CSVTU Official Contact Details 📞

👉 https://csvtu.ac.in/ew/contact-us/
""".strip()
        return jsonify({"reply": reply})

    # ORDINANCES
    if "ordinance" in lower or "ordinances" in lower:
        reply = """
CSVTU Ordinances & Amendments (Rules and Regulations)

👉 https://csvtu.ac.in/ew/the-university/ordinances/
""".strip()
        return jsonify({"reply": reply})

    # PROGRAMS & SCHEMES / SYLLABUS
    if (
        "scheme" in lower
        or "schemes" in lower
        or "syllabus" in lower
        or "curriculum" in lower
        or "programs and schemes" in lower
    ):
        reply = """
CSVTU "Programs and Schemes" (Scheme and Syllabus)

👉 https://csvtu.ac.in/ew/programs-and-schemes/

From here you can open scheme and syllabus PDFs for Diploma, B.Tech, M.Tech, MBA,
Pharmacy and other programmes.
""".strip()
        return jsonify({"reply": reply})

    # OFFICIAL WEBSITE
    if (
        "official website" in lower
        or "official site" in lower
        or "csvtu website" in lower
    ):
        reply = """
CSVTU Official Website ✅

https://csvtu.ac.in
""".strip()
        return jsonify({"reply": reply})

    # ABOUT CSVTU
    if (
        "about csvtu" in lower
        or "about university" in lower
        or "csvtu information" in lower
    ):
        reply = """
About CSVTU (Chhattisgarh Swami Vivekanand Technical University)

• State Government Technical University of Chhattisgarh  
• Main campus at Newai, Bhilai (District Durg)  
• Fields: Engineering, Technology, Architecture, Pharmacy, Management, MCA and Diploma  
• Many Engineering / Diploma / Pharmacy / MBA / MCA / M.Tech colleges are affiliated to CSVTU  
• UTD Bhilai runs B.Tech (Honours), M.Tech / M.Plan and Diploma programmes.
""".strip()
        return jsonify({"reply": reply})

    # JOURNALS
    if (
        "csvtu journal" in lower
        or "csvtu journals" in lower
        or "research journal" in lower
    ):
        reply = """
CSVTU Journals (Official Research Journals Portal)

👉 https://csvtujournal.in
""".strip()
        return jsonify({"reply": reply})

    # MoUs
    if "mou" in lower or "mous" in lower:
        reply = """
CSVTU Memorandum of Understanding (MoUs)

👉 https://csvtu.ac.in/ew/memorandum-of-understanding-mous/
""".strip()
        return jsonify({"reply": reply})

    # Ph.D Information
    if (
        "phd" in lower
        and ("information" in lower or "admission" in lower or "notice" in lower)
    ):
        reply = """
CSVTU Ph.D Information – Official Page

👉 https://csvtu.ac.in/ew/research/phd-information/
""".strip()
        return jsonify({"reply": reply})

    # ====================== FALLBACK → GEMINI (ENGLISH ONLY) ======================

    try:
        prompt = f"""
You are a university information chatbot for CSVTU (Chhattisgarh Swami Vivekanand Technical University).

User question: {user_msg}

Rules:
- Answer ONLY in English (no Hindi or Hinglish).
- If you know an official CSVTU link, include it.
- If you are not sure about a fact, do NOT guess.
- Prefer short, clear bullet points (3–6 lines).
"""

        ai_answer = ask_gemini(PRIMARY_MODEL, prompt)
        return jsonify({"reply": ai_answer})
    except Exception as e:
        print("Gemini Error (unexpected):", e)
        return jsonify({
            "reply": "There is a server-side problem. Please try again later."
        }), 200


if __name__ == "__main__":
    # Run on 0.0.0.0 so emulator / mobile on same Wi-Fi can reach it
    app.run(host="0.0.0.0", port=5000)
