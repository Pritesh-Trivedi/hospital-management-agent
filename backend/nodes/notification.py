from utils.notification_utils import create_notification, send_email_notification

def notification_node(state):

    notification = create_notification(state)

    state["notification_id"] = notification

    print("Notification Created:", notification)

    state["steps"].append(
        f"Notification: alert created, notification ID {notification}"
    )

    if state.get("email"):
        email_success, email_msg = send_email_notification(state)
        state["email_sent"] = email_success
        state["email_status"] = email_msg
        state["steps"].append(f"Notification: {email_msg}")
    else:
        state["email_sent"] = False
        state["email_status"] = "No email provided"

    return state