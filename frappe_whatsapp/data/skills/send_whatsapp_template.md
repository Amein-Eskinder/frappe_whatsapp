# How to Use send_whatsapp_template

## When to use this tool
Use `send_whatsapp_template` to send an **approved WhatsApp message template**. This is
the **only** way to **start** a conversation that is outside WhatsApp's 24-hour customer
service window (business-initiated messaging). For replies/conversation **within** 24h,
prefer `send_whatsapp_message` (plain text).

## Workflow (do this in order)
1. **Find the template.** List the `WhatsApp Templates` DocType (e.g. with `list_documents`)
   to get the exact template **name** and see its body — count the variables (`{{1}}`,
   `{{2}}`, ...).
2. **Send** with `body_parameters` filling those variables **in order**.

The sending account resolves **automatically from the logged-in user** — do not pass
`whatsapp_account` unless the user names one.

## Parameters
| Name | Type | Required | Description |
|---|---|---|---|
| `to` | string | yes | Recipient phone in international format, e.g. `+15551234567`. |
| `template` | string | yes | Name of the approved `WhatsApp Templates` record. |
| `body_parameters` | array[string] | no | Values for the body variables `{{1}}`, `{{2}}`, ... **in order**. Omit if the template has no variables. |
| `whatsapp_account` | string | no | Override the sending account. Omit to use the logged-in user's account. |

## Examples

### Template with two variables ({{1}} name, {{2}} order id)
```json
{"to": "+15551234567", "template": "order_confirmation", "body_parameters": ["Sara", "ORD-1042"]}
```

### Template with no variables
```json
{"to": "+15551234567", "template": "store_hours"}
```
Expected response on success:
```json
{"success": true, "status": "Success", "message_id": "wamid....", "template": "order_confirmation"}
```

## Common pitfalls
- **Template must be approved** by Meta and exist as a `WhatsApp Templates` record. If you
  get "WhatsApp Template '...' not found", list `WhatsApp Templates` for valid names.
- **`body_parameters` order and count must match** the template's `{{n}}` variables exactly.
  Too few/many or wrong order produces a malformed or rejected message.
- **Don't use this for replies within 24h** — plain `send_whatsapp_message` is cheaper and
  has no template approval requirement.

## Related tools
- `send_whatsapp_message` — for free-form replies inside the 24-hour window.
- `list_documents` on `WhatsApp Templates` — to discover template names and their variables.
