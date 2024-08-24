from rest_framework import serializers
from .models import FeeExtensions

class FeeExtensionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeExtensions
        fields = ['id', 'student', 'student_account', 'feecategory', 'dueDate', 'school_code', 'start_date', 'end_date', 'frequency', 'amount', 'last_reminder_sent', 'reminder_frequency', 'method_of_payment', 'status']
        read_only_fields = ['amount']  # Make the amount field read-only since it is computed automatically

    def create(self, validated_data):
        fee_extension = FeeExtensions.objects.create(**validated_data)
        fee_extension.compute_amount()  # Compute the amount
        fee_extension.save()
        return fee_extension

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.compute_amount()  # Recompute the amount on update
        instance.save()
        return instance
