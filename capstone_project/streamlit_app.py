import streamlit as st
from utils.groq_interface import extract_meeting_info
from utils.scheduler import schedule_meetings

st.set_page_config(page_title="AI Meeting Scheduler (Groq)", layout="centered")

st.title("🤖 AI Meeting Scheduler (Groq)")
st.markdown("Enter a natural language prompt to schedule meetings:")

# Text input area
prompt = st.text_area("📝 Your scheduling request", height=150)

# On Submit
if st.button("📤 Submit"):
    if not prompt.strip():
        st.error("Please enter a scheduling prompt.")
    else:
        st.info("Parsing your request using Groq...")
        result = extract_meeting_info(prompt.strip())

        if result.get("error"):
            st.error(f"Parsing Error: {result['error']}")
        else:
            st.success("Prompt parsed successfully!")
            st.json(result)

            st.info("Sending meeting invites...")
            try:
                emails = result["emails"]
                date = result["date"]
                time = result["time"]
                days = result["days"]

                schedule_meetings(emails, date, time, days)
                st.success("✅ Meeting invites sent successfully!")
            except Exception as e:
                st.error(f"Scheduling error: {str(e)}")
