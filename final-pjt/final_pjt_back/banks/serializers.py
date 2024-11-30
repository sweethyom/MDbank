from .models import BankAccount, Favorites, Bank
from rest_framework import serializers

class BankAccountSerializers(serializers.ModelSerializer):
    class Meta:
        model=BankAccount
        fields='__all__'


class FavoritesSerializers(serializers.ModelSerializer):
    bank_name = serializers.SerializerMethodField()
    class Meta:
        model=Favorites
        fields='__all__'
        read_only_fields = ('member_pk',)

    def get_bank_name(self, obj):
        return obj.bank.name
    
class BankSerializers(serializers.ModelSerializer):
    class Meta:
        model=Bank
        fields='__all__'
