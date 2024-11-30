from .models import Product, Option, ExchangeRate, Asset_type
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):       # 예적금 데이터 받는 용
    class Meta:
        model = Product
        fields = '__all__'          

class OptionSerializer(serializers.ModelSerializer):        # 예적금 옵션 데이터 받는 용
    class Meta:
        model = Option
        fields = '__all__'
        read_only_fields=('product',)

class RateComparisonSerializer(serializers.ModelSerializer):
    class OptionRateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Option
            fields = ('intr_rate2',)  # 최고금리용
    
    class PeriodSerializer(serializers.ModelSerializer):
        class Meta:
            model = Option
            fields = ('save_trm',)  # 기간용
    
    rates = serializers.SerializerMethodField()
    period = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_rates(self, obj):
        # 최고금리 옵션
        highest_rate_option = obj.rates.order_by('-intr_rate2').first()
        if highest_rate_option:
            return self.OptionRateSerializer(highest_rate_option).data
        return None

    def get_period(self, obj):
        # 최고금리 옵션의 기간
        highest_rate_option = obj.rates.order_by('-intr_rate2').first()
        if highest_rate_option:
            return self.PeriodSerializer(highest_rate_option).data
        return None

class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = '__all__'

class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset_type
        fields = '__all__'  
