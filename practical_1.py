# import streamlit as st
# import contextlib
# import io
# import random
# from datetime import datetime, timedelta
# import re
# import pandas as pd
# from streamlit_autorefresh import st_autorefresh

# st.set_page_config(page_title="Python Coding Exam", layout="wide")

# # Custom CSS to enable text selection and copying
# st.markdown(
#     """
#     <style>
#     * {
#         -webkit-user-select: text !important;
#         -moz-user-select: text !important;
#         -ms-user-select: text !important;
#         user-select: text !important;
#     }
#     textarea, pre, code, div {
#         -webkit-user-select: text !important;
#         -moz-user-select: text !important;
#         -ms-user-select: text !important;
#         user-select: text !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Lecturer credentials
# lecturer_credentials = {"Lecturer": "password123"}

# # Expected outputs and code patterns for marking
# expected_outputs = {
#     "List": "apple\nbanana\norange\nmango\npear\n",
#     "Function": "16\n",
#     "Set": "{1, 2, 3, 4}\n# Duplicates (2, 3) are removed as sets only keep unique elements\n",
#     "Dictionary": "Alice\nA\n",
#     "Tuple": "Java\n",
#     "If-Else": "Odd\n",
#     "For Loop": "1\n2\n3\n4\n5\n",
#     "While Loop": "1\n2\n3\n4\n5\n",
#     "List + Loop": "[4, 16, 36, 64]\n",
#     "Function + If-Else": "Not Positive\n"
# }

# code_patterns = {
#     "List": r"fruits\s*=\s*\[.*'apple'.*'banana'.*'orange'.*'mango'.*'pear'.*\].*for.*in.*fruits.*print",
#     "Function": r"def\s+square_number.*return.*\*\*2.*square_number\(4\)",
#     "Set": r"set\s*\(\[1,\s*2,\s*3,\s*4,\s*2,\s*3\]\).*#.*duplicates",
#     "Dictionary": r"dict\s*=\s*\{.*'name':\s*'Alice'.*'age':\s*20.*'grade':\s*'A'.*\}.*print.*dict\['name'\].*dict\['grade'\]",
#     "Tuple": r"tuple\s*=\s*\('Python',\s*'Java',\s*'C\+\+'\).*print.*tuple\[1\]",
#     "If-Else": r"num\s*=\s*7.*if.*num\s*%\s*2\s*==\s*0.*print.*['\"]Even['\"].*else.*print.*['\"]Odd['\"]", 
#     "For Loop": r"for.*in.*range\(1,\s*6\).*print",
#     "While Loop": r"num\s*=\s*1.*while.*num\s*<=.*5.*print.*num\s*\+=\s*1",
#     "List + Loop": r"numbers\s*=\s*\[2,\s*4,\s*6,\s*8\].*for.*in.*numbers.*\[.*\*\*2.*\].*print",
#     "Function + If-Else": r"def\s+is_positive.*if.*num\s*>.*0.*return.*['\"]Positive['\"].*else.*return.*['\"]Not Positive['\"].*is_positive\(-3\)"
# }

# # Session state initialization
# if "start_time" not in st.session_state:
#     st.session_state.start_time = None
# if "submitted" not in st.session_state:
#     st.session_state.submitted = False
# if "answers" not in st.session_state:
#     st.session_state.answers = {}
# if "scores" not in st.session_state:
#     st.session_state.scores = {}
# if "shuffled_questions" not in st.session_state:
#     st.session_state.shuffled_questions = []
# if "outputs" not in st.session_state:
#     st.session_state.outputs = {}
# if "current_question" not in st.session_state:
#     st.session_state.current_question = 0
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "student_id" not in st.session_state:
#     st.session_state.student_id = None
# if "timer_started" not in st.session_state:
#     st.session_state.timer_started = False
# if "timer_expired" not in st.session_state:
#     st.session_state.timer_expired = False
# if "lecturer_logged_in" not in st.session_state:
#     st.session_state.lecturer_logged_in = False

# # Reset login if session state is incomplete
# if st.session_state.logged_in and not all([st.session_state.student_id, st.session_state.shuffled_questions]):
#     st.session_state.logged_in = False
#     st.session_state.student_id = None
#     st.session_state.start_time = None
#     st.session_state.submitted = False
#     st.session_state.current_question = 0
#     st.session_state.answers = {}
#     st.session_state.outputs = {}
#     st.session_state.shuffled_questions = []
#     st.session_state.timer_started = False
#     st.session_state.timer_expired = False

# # Questions
# questions = [
#     ("List", "Create a list containing the names of five fruits (apple, banana, orange, mango, pear) and print each fruit on a separate line."),
#     ("Function", "Define a function named `square_number` that returns the square of a number. Call it with 4."),
#     ("Set", "Create a set using [1, 2, 3, 4, 2, 3]. Print the set and add a comment about duplicates."),
#     ("Dictionary", "Create a dictionary with keys: 'name', 'age', 'grade' with values 'Alice', 20, 'A'. Print name and grade."),
#     ("Tuple", "Create a tuple with ('Python', 'Java', 'C++'). Print the second item."),
#     ("If-Else", "Check if 7 is even or odd using if-else and print 'Even' or 'Odd'."),
#     ("For Loop", "Print numbers from 1 to 5 using a for loop."),
#     ("While Loop", "Print numbers from 1 to 5 using a while loop."),
#     ("List + Loop", "Square each number in [2, 4, 6, 8] using a for loop and print the resulting list."),
#     ("Function + If-Else", "Write a function is_positive(num). Return 'Positive' or 'Not Positive'. Test with -3.")
# ]

# # Timer display function
# def display_timer():
#     if st.session_state.start_time and not st.session_state.submitted and st.session_state.timer_started:
#         end_time = st.session_state.start_time + timedelta(minutes=20)
#         remaining_seconds = int((end_time - datetime.now()).total_seconds())
#         if remaining_seconds <= 0:
#             st.session_state.submitted = True
#             st.session_state.timer_expired = True
#         if st.session_state.timer_expired:
#             st.markdown("<h3 style='text-align: center; color: red;'>⏰ Time is up! Exam submitted.</h3>", unsafe_allow_html=True)
#             score = 0
#             for label, code in st.session_state.answers.items():
#                 if (code.strip() and 
#                     st.session_state.outputs.get(label) == expected_outputs.get(label) and 
#                     re.search(code_patterns.get(label), code.replace('\n', ' '), re.DOTALL)):
#                     score += 2
#             st.session_state.scores[st.session_state.student_id] = score
#         else:
#             minutes = remaining_seconds // 60
#             seconds = remaining_seconds % 60
#             st.markdown(
#                 f"<h3 style='text-align: center; color: red;'>⏳ Time Remaining: {minutes:02d}:{seconds:02d}</h3>",
#                 unsafe_allow_html=True
#             )

# # Sidebar role selection
# role = st.sidebar.selectbox("Select Role", ["Student", "Lecturer"])

# if role == "Student":
#     st.title("🧪 Python Coding Exam - Student Login")
    
#     if not st.session_state.logged_in:
#         with st.form(key="login_form"):
#             full_name = st.text_input("Enter your Full Name")
#             course_title = st.text_input("Enter your Course Title")
#             index_number = st.text_input("Enter your Index Number")
#             submit_login = st.form_submit_button("Start Exam")

#             if submit_login and full_name and course_title and index_number:
#                 st.session_state.logged_in = True
#                 st.session_state.student_id = f"{full_name} ({index_number}) - {course_title}"
#                 st.session_state.start_time = datetime.now()
#                 st.session_state.shuffled_questions = random.sample(questions, len(questions))  # Shuffle questions
#                 st.session_state.submitted = False
#                 st.session_state.current_question = 0
#                 st.session_state.answers = {}
#                 st.session_state.outputs = {}
#                 st.session_state.timer_started = False
#                 st.session_state.timer_expired = False
#                 st.success("Login successful! Starting exam...")

#     else:
#         # Enable auto-refresh only for student exam interface
#         st_autorefresh(interval=1000, limit=None, key="timer_refresh")
        
#         st.title(f"Welcome, {st.session_state.student_id.split(' (')[0]}")
        
#         # Logout button
#         if st.button("Logout"):
#             st.session_state.logged_in = False
#             st.session_state.student_id = None
#             st.session_state.start_time = None
#             st.session_state.submitted = False
#             st.session_state.current_question = 0
#             st.session_state.answers = {}
#             st.session_state.outputs = {}
#             st.session_state.shuffled_questions = []
#             st.session_state.timer_started = False
#             st.session_state.timer_expired = False
#             st.rerun()

#         with st.container():
#             # Start timer after rendering exam UI
#             st.session_state.timer_started = True
#             display_timer()

#         if not st.session_state.submitted:
#             label, instruction = st.session_state.shuffled_questions[st.session_state.current_question]
#             st.markdown(f"**Question {st.session_state.current_question + 1} of {len(st.session_state.shuffled_questions)}: {label}**")
#             st.write(instruction)
            
#             # Persistent code input
#             user_code = st.text_area(
#                 f"Write your code here:",
#                 value=st.session_state.answers.get(label, ""),
#                 height=200,
#                 key=f"code_{label}_{st.session_state.current_question}"
#             )
#             st.session_state.answers[label] = user_code

#             run = st.button(f"Run Code", key=f"run_{label}_{st.session_state.current_question}")

#             # Display persistent output
#             output_container = st.container()
#             with output_container:
#                 if run:
#                     output = io.StringIO()
#                     try:
#                         with contextlib.redirect_stdout(output):
#                             exec(user_code, {})
#                         st.session_state.outputs[label] = output.getvalue()
#                         st.success("✅ Code executed successfully!")
#                         st.code(st.session_state.outputs[label], language="python")
#                     except Exception as e:
#                         st.session_state.outputs[label] = str(e)
#                         st.error(f"❌ Error: {e}")
#                 elif label in st.session_state.outputs:
#                     # Redisplay previous output
#                     if "Error" in st.session_state.outputs[label]:
#                         st.error(f"❌ Error: {st.session_state.outputs[label]}")
#                     else:
#                         st.success("✅ Code executed successfully!")
#                         st.code(st.session_state.outputs[label], language="python")

#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.session_state.current_question > 0:
#                     if st.button("Previous Question"):
#                         st.session_state.current_question -= 1
#                         st.rerun()
#             with col2:
#                 if st.session_state.current_question < len(st.session_state.shuffled_questions) - 1:
#                     if st.button("Next Question"):
#                         st.session_state.current_question += 1
#                         st.rerun()

#             if st.session_state.current_question == len(st.session_state.shuffled_questions) - 1:
#                 if st.button("Submit Exam"):
#                     st.session_state.submitted = True
#                     st.rerun()

#         if st.session_state.submitted:
#             score = st.session_state.scores.get(st.session_state.student_id, 0)
#             if score == 0:
#                 for label, code in st.session_state.answers.items():
#                     if (code.strip() and 
#                         st.session_state.outputs.get(label) == expected_outputs.get(label) and 
#                         re.search(code_patterns.get(label), code.replace('\n', ' '), re.DOTALL)):
#                         score += 2
#                 st.session_state.scores[st.session_state.student_id] = score
#             st.success("✅ Your exam has been submitted!")
#             st.write(f"**Total Score:** {score} / 20")

# elif role == "Lecturer":
#     st.title("🔐 Lecturer Login")
    
#     if not st.session_state.lecturer_logged_in:
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")

#         if st.button("Login"):
#             if lecturer_credentials.get(username) == password:
#                 st.session_state.lecturer_logged_in = True
#                 st.success("Login successful.")
#                 st.rerun()
#             else:
#                 st.error("Invalid login credentials.")
#     else:
#         st.title("📊 Student Results Summary")
#         if st.button("Logout"):
#             st.session_state.lecturer_logged_in = False
#             st.rerun()

#         if st.session_state.scores:
#             st.write("### Scores of Submitted Students")
#             for student, score in st.session_state.scores.items():
#                 st.write(f"- **{student}**: {score} / 20")
#             # Download scores as CSV
#             scores_df = pd.DataFrame(
#                 list(st.session_state.scores.items()),
#                 columns=["Student ID", "Total Score"]
#             )
#             csv = scores_df.to_csv(index=False)
#             st.download_button(
#                 label="Download Scores as CSV",
#                 data=csv,
#                 file_name="student_scores.csv",
#                 mime="text/csv"
#             )
#         else:
#             st.info("No submissions yet.")


import streamlit as st
import contextlib
import io
import random
from datetime import datetime, timedelta
import re
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Python Coding Exam", layout="wide")

# Custom CSS to enable text selection and copying
st.markdown(
    """
    <style>
    * {
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
        user-select: text !important;
    }
    textarea, pre, code, div {
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
        user-select: text !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Lecturer credentials
lecturer_credentials = {"Lecturer": "password123"}

# Expected outputs and code patterns for marking
expected_outputs = {
    "List": "apple\nbanana\norange\nmango\npear\n",
    "Function": "16\n",
    "Set": "{1, 2, 3, 4}\n# Duplicates (2, 3) are removed as sets only keep unique elements\n",
    "Dictionary": "Alice\nA\n",
    "Tuple": "Java\n",
    "If-Else": "Odd\n",
    "For Loop": "1\n2\n3\n4\n5\n",
    "While Loop": "1\n2\n3\n4\n5\n",
    "List + Loop": "[4, 16, 36, 64]\n",
    "Function + If-Else": "Not Positive\n"
}

code_patterns = {
    "List": r"fruits\s*=\s*\[.*'apple'.*'banana'.*'orange'.*'mango'.*'pear'.*\].*for.*in.*fruits.*print",
    "Function": r"def\s+square_number.*return.*\*\*2.*square_number\(4\)",
    "Set": r"set\s*\(\[1,\s*2,\s*3,\s*4,\s*2,\s*3\]\).*#.*duplicates",
    "Dictionary": r"dict\s*=\s*\{.*'name':\s*'Alice'.*'age':\s*20.*'grade':\s*'A'.*\}.*print.*dict\['name'\].*dict\['grade'\]",
    "Tuple": r"tuple\s*=\s*\('Python',\s*'Java',\s*'C\+\+'\).*print.*tuple\[1\]",
    "If-Else": r"num\s*=\s*7.*if.*num\s*%\s*2\s*==\s*0.*print.*['\"]Even['\"].*else.*print.*['\"]Odd['\"]", 
    "For Loop": r"for.*in.*range\(1,\s*6\).*print",
    "While Loop": r"num\s*=\s*1.*while.*num\s*<=.*5.*print.*num\s*\+=\s*1",
    "List + Loop": r"numbers\s*=\s*\[2,\s*4,\s*6,\s*8\].*for.*in.*numbers.*\[.*\*\*2.*\].*print",
    "Function + If-Else": r"def\s+is_positive.*if.*num\s*>.*0.*return.*['\"]Positive['\"].*else.*return.*['\"]Not Positive['\"].*is_positive\(-3\)"
}

# Questions
questions = [
    ("List", "Create a list containing the names of five fruits (apple, banana, orange, mango, pear) and print each fruit on a separate line."),
    ("Function", "Define a function named `square_number` that returns the square of a number. Call it with 4."),
    ("Set", "Create a set using [1, 2, 3, 4, 2, 3]. Print the set and add a comment about duplicates."),
    ("Dictionary", "Create a dictionary with keys: 'name', 'age', 'grade' with values 'Alice', 20, 'A'. Print name and grade."),
    ("Tuple", "Create a tuple with ('Python', 'Java', 'C++'). Print the second item."),
    ("If-Else", "Check if 7 is even or odd using if-else and print 'Even' or 'Odd'."),
    ("For Loop", "Print numbers from 1 to 5 using a for loop."),
    ("While Loop", "Print numbers from 1 to 5 using a while loop."),
    ("List + Loop", "Square each number in [2, 4, 6, 8] using a for loop and print the resulting list."),
    ("Function + If-Else", "Write a function is_positive(num). Return 'Positive' or 'Not Positive'. Test with -3.")
]

# Session state initialization
if "user_sessions" not in st.session_state:
    st.session_state.user_sessions = {}
if "scores" not in st.session_state:
    st.session_state.scores = {}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_id" not in st.session_state:
    st.session_state.student_id = None
if "lecturer_logged_in" not in st.session_state:
    st.session_state.lecturer_logged_in = False

# Timer display function
def display_timer(student_id):
    user_session = st.session_state.user_sessions[student_id]
    if user_session["start_time"] and not user_session["submitted"] and user_session["timer_started"]:
        end_time = user_session["start_time"] + timedelta(minutes=20)
        remaining_seconds = int((end_time - datetime.now()).total_seconds())
        if remaining_seconds <= 0:
            user_session["submitted"] = True
            user_session["timer_expired"] = True
            score = 0
            for label, code in user_session["answers"].items():
                if (code.strip() and 
                    user_session["outputs"].get(label) == expected_outputs.get(label) and 
                    re.search(code_patterns.get(label), code.replace('\n', ' '), re.DOTALL)):
                    score += 2
            st.session_state.scores[student_id] = score
        if user_session["timer_expired"]:
            st.markdown("<h3 style='text-align: center; color: red;'>⏰ Time is up! Exam submitted.</h3>", unsafe_allow_html=True)
        else:
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            st.markdown(
                f"<h3 style='text-align: center; color: red;'>⏳ Time Remaining: {minutes:02d}:{seconds:02d}</h3>",
                unsafe_allow_html=True
            )

# Sidebar role selection
role = st.sidebar.selectbox("Select Role", ["Student", "Lecturer"])

if role == "Student":
    st.title("🧪 Python Coding Exam - Student Login")
    
    if not st.session_state.logged_in:
        with st.form(key="login_form"):
            full_name = st.text_input("Enter your Full Name")
            course_title = st.text_input("Enter your Course Title")
            index_number = st.text_input("Enter your Index Number")
            submit_login = st.form_submit_button("Start Exam")

            if submit_login and full_name and course_title and index_number:
                student_id = f"{full_name} ({index_number}) - {course_title}"
                st.session_state.student_id = student_id
                st.session_state.logged_in = True
                st.session_state.user_sessions[student_id] = {
                    "start_time": datetime.now(),
                    "submitted": False,
                    "answers": {},
                    "shuffled_questions": random.sample(questions, len(questions)),
                    "outputs": {},
                    "current_question": 0,
                    "timer_started": False,
                    "timer_expired": False
                }
                st.success("Login successful! Starting exam...")
                st.rerun()
    else:
        st_autorefresh(interval=5000, limit=None, key="timer_refresh")
        student_id = st.session_state.student_id
        user_session = st.session_state.user_sessions[student_id]
        st.title(f"Welcome, {student_id.split(' (')[0]}")
        
        # Logout button
        if st.button("Logout"):
            if student_id in st.session_state.user_sessions:
                del st.session_state.user_sessions[student_id]
            st.session_state.logged_in = False
            st.session_state.student_id = None
            st.rerun()

        with st.container():
            user_session["timer_started"] = True
            display_timer(student_id)

        if not user_session["submitted"]:
            label, instruction = user_session["shuffled_questions"][user_session["current_question"]]
            st.markdown(f"**Question {user_session['current_question'] + 1} of {len(user_session['shuffled_questions'])}: {label}**")
            st.write(instruction)
            
            # Persistent code input
            user_code = st.text_area(
                f"Write your code here:",
                value=user_session["answers"].get(label, ""),
                height=200,
                key=f"code_{label}_{user_session['current_question']}"
            )
            user_session["answers"][label] = user_code

            run = st.button(f"Run Code", key=f"run_{label}_{user_session['current_question']}")

            # Display persistent output
            output_container = st.container()
            with output_container:
                if run:
                    output = io.StringIO()
                    try:
                        with contextlib.redirect_stdout(output):
                            exec(user_code, {})
                        user_session["outputs"][label] = output.getvalue()
                        st.success("✅ Code executed successfully!")
                        st.code(user_session["outputs"][label], language="python")
                    except Exception as e:
                        user_session["outputs"][label] = str(e)
                        st.error(f"❌ Error: {e}")
                elif label in user_session["outputs"]:
                    if "Error" in user_session["outputs"][label]:
                        st.error(f"❌ Error: {user_session['outputs'][label]}")
                    else:
                        st.success("✅ Code executed successfully!")
                        st.code(user_session["outputs"][label], language="python")

            col1, col2 = st.columns(2)
            with col1:
                if user_session["current_question"] > 0:
                    if st.button("Previous Question"):
                        user_session["current_question"] -= 1
                        st.rerun()
            with col2:
                if user_session["current_question"] < len(user_session["shuffled_questions"]) - 1:
                    if st.button("Next Question"):
                        user_session["current_question"] += 1
                        st.rerun()

            if user_session["current_question"] == len(user_session["shuffled_questions"]) - 1:
                if st.button("Submit Exam"):
                    user_session["submitted"] = True
                    score = 0
                    for label, code in user_session["answers"].items():
                        if (code.strip() and 
                            user_session["outputs"].get(label) == expected_outputs.get(label) and 
                            re.search(code_patterns.get(label), code.replace('\n', ' '), re.DOTALL)):
                            score += 2
                    st.session_state.scores[student_id] = score
                    st.rerun()

        if user_session["submitted"]:
            score = st.session_state.scores.get(student_id, 0)
            st.success("✅ Your exam has been submitted!")
            st.write(f"**Total Score:** {score} / 20")

elif role == "Lecturer":
    st.title("🔐 Lecturer Login")
    
    if not st.session_state.lecturer_logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if lecturer_credentials.get(username) == password:
                st.session_state.lecturer_logged_in = True
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid login credentials.")
    else:
        st.title("📊 Student Results Summary")
        if st.button("Logout"):
            st.session_state.lecturer_logged_in = False
            st.rerun()

        if st.session_state.scores:
            st.write("### Scores of Submitted Students")
            for student, score in st.session_state.scores.items():
                st.write(f"- **{student}**: {score} / 20")
            # Download scores as CSV
            scores_df = pd.DataFrame(
                list(st.session_state.scores.items()),
                columns=["Student ID", "Total Score"]
            )
            csv = scores_df.to_csv(index=False)
            st.download_button(
                label="Download Scores as CSV",
                data=csv,
                file_name="student_scores.csv",
                mime="text/csv"
            )
        else:
            st.info("No submissions yet.")
