import frappe

@frappe.whitelist(allow_guest=True)
def create_issue_from_ticket(subject, description, raised_by, priority="Medium",
                              issue_type=None, customer=None, project=None):

    if frappe.db.exists("User", raised_by):
        frappe.set_user(raised_by)
    else:
        frappe.set_user("Guest")

    issue = frappe.get_doc({
        "doctype": "Issue",
        "subject": subject,
        "description": f"<b>Raised by:</b> {raised_by}<br><br>{description}",
        "raised_by": raised_by,
        "status": "Open",
        "priority": priority,
        "issue_type": issue_type,
        "customer": customer,
        "project": project,
    })
    issue.insert(ignore_permissions=True)
    frappe.db.commit()

    return issue.name