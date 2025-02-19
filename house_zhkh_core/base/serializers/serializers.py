from rest_framework import serializers
from house_zhkh.base.models.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'