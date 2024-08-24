from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from .models import FeeExtensions, StudentAccount
from students.models import Students
from studentsparents.models import StudentsParents
from .forms import FeeExtensionForm
from .serializers import FeeExtensionsSerializer
from rest_framework.response import Response


@login_required
def create_fee_extension(request, student_id):
    student = get_object_or_404(Students, pk=student_id)
    student_account = get_object_or_404(StudentAccount, student=student)
    parent = get_object_or_404(StudentsParents, studentID=student).parentID
    outstanding_balance = student_account.balance

    if request.method == 'POST':
        form = FeeExtensionForm(request.POST)
        if form.is_valid():
            fee_extension = form.save(commit=False)
            fee_extension.student = student
            fee_extension.student_account = student_account
            fee_extension.save()

            # Send notification to admin
            send_mail(
                'New Fee Extension Request',
                f'A new fee extension request has been created for {student.firstName} {student.lastName}.',
                'from@example.com',
                ['admin@example.com'],
            )

            # Send notification to parent
            send_mail(
                'Fee Extension Request Created',
                f'Your fee extension request for {student.firstName} {student.lastName} has been created and is pending approval.',
                'from@example.com',
                [parent.email],
            )

            messages.success(request, 'Fee extension request created successfully.')
            return redirect('fee_extension_method', fee_extension.id)
    else:
        form = FeeExtensionForm(initial={'outstanding_balance': outstanding_balance})

    return render(request, 'feeextensions/create_fee_extension.html', {'form': form, 'student': student})


@login_required
def fee_extension_method(request, fee_extension_id):
    fee_extension = get_object_or_404(FeeExtensions, pk=fee_extension_id)

    if request.method == 'POST':
        method_of_payment = request.POST.get('method_of_payment')
        fee_extension.method_of_payment = method_of_payment
        fee_extension.save()

        # Send notification to admin
        send_mail(
            'Fee Extension Payment Method Set',
            f'The payment method for fee extension request {fee_extension.id} has been set to {method_of_payment}.',
            'from@example.com',
            ['admin@example.com'],
        )

        # Send notification to parent
        parent = get_object_or_404(StudentsParents, studentID=fee_extension.student).parentID
        send_mail(
            'Payment Method Set for Fee Extension',
            f'The payment method for your fee extension request for {fee_extension.student.firstName} {fee_extension.student.lastName} has been set to {method_of_payment}.',
            'from@example.com',
            [parent.email],
        )

        messages.success(request, 'Payment method set successfully.')
        return redirect('fee_extension_details', fee_extension.id)

    return render(request, 'feeextensions/fee_extension_method.html', {'fee_extension': fee_extension})


class FeeExtensionsView(viewsets.ModelViewSet):
    queryset = FeeExtensions.objects.all()
    serializer_class = FeeExtensionsSerializer

    def create(self, request, *args, **kwargs):
        student = get_object_or_404(Students, id=request.data.get('student'))
        student_account = get_object_or_404(StudentAccount, student=student)

        # Check if the account has an outstanding balance
        if student_account.balance <= 0:
            return Response({"error": "No outstanding balance to create a fee extension."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.data['student_account'] = student_account.id

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            fee_extension = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            fee_extension = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
