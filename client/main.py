import os
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from io import BytesIO
import re
from dotenv import load_dotenv

load_dotenv()

# CONFIG
BACKEND_URL = os.getenv("BACKEND_URL")
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

st.set_page_config(
    page_title="EduSmart AI",
    page_icon="🎓",
    layout="wide",
)

# Get background image
BACKGROUND_IMAGE = os.path.join(ASSETS_DIR, "landing-page.jpg")

if os.path.exists(BACKGROUND_IMAGE):
    import base64
    with open(BACKGROUND_IMAGE, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    BACKGROUND_CSS = f"url(data:image/jpeg;base64,{img_base64})"
else:
    BACKGROUND_CSS = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"

# CUSTOM CSS
st.markdown(f"""
<style>
    /* Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Full page background */
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                    {BACKGROUND_CSS};
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Glass card */
    .glass-card {{
        background: rgba(20, 20, 30, 0.85);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem auto;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        max-width: 600px;
        width: 100%;
    }}
    
    /* Purple input fields for login and signup */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)) !important;
        background-color: rgba(102, 126, 234, 0.15) !important;
        color: white !important;
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.5) !important;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }}
    
    /* Input focus effect */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus {{
        border: 1px solid #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3) !important;
        background-color: rgba(102, 126, 234, 0.25) !important;
    }}
    
    /* Input labels */
    .stTextInput > label,
    .stTextArea > label,
    .stNumberInput > label,
    .stSelectbox > label {{
        color: white !important;
        font-weight: 500;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }}
    
    /* Placeholder text color */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {{
        color: rgba(255, 255, 255, 0.5) !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        max-width: 400px;
        margin: 0 auto;
        display: block;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }}
    
    /* Chat input */
    .stChatInput > div > div > textarea {{
        background-color: #f5f5f5 !important;
        color: #1a1a2e !important;
        border-radius: 10px;
    }}
    
    /* Chat messages */
    .stChatMessage {{
        background: rgba(245, 245, 245, 0.95) !important;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.8rem 0;
        color: #1a1a2e !important;
    }}
    
    .stChatMessage p, .stChatMessage div {{
        color: #1a1a2e !important;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: rgba(20, 20, 30, 0.95);
        backdrop-filter: blur(10px);
    }}
    
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.5rem;
        justify-content: center;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        color: white;
        font-weight: 500;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }}
    
    /* Headers and text */
    h1, h2, h3, h4, p, li, div {{
        color: white !important;
        text-align: center;
    }}
    
    /* Lists */
    ul {{
        padding-left: 0;
        list-style: none;
        text-align: center;
    }}
    
    li {{
        margin: 0.7rem 0;
        font-size: 1rem;
        text-align: center;
    }}
    
    /* Form styling */
    .stForm {{
        background: transparent;
    }}
    
    /* Center content */
    .block-container {{
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 2rem;
        margin: 0 auto;
    }}
    
    /* File uploader */
    .stFileUploader > div {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        max-width: 500px;
        margin: 0 auto;
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
    }}
    
    /* Cursor */
    input, textarea {{
        caret-color: #667eea !important;
    }}
    
    /* Number input styling */
    .stNumberInput input {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)) !important;
        color: white !important;
    }}
    
    /* Selectbox styling */
    .stSelectbox select {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)) !important;
        color: white !important;
    }}
</style>
""", unsafe_allow_html=True)

# SESSION STATE INIT
def init_state():
    defaults = {
        "page": "landing",
        "authenticated": False,
        "username": "",
        "password": "",
        "role": "",
        "grade": 0,
        "chat_messages": [],
        "generated_quiz": None,
        "quiz_result": None,
        "quiz_history": None,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

init_state()

# HELPERS
def auth():
    return HTTPBasicAuth(st.session_state.username, st.session_state.password)

def api(method, path, **kwargs):
    return requests.request(method, f"{BACKEND_URL}{path}", auth=auth(), timeout=60, **kwargs)

def logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]

# LANDING PAGE
def landing_page():
    st.markdown("""
    <div class="glass-card">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">🎓 EduSmart AI</h1>
        <h3 style="margin-bottom: 1.5rem;">Your Personal AI Learning Assistant</h3>
        <p style="font-size: 1rem; margin-bottom: 2rem;">
            Upload your study materials and let AI help you learn better!
        </p>
        <div style="margin: 1.5rem 0;">
            <div style="margin-bottom: 0.8rem;">📚 Upload textbooks & notes</div>
            <div style="margin-bottom: 0.8rem;">💬 Ask questions & get answers</div>
            <div style="margin-bottom: 0.8rem;">📝 Generate practice quizzes</div>
            <div style="margin-bottom: 0.8rem;">📊 Track your progress</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.page = "signup"
    with col2:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.page = "login"

# LOGIN PAGE
def login_page():
    st.markdown("""
    <div class="glass-card">
        <h2 style="text-align: center; margin-bottom: 2rem;">🔐 Welcome Back</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                r = requests.get(f"{BACKEND_URL}/login", auth=HTTPBasicAuth(username, password))
                if r.status_code == 200:
                    data = r.json()
                    st.session_state.update({
                        "authenticated": True,
                        "username": username,
                        "password": password,
                        "role": data["role"],
                        "grade": data.get("grade", 0),
                        "page": "app",
                    })
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.page = "landing"

# SIGNUP PAGE
def signup_page():
    st.markdown("""
    <div class="glass-card">
        <h2 style="text-align: center; margin-bottom: 2rem;">✍️ Create Account</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        role = st.selectbox("I am a", ["Student", "Teacher"])
        
        with st.form("signup_form"):
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email", placeholder="Enter your email")
            username = st.text_input("Username", placeholder="Choose a username")
            password = st.text_input("Password", type="password", placeholder="Choose a password")
            
            if role == "Student":
                grade = st.number_input("Grade", 1, 12, step=1)
                school = st.text_input("School", placeholder="Enter your school name")
            
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            
            if submitted:
                endpoint = "/signup/student" if role == "Student" else "/signup/teacher"
                payload = {"fullname": full_name, "email": email, "username": username, "password": password}
                if role == "Student":
                    payload.update({"grade": grade, "school": school})
                else:
                    payload.update({"school": "N/A"})
                
                r = requests.post(f"{BACKEND_URL}{endpoint}", json=payload)
                if r.status_code == 200:
                    st.success("Account created! Please login.")
                else:
                    st.error(r.text)
        
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.page = "landing"

# TEACHER DASHBOARD
def teacher_dashboard():
    st.markdown("""
    <div class="glass-card">
        <h2 style="text-align: center; margin-bottom: 1rem;">📚 Upload Study Materials</h2>
        <p style="text-align: center; margin-bottom: 2rem;">Share your knowledge with students</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pdf = st.file_uploader("📄 Select PDF Document", type="pdf")
        grade = st.number_input("📊 Grade Level", 1, 12)
        
        if st.button("🚀 Upload Document", use_container_width=True, disabled=not pdf):
            with st.spinner("Processing..."):
                files = {"file": (pdf.name, BytesIO(pdf.getvalue()), "application/pdf")}
                data = {"grade": str(int(grade))}
                r = api("POST", "/upload_docs", files=files, data=data)
                if r.status_code == 200:
                    st.success("✅ Document uploaded successfully!")
                    st.balloons()
                else:
                    st.error("❌ Upload failed")

# STUDENT DASHBOARD
def student_dashboard():
    st.markdown(f"""
    <div class="glass-card">
        <h2 style="text-align: center;">🎓 Welcome, {st.session_state.username}!</h2>
        <p style="text-align: center;">Ask questions, take quizzes, and learn smarter with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    chat_tab, quiz_tab, history_tab = st.tabs(["💬 Ask & Learn", "📝 Practice Quiz", "📜 Your Progress"])
    
    # CHAT TAB
    with chat_tab:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 Ask Your AI Tutor")
        st.markdown("Have questions about your studies? Ask anything and get instant answers!")
        
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if prompt := st.chat_input("Type your question here... e.g., 'Explain photosynthesis'"):
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    r = api("POST", "/chat", json={"query": prompt})
                    if r.status_code == 200:
                        data = r.json()
                        answer = data["answer"]
                        if data["sources"]:
                            answer += f"\n\n📚 **Source:** {', '.join(data['sources'])}"
                        st.markdown(answer)
                        st.session_state.chat_messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error("Sorry, I couldn't answer that. Please try again.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # QUIZ TAB
    with quiz_tab:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Test Your Knowledge")
        
        if st.session_state.generated_quiz is None:
            topic = st.text_input("📚 Topic", placeholder="e.g., Python, History, Biology")
            num_q = st.slider("Number of Questions", 1, 10, 3)
            
            if st.button("🎯 Generate Quiz", use_container_width=True, disabled=not topic):
                with st.spinner("Creating your quiz..."):
                    r = api("POST", "/quiz", json={"topic": topic, "num_questions": num_q})
                    if r.status_code == 200:
                        st.session_state.generated_quiz = r.json()
                        st.session_state.generated_quiz["topic"] = topic
                        st.session_state.quiz_result = None
                        st.rerun()
                    else:
                        st.error("Failed to generate quiz")
        else:
            quiz = st.session_state.generated_quiz
            raw = quiz["quiz"]
            
            blocks = re.split(r"(Question \d+:)", raw)[1:]
            questions = []
            for i in range(0, len(blocks), 2):
                lines = blocks[i + 1].strip().split("\n")
                q_text = lines[0]
                options = [l for l in lines if re.match(r"[A-Z]\)", l)]
                questions.append({"q": q_text, "opts": options})
            
            st.markdown(f"### 📖 Topic: {quiz['topic']}")
            
            with st.form("quiz_form"):
                answers = []
                for i, q in enumerate(questions):
                    st.markdown(f"**Q{i+1}. {q['q']}**")
                    choice = st.radio(
                        "Select answer:",
                        [o[0] for o in q["opts"]],
                        format_func=lambda x: next(o for o in q["opts"] if o.startswith(x)),
                        key=f"quiz_q{i}",
                    )
                    answers.append(choice)
                
                submitted = st.form_submit_button("✅ Submit Quiz", use_container_width=True)
            
            if submitted:
                with st.spinner("Evaluating..."):
                    r = api("POST", "/quiz/check", json={"quiz_id": quiz["quiz_id"], "answers": answers})
                    if r.status_code == 200:
                        st.session_state.quiz_result = r.json()
                        st.session_state.generated_quiz = None
                        st.rerun()
                    else:
                        st.error("Failed to submit")
        
        if st.session_state.quiz_result:
            res = st.session_state.quiz_result
            score_percent = int((res["score"] / res["total"]) * 100)
            st.success(f"🎉 Score: {res['score']}/{res['total']} ({score_percent}%)")
            
            for r in res["results"]:
                status = "✅" if r["is_correct"] else "❌"
                st.markdown(f"**{status} Q{r['question_number']}**")
                st.markdown(f"Your answer: {r['user_answer']}")
                st.markdown(f"Correct: {r['correct_answer']}")
            
            if st.button("🔄 New Quiz", use_container_width=True):
                st.session_state.quiz_result = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # HISTORY TAB
    with history_tab:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Your Learning Progress")
        
        if st.button("📈 Load My History", use_container_width=True):
            with st.spinner("Loading..."):
                r = api("GET", "/quiz/history")
                if r.status_code == 200:
                    st.session_state.quiz_history = r.json()["history"]
                    st.success("History loaded!")
                else:
                    st.error("No history found")
        
        history = st.session_state.quiz_history
        if history:
            for attempt in history:
                score = attempt["score"]
                total = attempt["total"]
                percent = int((score / total) * 100)
                
                with st.expander(f"📚 {attempt['topic']} — {score}/{total} ({percent}%)"):
                    raw_quiz = attempt["quiz_content"]
                    blocks = re.split(r"(Question \d+:)", raw_quiz)[1:]
                    parsed = []
                    for i in range(0, len(blocks), 2):
                        lines = blocks[i + 1].strip().split("\n")
                        parsed.append({
                            "question": lines[0],
                            "options": [l for l in lines if re.match(r"[A-Z]\)", l)]
                        })
                    
                    for i, res in enumerate(attempt["results"]):
                        q = parsed[i]
                        st.markdown(f"**Q{i+1}: {q['question']}**")
                        for opt in q["options"]:
                            letter = opt[0]
                            if letter == res["correct_answer"]:
                                st.markdown(f"✅ {opt}")
                            elif letter == res["user_answer"]:
                                st.markdown(f"❌ {opt}")
                            else:
                                st.markdown(f"   {opt}")
                        st.divider()
        else:
            st.info("📝 No quiz history yet. Take a quiz to see your progress!")
        st.markdown('</div>', unsafe_allow_html=True)

# ROUTER
if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "app":
    st.sidebar.markdown("<h2 style='text-align: center;'>🎓 EduSmart AI</h2>", unsafe_allow_html=True)
    st.sidebar.success(f"👋 **{st.session_state.username}**\n\n📌 Role: **{st.session_state.role}**")
    
    if st.session_state.role == "Student" and st.session_state.grade:
        st.sidebar.info(f"📚 Grade: {st.session_state.grade}")
    
    st.sidebar.markdown("---")
    st.sidebar.button("🚪 Logout", on_click=logout, use_container_width=True)
    
    if st.session_state.role == "Teacher":
        teacher_dashboard()
    else:
        student_dashboard()