from rest_framework import serializers
from walletapp.models import *
from datetime import date, datetime

class InitSerializer(serializers.Serializer):   
    username = serializers.CharField()
    password = serializers.CharField()
    fullname = serializers.CharField()

class WalletResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    owned_by = serializers.CharField(source='account_id')    
    status = serializers.SerializerMethodField()
    enabled_at = serializers.SerializerMethodField()

    def get_status(self, instance):
        if instance.status:
            return 'enabled'
        else:
            return 'disabled'
    
    def get_enabled_at(self, instance):
        now = datetime.now()
        return str(now)

    class Meta:
        model = Wallet
        fields = ('id', 'owned_by', 'status', 'enabled_at', 'balance')


# class WalletDepositSerializer(serializers.ModelSerializer):
    # id = serializers.CharField()
    # deposited_by = serializers.CharField(source='account_id')
    # deposited_at = serializers.SerializerMethodField()
    # amount = serializers.SerializerMethodField()
#    
    # def get_deposited_at(self, instance):
        # now = datetime.now()
        # return str(now)
    # 
    # def get_amount(self, instance):
        # last_trx = Transcation.objects.filter(transaction_by=instance.account).last()
        # return str(last_trx.amount)
    # 
    # def to_representation(self, instance):
        # data = super(WalletDepositSerializer, self).to_representation(instance)
        # data['status'] = 'success'
        # return data
# 
    # class Meta:
        # model = Wallet
        # fields = ('id', 'deposited_by', 'deposited_at', 'amount')


# class WalletWithdrawSerializer(serializers.ModelSerializer):
#     id = serializers.CharField()
#     withdrawn_by = serializers.CharField(source='account_id')
#     withdrawn_at = serializers.SerializerMethodField()
#     amount = serializers.SerializerMethodField()
   
#     def get_withdrawn_at(self, instance):
#         now = datetime.now()
#         return str(now)
    
#     def get_amount(self, instance):
#         last_trx = Transcation.objects.filter(transaction_by=instance.account).last()
#         return str(last_trx.amount)
    
#     def to_representation(self, instance):
#         data = super(WalletWithdrawSerializer, self).to_representation(instance)
#         data['status'] = 'success'
#         return data

#     class Meta:
#         model = Wallet
#         fields = ('id', 'withdrawn_by', 'withdrawn_at', 'amount')


class WalletDisableSerializer(serializers.ModelSerializer):
    id= serializers.CharField()
    owned_by = serializers.CharField(source='account_id')    
    status = serializers.SerializerMethodField()
    disabled_at = serializers.SerializerMethodField()

    def get_status(self, instance):
        if instance.status:
            return 'enabled'
        else:
            return 'disabled'
        
    def get_disabled_at(self, instance):
        now = datetime.now()
        return str(now)

    class Meta:
        model = Wallet
        fields = ('id', 'owned_by', 'status', 'disabled_at', 'balance')


class WalletTransactionSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    transaction_by = serializers.CharField(source='account_id')
    transaction_at = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
   
    def get_transaction_at(self, instance):
        now = datetime.now()
        return str(now)
    
    def get_amount(self, instance):
        last_trx = Transcation.objects.filter(transaction_by=instance.account).last()
        return str(last_trx.amount)
    
    def to_representation(self, instance):
        data = super(WalletTransactionSerializer, self).to_representation(instance)
        data['status'] = 'success'
        if self.context['trx_type'] == 'deposit':
            data['deposited_by'] = data['transaction_by']
            data['deposited_at'] = data['transaction_at']
        elif self.context['trx_type'] == 'withdraw':
            data['withdrawn_by'] = data['transaction_by']
            data['withdrawn_at'] = data['transaction_at']
        data.pop('transaction_by')
        data.pop('transaction_at')
        return data

    class Meta:
        model = Wallet
        fields = ('id', 'transaction_by', 'transaction_at', 'amount')