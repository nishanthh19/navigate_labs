# 🤖 AI Meeting Scheduler

An AI-powered meeting scheduler that sends RSVP-based email invites and handles responses using a Flask backend and email automation.

---

## 🌐 Features

- ✅ Accepts natural language dates like `tomorrow`, `next Monday`, `15 days later`, etc.
- 📧 Sends RSVP-based meeting invites with Accept/Decline links.
- 📨 Automatically updates RSVP status and logs them.
- 🔗 Sends a follow-up meeting link when a user accepts.
- 🌍 Works on local networks with full Flask endpoint URLs.
- 📁 Stores meeting details in `meeting_logs.json`.

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Flask**
- **dateparser** – for flexible date input
- **SMTP** – to send emails via `utils/email_sender.py`
- **JSON** – for logging and config

---

# 🛠️ Execution Instructions

To run the project, follow these steps:

### 1. Run the main Python application
Execute the following command in your terminal to run the main Python application (`app.py`):

```bash
python app.py

### 2. Run the Streamlit app
Execute the following command to start the Streamlit app (`streamlit_app.py`):

```bash
streamlit run streamlit_app.py



