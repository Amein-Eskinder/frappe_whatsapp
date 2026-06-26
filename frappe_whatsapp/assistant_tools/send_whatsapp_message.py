"""
Send WhatsApp Message — Frappe Assistant Core tool for frappe_whatsapp.

Gives the AI a purpose-built tool to send a WhatsApp text message instead of
operating on the raw "WhatsApp Message" doctype via the generic create_document
tool. The sending account is resolved automatically from the logged-in user's
WhatsApp Account (see WhatsAppMessage.set_whatsapp_account).
"""

import frappe
from frappe import _
from typing import Any, Dict

from frappe_assistant_core.core.base_tool import BaseTool


class SendWhatsAppMessage(BaseTool):
    """Send a WhatsApp text message from the logged-in user's WhatsApp Account."""

    def __init__(self):
        super().__init__()
        self.name = "send_whatsapp_message"
        self.description = (
            "Send a free-form WhatsApp TEXT message to a phone number (use this for "
            "replies and conversations within the 24-hour service window). To start a "
            "new conversation outside that window, use send_whatsapp_template instead. "
            "The sending account is chosen automatically from the logged-in user's "
            "WhatsApp Account — do NOT ask for or pass an account unless the user "
            "explicitly names one. Provide the recipient number in international format "
            "(e.g. +15551234567) and the message text. Pass reply_to to reply to a "
            "specific message. Returns the WhatsApp message id on success."
        )
        self.category = "WhatsApp"
        self.source_app = "frappe_whatsapp"
        # Gate: caller must have access to WhatsApp Message
        self.requires_permission = "WhatsApp Message"
        self.inputSchema = {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Recipient phone number in international format, e.g. +15551234567",
                },
                "message": {
                    "type": "string",
                    "description": "The text message to send",
                },
                "reply_to": {
                    "type": "string",
                    "description": (
                        "Optional. The WhatsApp message id (wamid...) of a previous/incoming "
                        "message to reply to. When set, this is sent as a threaded reply."
                    ),
                },
                "whatsapp_account": {
                    "type": "string",
                    "description": (
                        "Optional. WhatsApp Account name to send from. Omit to use the "
                        "logged-in user's account."
                    ),
                },
            },
            "required": ["to", "message"],
        }

    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        to = (arguments.get("to") or "").strip()
        message = arguments.get("message")
        account = arguments.get("whatsapp_account") or None
        reply_to = arguments.get("reply_to") or None

        if not to or not message:
            return {"success": False, "error": _("Both 'to' and 'message' are required.")}

        try:
            data = {
                "doctype": "WhatsApp Message",
                "type": "Outgoing",
                "message_type": "Manual",
                "content_type": "text",
                "to": to,
                "message": message,
                # None -> resolved from the logged-in user's WhatsApp Account
                "whatsapp_account": account,
            }
            if reply_to:
                data["is_reply"] = 1
                data["reply_to_message_id"] = reply_to
            doc = frappe.get_doc(data)
            doc.insert()  # respects the caller's permissions
            return {
                "success": True,
                "name": doc.name,
                "status": doc.status,
                "message_id": doc.message_id,
                "whatsapp_account": doc.whatsapp_account,
            }
        except Exception as e:
            # Standing rule: log every error to the Frappe Error Log with traceback.
            frappe.log_error(
                title=_("Send WhatsApp Message Error"),
                message=f"to={to} account={account}\n\n{frappe.get_traceback()}",
            )
            return {"success": False, "error": str(e)}


__all__ = ["SendWhatsAppMessage"]
