import frappe
from frappe import _


def assign_ticket_to_agent(ticket_id, agent_id=None):
    if not ticket_id:
        return

    ticket_doc = frappe.get_doc("HD Ticket", ticket_id)

    if not agent_id:
        # assign to self
        agent_id = frappe.session.user

    if not frappe.db.exists("HD Agent", agent_id):
        frappe.throw(_("Tickets can only be assigned to agents"))

    ticket_doc.assign_agent(agent_id)
    return ticket_doc

@frappe.whitelist()
def get_user_projects():
    user = frappe.session.user
    projects = frappe.db.sql("""
        SELECT DISTINCT p.name
        FROM `tabProject` p
        INNER JOIN `tabProject User` pu ON pu.parent = p.name
        WHERE pu.user = %s
        AND p.status != 'Cancelled'
    """, user, as_dict=True)
    
    return [{"value": p.name, "label": p.name} for p in projects]