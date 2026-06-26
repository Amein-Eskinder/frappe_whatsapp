"""
Send WhatsApp Template — Frappe Assistant Core tool for frappe_whatsapp.

Sends an APPROVED WhatsApp message template. Required to start a conversation
outside the 24-hour service window (Meta rejects free-form text there). The
sending account is resolved from the logged-in user's WhatsApp Account.
"""

import json
from typing import Any, Dict

import frappe
from frappe import _

from frappe_assistant_core.core.base_tool import BaseTool


class SendWhatsAppTemplate(BaseTool):
    """Send an approved WhatsApp template message."""

    def __init__(self):
        super().__init__()
        self.name = "send_whatsapp_template"
        self.description = (
            "Send an APPROVED WhatsApp template message to a phone number. Use this to "
            "START a new conversation (business-initiated, outside the 24-hour service "
            "window) — free-form text is rejected by Meta in that case; use "
            "send_whatsapp_message only for replies within 24h. First read the "
            "'WhatsApp Templates' doctype to get the exact template name and how many "
            "body variables it expects, then pass body_parameters in order. The sending "
            "account is chosen automatically from the logged-in user's WhatsApp Account."
        )
        self.category = "WhatsApp"
        self.source_app = "frappe_whatsapp"
        self.requires_permission = "WhatsApp Message"
        self.inputSchema = {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Recipient phone number in international format, e.g. +15551234567",
                },
                "template": {
                    "type": "string",
                    "description": "Name of the WhatsApp Templates record to send (must be approved).",
                },
                "body_parameters": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Values for the template body variables {{1}}, {{2}}, ... in order. "
                        "Omit if the template has no variables."
                    ),
                },
                "whatsapp_account": {
                    "type": "string",
                    "description": "Optional. WhatsApp Account to send from. Omit to use the logged-in user's account.",
                },
            },
            "required": ["to", "template"],
        }

    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        to = (arguments.get("to") or "").strip()
        template = arguments.get("template")
        body_parameters = arguments.get("body_parameters") or []
        account = arguments.get("whatsapp_account") or None

        if not to or not template:
            return {"success": False, "error": _("Both 'to' and 'template' are required.")}

        if not frappe.db.exists("WhatsApp Templates", template):
            return {
                "success": False,
                "error": _("WhatsApp Template '{0}' not found.").format(template),
                "hint": "List the 'WhatsApp Templates' doctype to see valid template names.",
            }

        try:
            data = {
                "doctype": "WhatsApp Message",
                "type": "Outgoing",
                "message_type": "Template",
                "content_type": "text",
                "to": to,
                "template": template,
                # None -> resolved from the logged-in user's WhatsApp Account
                "whatsapp_account": account,
            }
            if body_parameters:
                # frappe_whatsapp reads body_param as a JSON object and sends its values in order
                data["body_param"] = json.dumps(
                    {str(i + 1): v for i, v in enumerate(body_parameters)}
                )
            doc = frappe.get_doc(data)
            doc.insert()  # before_insert dispatches the template to Meta
            return {
                "success": True,
                "name": doc.name,
                "status": doc.status,
                "message_id": doc.message_id,
                "whatsapp_account": doc.whatsapp_account,
                "template": template,
            }
        except Exception as e:
            frappe.log_error(
                title=_("Send WhatsApp Template Error"),
                message=f"to={to} template={template}\n\n{frappe.get_traceback()}",
            )
            return {"success": False, "error": str(e)}


__all__ = ["SendWhatsAppTemplate"]
