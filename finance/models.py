from django.db import models
from users.models import User
from academics.models import Course, Batch

class FeeType(models.Model):
    fee_type_id = models.AutoField(primary_key=True, db_column='FeeTypeId')
    fee_type_name = models.CharField(max_length=100, db_column='FeeTypeName')
    description = models.CharField(max_length=500, null=True, blank=True, db_column='Description')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    class Meta: db_table = 'FeeType'

class CourseFee(models.Model):
    course_fee_id = models.AutoField(primary_key=True, db_column='CourseFeeId')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='CourseId')
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE, db_column='FeeTypeId')
    amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='Amount')
    effective_from = models.DateField(null=True, blank=True, db_column='EffectiveFrom')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')
    class Meta: db_table = 'CourseFee'

class StudentFee(models.Model):
    student_fee_id = models.AutoField(primary_key=True, db_column='StudentFeeId')
    student = models.ForeignKey(User, on_delete=models.CASCADE, db_column='StudentId')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, db_column='CourseId')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, db_column='BatchId')
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalAmount')
    discount_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0, db_column='DiscountAmount')
    final_amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='FinalAmount')
    due_date = models.DateField(null=True, blank=True, db_column='DueDate')
    status = models.SmallIntegerField(db_column='Status') # 1=Pending, 2=Partial, 3=Paid, 4=Cancelled
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')
    class Meta: db_table = 'StudentFee'

class StudentFeeInstallment(models.Model):
    installment_id = models.AutoField(primary_key=True, db_column='InstallmentId')
    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE, db_column='StudentFeeId')
    installment_no = models.IntegerField(db_column='InstallmentNo')
    due_date = models.DateField(db_column='DueDate')
    amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='Amount')
    paid_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0, db_column='PaidAmount')
    status = models.SmallIntegerField(db_column='Status')
    remarks = models.CharField(max_length=500, null=True, blank=True, db_column='Remarks')
    class Meta: db_table = 'StudentFeeInstallment'

class FeePayment(models.Model):
    fee_payment_id = models.AutoField(primary_key=True, db_column='FeePaymentId')
    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE, db_column='StudentFeeId')
    receipt_no = models.CharField(max_length=50, null=True, blank=True, db_column='ReceiptNo')
    payment_date = models.DateTimeField(auto_now_add=True, db_column='PaymentDate')
    paid_amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='PaidAmount')
    payment_mode = models.SmallIntegerField(db_column='PaymentMode') # 1=Cash, 2=UPI, 3=CC, 4=DC, 5=NetBanking
    transaction_no = models.CharField(max_length=200, null=True, blank=True, db_column='TransactionNo')
    remarks = models.CharField(max_length=500, null=True, blank=True, db_column='Remarks')
    created_date = models.DateTimeField(auto_now_add=True, db_column='CreatedDate')
    created_by = models.IntegerField(null=True, blank=True, db_column='CreatedBy')
    class Meta: db_table = 'FeePayment'

class FeeReceipt(models.Model):
    receipt_id = models.AutoField(primary_key=True, db_column='ReceiptId')
    receipt_no = models.CharField(max_length=50, db_column='ReceiptNo')
    student = models.ForeignKey(User, on_delete=models.CASCADE, db_column='StudentId')
    fee_payment = models.ForeignKey(FeePayment, on_delete=models.CASCADE, db_column='FeePaymentId')
    receipt_date = models.DateTimeField(auto_now_add=True, db_column='ReceiptDate')
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='TotalAmount')
    generated_by = models.IntegerField(null=True, blank=True, db_column='GeneratedBy')
    class Meta: db_table = 'FeeReceipt'

class DiscountMaster(models.Model):
    discount_id = models.AutoField(primary_key=True, db_column='DiscountId')
    discount_name = models.CharField(max_length=200, db_column='DiscountName')
    discount_type = models.SmallIntegerField(db_column='DiscountType') # 1=Percentage, 2=Fixed
    discount_value = models.DecimalField(max_digits=18, decimal_places=2, db_column='DiscountValue')
    is_active = models.BooleanField(default=True, db_column='IsActive')
    class Meta: db_table = 'DiscountMaster'

class FeeRefund(models.Model):
    refund_id = models.AutoField(primary_key=True, db_column='RefundId')
    student = models.ForeignKey(User, on_delete=models.CASCADE, db_column='StudentId')
    receipt = models.ForeignKey(FeeReceipt, on_delete=models.CASCADE, db_column='ReceiptId')
    refund_amount = models.DecimalField(max_digits=18, decimal_places=2, db_column='RefundAmount')
    refund_date = models.DateTimeField(auto_now_add=True, db_column='RefundDate')
    reason = models.CharField(max_length=500, null=True, blank=True, db_column='Reason')
    approved_by = models.IntegerField(null=True, blank=True, db_column='ApprovedBy')
    class Meta: db_table = 'FeeRefund'
