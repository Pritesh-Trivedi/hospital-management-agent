import os
import pandas as pd
from datetime import datetime
from config import DATA_DIR, get_env

def generate_notification_id():

    notifications = pd.read_csv(DATA_DIR / "notifications.csv")

    if len(notifications) == 0:
        return "N1001"

    last_id = notifications.iloc[-1]["notification_id"]

    number = int(last_id[1:])

    return f"N{number + 1}"
def create_notification(state):

    notifications = pd.read_csv(DATA_DIR / "notifications.csv")

    notification_id = generate_notification_id()

    new_notification = {

        "notification_id": notification_id,

        "patient_id": state["patient_id"],

        "patient_name": state["patient_name"],

        "doctor": state["assigned_doctor"],

        "ward": state["ward"],

        "message": f"Patient should report to {state['ward']} ward under {state['assigned_doctor']}.",

        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "status": "Pending"

    }

    notifications = pd.concat(
        [notifications, pd.DataFrame([new_notification])],
        ignore_index=True
    )

    notifications.to_csv(DATA_DIR / "notifications.csv", index=False)

    return notification_id


def send_email_notification(state):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    recipient = state.get("email")
    if not recipient or not str(recipient).strip():
        return False, "No email address provided"

    recipient = str(recipient).strip()
    patient_name = state.get("patient_name", "Patient")
    hospital_name = state.get("hospital_name", "Hospital")
    hospital_address = state.get("hospital_address", "")
    ward = state.get("ward", "General")
    priority = state.get("priority", "Medium")
    doctor = state.get("assigned_doctor", "Duty Doctor")
    next_slot = state.get("next_slot", "N/A")
    token_number = state.get("token_number", "N/A")
    consultation_room = state.get("consultation_room", "N/A")
    queue_pos = state.get("queue_position", 1)
    wait_min = state.get("estimated_wait_minutes", 0)
    guidance = state.get("guidance", "Please arrive 15 minutes before your scheduled slot.")
    patient_id = state.get("patient_id", "N/A")

    subject = f"🏥 Triage Confirmation - {hospital_name} (Token: {token_number})"

    html_content = f"""
    <html>
    <head>
      <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; background-color: #f8fafc; padding: 20px; }}
        .card {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
        .header {{ border-bottom: 2px solid #3b82f6; padding-bottom: 12px; margin-bottom: 20px; }}
        .header h2 {{ margin: 0; color: #1e40af; font-size: 22px; }}
        .badge {{ display: inline-block; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 13px; margin-right: 8px; }}
        .badge-emergency {{ background: #fee2e2; color: #991b1b; }}
        .badge-general {{ background: #dbeafe; color: #1e40af; }}
        .badge-high {{ background: #fef3c7; color: #92400e; }}
        .detail-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f1f5f9; }}
        .label {{ font-weight: 600; color: #64748b; }}
        .value {{ color: #0f172a; font-weight: 500; }}
        .guidance-box {{ background: #f0fdf4; border-left: 4px solid #22c55e; padding: 12px; margin-top: 16px; border-radius: 4px; }}
        .footer {{ margin-top: 24px; font-size: 12px; color: #94a3b8; text-align: center; }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="header">
          <h2>🏥 Hospital Triage Confirmation</h2>
          <p style="margin:4px 0 0 0; color:#64748b;">Autonomous Hospital Management System</p>
        </div>
        
        <p>Dear <strong>{patient_name}</strong>,</p>
        <p>Your triage request has been processed successfully. Below are your appointment and admission details:</p>
        
        <div style="margin: 16px 0;">
          <span class="badge badge-general">Ward: {ward}</span>
          <span class="badge badge-high">Priority: {priority}</span>
        </div>

        <div class="detail-row"><span class="label">Patient ID:</span><span class="value">{patient_id}</span></div>
        <div class="detail-row"><span class="label">Hospital:</span><span class="value">{hospital_name}</span></div>
        {f'<div class="detail-row"><span class="label">Address:</span><span class="value">{hospital_address}</span></div>' if hospital_address else ''}
        <div class="detail-row"><span class="label">Assigned Doctor:</span><span class="value">{doctor}</span></div>
        <div class="detail-row"><span class="label">Appointment Time:</span><span class="value">{next_slot}</span></div>
        <div class="detail-row"><span class="label">Token Number:</span><span class="value"><strong>{token_number}</strong></span></div>
        <div class="detail-row"><span class="label">Consultation Room:</span><span class="value">{consultation_room}</span></div>
        <div class="detail-row"><span class="label">Queue Position:</span><span class="value">#{queue_pos} (~{wait_min} mins wait)</span></div>

        <div class="guidance-box">
          <strong>📋 Patient Guidance:</strong><br/>
          {guidance}
        </div>

        <div class="footer">
          <p>This is an automated email from the Hospital Management Agentic System. Please do not reply directly to this email.</p>
        </div>
      </div>
    </body>
    </html>
    """

    text_content = f"""
    Hospital Triage Confirmation
    ---------------------------
    Dear {patient_name},

    Your triage request has been processed successfully.

    Patient ID: {patient_id}
    Hospital: {hospital_name}
    Ward: {ward} | Priority: {priority}
    Assigned Doctor: {doctor}
    Appointment Time: {next_slot}
    Token Number: {token_number}
    Consultation Room: {consultation_room}
    Queue Position: #{queue_pos} (Est. wait: {wait_min} mins)

    Guidance: {guidance}
    """

    # 1. Check EmailJS configuration
    emailjs_service_id = get_env("EMAILJS_SERVICE_ID")
    emailjs_template_id = get_env("EMAILJS_TEMPLATE_ID")
    emailjs_public_key = get_env("EMAILJS_PUBLIC_KEY")
    emailjs_private_key = get_env("EMAILJS_PRIVATE_KEY")

    if emailjs_service_id and emailjs_template_id and emailjs_public_key:
        try:
            import requests

            payload = {
                "service_id": emailjs_service_id,
                "template_id": emailjs_template_id,
                "user_id": emailjs_public_key,
                "template_params": {
                    "to_email": recipient,
                    "email": recipient,
                    "name": patient_name,
                    "patient_name": patient_name,
                    "patient_id": patient_id,
                    "title": f"Hospital Triage Confirmation ({token_number})",
                    "time": next_slot,
                    "hospital_name": hospital_name,
                    "hospital_address": hospital_address,
                    "doctor": doctor,
                    "assigned_doctor": doctor,
                    "ward": ward,
                    "priority": priority,
                    "token_number": token_number,
                    "consultation_room": consultation_room,
                    "queue_position": queue_pos,
                    "estimated_wait_minutes": wait_min,
                    "guidance": guidance,
                    "message": (
                        f"Patient ID: {patient_id}\n"
                        f"Hospital: {hospital_name}\n"
                        f"Address: {hospital_address}\n"
                        f"Ward: {ward} | Priority: {priority}\n"
                        f"Assigned Doctor: {doctor}\n"
                        f"Appointment Time: {next_slot}\n"
                        f"Token Number: {token_number}\n"
                        f"Consultation Room: {consultation_room}\n"
                        f"Queue Position: #{queue_pos} (Est. wait: {wait_min} mins)\n\n"
                        f"Patient Guidance: {guidance}"
                    )
                }
            }

            if emailjs_private_key:
                payload["accessToken"] = emailjs_private_key

            res = requests.post(
                "https://api.emailjs.com/api/v1.0/email/send",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if res.status_code == 200:
                print(f"[EMAIL] Live Email sent via EmailJS successfully to {recipient}")
                return True, f"Email sent via EmailJS to {recipient}"
            else:
                print(f"[EMAIL] EmailJS API error ({res.status_code}): {res.text}")
                return False, "Email notification unavailable (development mode)"
        except Exception as e:
            print(f"[EMAIL] Exception during EmailJS send to {recipient}: {str(e)}")
            return False, "Email notification unavailable (development mode)"

    # 2. Check SMTP credentials from environment
    smtp_server = get_env("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(get_env("SMTP_PORT", "587"))
    smtp_username = get_env("SMTP_USERNAME")
    smtp_password = get_env("SMTP_PASSWORD")
    sender_email = get_env("SENDER_EMAIL", smtp_username or "noreply@hospital-agent.ai")

    if smtp_username and smtp_password:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"Hospital Agent <{sender_email}>"
            msg["To"] = recipient

            msg.attach(MIMEText(text_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)

            print(f"[EMAIL] Live Email sent successfully to {recipient}")
            return True, f"Email sent successfully to {recipient}"
        except Exception as e:
            print(f"[EMAIL] Failed to send SMTP email to {recipient}: {str(e)}")
            return False, "Email notification unavailable (development mode)"
    else:
        # Simulation mode when no EmailJS or SMTP credentials configured
        print("\n" + "="*50)
        print(f"[EMAIL] [SIMULATION] To: {recipient}")
        print("Subject: " + subject.encode("ascii", "ignore").decode("ascii"))
        print(text_content.strip())
        print("="*50 + "\n")
        return False, "Email notification unavailable (development mode)"

