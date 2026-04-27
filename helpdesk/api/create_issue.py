import frappe
import requests

LIVE_SITE_URL = "https://erp.ethicalintelligent.com"   # 🔁 Replace with your live site URL
API_KEY = "1bb19f90d97e69c"                         # 🔁 From step 1
API_SECRET = "2b66f346c3b277d"                   # 🔁 From step 1

def create_issue_from_ticket(doc, method=None):
    # Prevent duplicate
    if getattr(doc, "issue", None):
        return

    headers = {
        "Authorization": f"token {API_KEY}:{API_SECRET}",
        "Content-Type": "application/json",
    }

    payload = {
        "doctype": "Issue",
        "subject": doc.subject,
        "description": doc.description or getattr(doc, "content", ""),
        "raised_by": doc.raised_by or getattr(doc, "email", None),
        "status": "Open",
        "priority": getattr(doc, "priority", "Medium"),
        "issue_type": getattr(doc, "ticket_type", None),
        "customer": getattr(doc, "customer", None),
        "project": getattr(doc, "project", None),
    }

    try:
        response = requests.post(
            f"{LIVE_SITE_URL}/api/resource/Issue",
            json=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        issue_name = response.json().get("data", {}).get("name")

        # Link back the issue name to the local ticket
        if issue_name and hasattr(doc, "issue"):
            doc.db_set("issue", issue_name)

        frappe.logger().info(f"Issue created on live site: {issue_name}")

    except requests.exceptions.HTTPError as e:
        frappe.log_error(
            title="Live Site Issue Creation Failed",
            message=f"HTTP Error: {e}\nResponse: {response.text}"
        )
    except requests.exceptions.RequestException as e:
        frappe.log_error(
            title="Live Site Issue Creation Failed",
            message=f"Connection Error: {str(e)}"
        )