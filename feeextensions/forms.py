from django import forms
from .models import FeeExtensions
from students.models import StudentAccount


class FeeExtensionForm(forms.ModelForm):
    outstanding_balance = forms.DecimalField(
        widget=forms.NumberInput(attrs={'readonly': 'readonly'}),
        required=False
    )

    class Meta:
        model = FeeExtensions
        fields = ['start_date', 'end_date', 'frequency', 'outstanding_balance']

    def __init__(self, *args, **kwargs):
        # Assuming instance is passed to the form
        student_account = kwargs.pop('student_account', None)
        super(FeeExtensionForm, self).__init__(*args, **kwargs)

        if student_account:
            self.fields['outstanding_balance'].initial = student_account.balance

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        frequency = cleaned_data.get('frequency')

        if end_date and end_date <= start_date:
            raise forms.ValidationError("End date must be after start date")

        outstanding_balance = cleaned_data.get('outstanding_balance', 0)

        num_installments = 0
        if frequency == 'weekly':
            num_installments = (end_date - start_date).days // 7
        elif frequency == 'bi_weekly':
            num_installments = (end_date - start_date).days // 14
        elif frequency == 'monthly':
            num_installments = (end_date - start_date).days // 30

        if num_installments > 0:
            installment_amount = outstanding_balance / num_installments
        else:
            installment_amount = 0

        # Optionally, you can set installment_amount in cleaned_data if needed
        self.cleaned_data['amount'] = installment_amount
        return self.cleaned_data
