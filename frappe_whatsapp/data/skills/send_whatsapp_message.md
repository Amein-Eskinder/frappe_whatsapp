# How to Use send_whatsapp_message

## When to use this tool
Use `send_whatsapp_message` to send a **free-form WhatsApp text message** — a reply
or an ongoing conversation **within WhatsApp's 24-hour customer service window** (i.e.
the contact has messaged the business in the last 24 hours). To **start** a new
conversation outside that window, free-form text is rejected by Meta — use
`send_whatsapp_template` instead.

## Account selection (important)
The sending WhatsApp Account is resolved **automatically from the logged-in user's**
mapped WhatsApp Account. **Do not ask the user which account to send from, and do not
pass `whatsapp_account`,** unless the user explicitly names a specific account. If the
logged-in user has no mapped account and no default exists, the call fails with
"Please set a default outgoing WhatsApp Account" — tell the user to map their User to a
WhatsApp Account (field `user` on WhatsApp Account).

## Parameters
| Name | Type | Required | Description |
|---|---|---|---|
| `to` | string | yes | Recipient phone in **international format**, e.g. `+15551234567`. |
| `message` | string | yes | The text body to send. |
| `reply_to` | string | no | The WhatsApp message id (`wamid...`) of a prior/incoming message to reply to. Sends as a threaded reply. |
| `whatsapp_account` | string | no | Override the sending account. Omit to use the logged-in user's account. |

## Examples

### Plain message
```json
{"to": "+15551234567", "message": "Thanks for your order — it ships today."}
```

### Reply to an incoming message
```json
{"to": "+15551234567", "message": "Yes, that size is in stock.", "reply_to": "wamid.HBgM..."}
```
Expected response on success:
```json
{"success": true, "status": "Success", "message_id": "wamid....", "whatsapp_account": "Farhia Mohammed"}
```

## Common pitfalls
- **24-hour window:** free-form text only works if the contact messaged within 24h. Outside it, Meta rejects the send — switch to `send_whatsapp_template`.
- **Phone format:** always international (`+<country><number>`). No spaces or local-only numbers.
- **Don't pass `whatsapp_account`** — it resolves from the logged-in user. Passing the wrong one sends from another person's number.
- **`reply_to` is a `wamid`**, not a document name — get it from a previous message's `message_id`.

## Related tools
- `send_whatsapp_template` — to **start** a conversation (outside 24h) with an approved template.
- `get_document` / `list_documents` on `WhatsApp Message` — to read conversation history.
