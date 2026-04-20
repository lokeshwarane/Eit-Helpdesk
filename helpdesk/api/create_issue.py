import frappe

def create_issue_from_ticket(doc, method=None):
    # Prevent duplicate
    if getattr(doc, "issue", None):
        return

    issue = frappe.get_doc({
        "doctype": "Issue",
        "subject": doc.subject,
        "description": doc.description or getattr(doc, "content", ""),
        "raised_by": doc.raised_by or getattr(doc, "email", None),
        "status": "Open",
        "priority": getattr(doc, "priority", "Medium"),

        # 🔥 NEW MAPPINGS
        "issue_type": getattr(doc, "ticket_type", None),
        "customer": getattr(doc, "customer", None),
        "project": getattr(doc, "project", None),
    })

    issue.insert(ignore_permissions=True)

    # Link back
    if hasattr(doc, "issue"):
        doc.db_set("issue", issue.name)
        
