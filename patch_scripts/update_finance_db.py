with open('finance/models.py', 'r') as f:
    content = f.read()

new_finance = '''
class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid'), ('Partial', 'Partial')])
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'invoices'

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='transactions')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('UPI', 'UPI'), ('Card', 'Card')])
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transactions'
'''
if 'Invoice' not in content:
    content += '\n' + new_finance

with open('finance/models.py', 'w') as f:
    f.write(content)
