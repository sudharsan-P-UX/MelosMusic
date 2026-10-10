import re

with open('website/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix FeeReceipt query
text = text.replace("'fee_payment__student_fee__student__first_name'", "'student__first_name'")
text = text.replace("'payment_date'", "'receipt_date'")

with open('website/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
