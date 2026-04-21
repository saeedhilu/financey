from rest_framework import serializers
from .models import Transaction, EMIPlan

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('user',)

class EMIPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = EMIPlan
        fields = '__all__'
        read_only_fields = ('user',)
