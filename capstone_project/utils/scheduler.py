import datetime
import json
import os
import dateparser
from utils.email_sender import send_email
from utils.contact_map import resolve_emails_from_names

# Load config
with open("config.json") as f:
    config = json.load(f)

SENDER_EMAIL = config["sender_email"]
SENDER_PASSWORD = config["sender_password"]
LOG_FILE = "logs/meeting_logs.json"

def schedule_meetings(names_from_user, date, time, days):
    logs = []

    # Resolve names to email addresses
    emails = resolve_emails_from_names(names_from_user)
    if not emails:
        print("No valid emails resolved. Check contact names.")
        return

    # Parse the date (supports relative like 'tomorrow', 'next Monday')
    parsed_date = dateparser.parse(date)
    if not parsed_date:
        print("❌ Error parsing date:", date)
        return

    for i in range(days):
        scheduled_date = (
            parsed_date + datetime.timedelta(days=i)
        ).strftime("%Y-%m-%d")

        for email in emails:
            base_url = "http://localhost:5001"
            accept_link = f"{base_url}/rsvp/accept/{email}"
            decline_link = f"{base_url}/rsvp/decline/{email}"

            message = f"""\
Hi {email},

You're invited to a meeting on {scheduled_date} at {time}.

Please RSVP below:
✅ Accept: {accept_link}
❌ Decline: {decline_link}

Best,
AI Scheduler Bot
"""

            try:
                send_email(email, "Meeting Invite with RSVP", message, SENDER_EMAIL, SENDER_PASSWORD)
            except Exception as e:
                print(f"Failed to send email to {email}: {e}")

        logs.append({
            "emails": emails,
            "date": scheduled_date,
            "time": time,
            "rsvp": {email: None for email in emails}
        })

    # Save logs
    os.makedirs("logs", exist_ok=True)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r+") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
            existing.extend(logs)
            f.seek(0)
            json.dump(existing, f, indent=4)
            f.truncate()
    else:
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)


def update_rsvp_status(email, response, reason=None):
    """ Update RSVP status in logs; store reason for declines. """
    if not os.path.exists(LOG_FILE):
        print("No meeting logs found to update.")
        return

    with open(LOG_FILE, "r") as f:
        try:
            meeting_logs = json.load(f)
        except json.JSONDecodeError:
            print("❌ Could not parse meeting log file.")
            return

    for log in meeting_logs:
        if email in log.get("emails", []):
            if response == "accept":
                log["rsvp"][email] = "Accepted"
            elif response == "decline":
                log["rsvp"][email] = {"status": "Declined", "reason": reason}

    with open(LOG_FILE, "w") as f:
        json.dump(meeting_logs, f, indent=4)
