from rest_framework import serializers
from enrollment.models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enrollment
        fields="__all__"

    def validate_months(self,value):
        if value<=0:
            raise serializers.ValidationError("Duration must be a +ve value.")
        return value

    def validate_fee(self,value):
        if value<=0:
            raise serializers.ValidationError("Fee cannot be negative.")
        return value