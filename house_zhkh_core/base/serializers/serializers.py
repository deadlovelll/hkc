from rest_framework import serializers

from house_zhkh_core.base.models.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'