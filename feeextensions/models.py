from django.db import models
from feecategories.models import FeeCategories
from schools.models import Schools
from students.models import Students, StudentAccount
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta


class FeeExtensions(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    student_account = models.OneToOneField(StudentAccount, on_delete=models.CASCADE)
    feecategory = models.ForeignKey(FeeCategories, on_delete=models.CASCADE)
    dueDate = models.DateField(null=True)
    school_code = models.ForeignKey(Schools, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    frequency_choices = [
        ('weekly', 'Weekly'),
        ('bi_weekly', 'Bi-Weekly'),
        ('monthly', 'Monthly'),
    ]
    frequency = models.CharField(max_length=20, choices=frequency_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_reminder_sent = models.DateField(null=True, blank=True)
    reminder_frequency = models.IntegerField(default=3)  # Number of days between reminders
    method_of_payment = models.CharField(max_length=20, choices=[
        ('mobile_money', 'Mobile Money'),
        ('equity_account', 'Equity Account'),
        ('stripe_card', 'Stripe Card'),
    ], null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('lapsed', 'Lapsed'),
    ], default='pending')

    def __str__(self):
        return f"FeeExtension ID: {self.id}, Student: {self.student}, Fee Category: {self.feecategory}"

    class Meta:
        db_table = 'fee_extensions'

    def compute_amount(self):
        # Calculate the duration in days
        duration = (self.end_date - self.start_date).days

        # Determine the number of payments based on frequency
        if self.frequency == 'weekly':
            num_payments = duration // 7
        elif self.frequency == 'bi_weekly':
            num_payments = duration // 14
        elif self.frequency == 'monthly':
            num_payments = duration // 30
        else:
            num_payments = 1  # Default to a single payment if no valid frequency is provided

        # Ensure there's at least one payment
        num_payments = max(num_payments, 1)

        # Compute the amount per payment based on the outstanding balance
        self.amount = self.student_account.balance / num_payments

    def save(self, *args, **kwargs):
        self.compute_amount()  # Compute the amount before saving
        super().save(*args, **kwargs)


class PaymentPlan(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    frequency = models.CharField(max_length=20)  # daily, weekly, bi_weekly, monthly

    def __str__(self):
        return f"Payment Plan for {self.student} - {self.total_amount}"


class PaymentInstallment(models.Model):
    payment_plan = models.ForeignKey(PaymentPlan, related_name='installments', on_delete=models.CASCADE)
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Installment for {self.payment_plan} - {self.amount} due on {self.due_date}"


@receiver(post_save, sender=PaymentInstallment)
def update_student_balance(sender, instance, **kwargs):
    student_account = instance.payment_plan.student.studentaccount
    if instance.is_paid:
        student_account.credit += instance.amount
    else:
        student_account.debit += instance.amount
    student_account.save()
