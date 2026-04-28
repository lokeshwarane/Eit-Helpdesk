import frappe
import requests

LIVE_SITE_URL = "https://erp.ethicalintelligent.com"

def recieve_helpdesk_ticket(doc, method=None):
    if getattr(doc, "issue", None):
        return

    raiser = doc.raised_by or getattr(doc, "email", None)

    payload = {
        "subject": doc.subject,
        "description": doc.description or getattr(doc, "content", ""),
        "raised_by": raiser,
        "priority": getattr(doc, "priority", "Medium"),
        "issue_type": getattr(doc, "ticket_type", None),
        "customer": getattr(doc, "customer", None),
        "project": getattr(doc, "project", None),
    }

    try:
        response = requests.post(
            f"{LIVE_SITE_URL}/api/method/helpdesk.api.create_issue.create_issue_from_ticket",
            json=payload,
            # 👆 No Authorization header at all
            timeout=10
        )
        response.raise_for_status()

        issue_name = response.json().get("message")

        if issue_name and hasattr(doc, "issue"):
            doc.db_set("issue", issue_name)

    except requests.exceptions.HTTPError as e:
        frappe.log_error("Live Site Issue Creation Failed", f"HTTP Error: {e}\nResponse: {response.text}")
    except requests.exceptions.RequestException as e:
        frappe.log_error("Live Site Issue Creation Failed", f"Connection Error: {str(e)}")