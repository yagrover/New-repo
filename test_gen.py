from genai_utils import generate_dispute_reply

invoice_text = "This invoice was disputed due to incorrect tax rates and a missing PO reference."

response = generate_dispute_reply(invoice_text)

print("\n🧠 Draft Email from Claude:\n")
print(response)
