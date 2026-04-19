from rest_framework import serializers
from .models import SavingsGoal

class SavingsGoalSerializer(serializers.ModelSerializer):
    current_amount = serializers.ReadOnlyField()

    class Meta:
        model = SavingsGoal
        fields = '__all__'
        read_only_fields = ('user',)
