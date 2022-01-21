from django.contrib.auth.models import User
from django.core.exceptions import TooManyFieldsSent
from walletapp.serializers import *
from walletapp.models import *
from walletapp import views
from rest_framework.authtoken.models import Token
from django.db import transaction

def build_response(status, data):
    response = {
        'status': status,
        'data': data}
    return response

def initialise_wallet(data):
    try:
        username = data.get('username')
        password = data.get('password')
        fullname = data.get('fullname')
        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password)
            token, created = Token.objects.get_or_create(user=user)
            account = Account.objects.create(full_name=fullname, user=user)
            Wallet.objects.create(account=account, balance=0)
        return_data = {"token": token.key}
        response = build_response(status='success', data=return_data)
        return response
    except Exception as exc:
        return_data = {
            "error": str(exc)
            }
        response = build_response(status='failure', data=return_data)
        return response


def view_wallet(user, only_view=False):
    try:
        wallet = user.account.wallet
        status = 'success'
        if only_view and wallet.status:
            wallet_serializer = WalletResponseSerializer(wallet)
            return_data = {
                "wallet": wallet_serializer.data
            }
        elif not wallet.status and not only_view:
            wallet.status = True
            wallet.save()
            wallet_serializer = WalletResponseSerializer(wallet)
            return_data = {
                "wallet": wallet_serializer.data
            }
        elif wallet.status:
            return_data = {
                "error": "Already the wallet is enabled"
            }
            status = 'failure'
        else:
            return_data = {
                "error": "Wallet is not enabled, please enable the wallet 1st to proceed further"
            }
            status = 'failure'

        response = build_response(status, return_data)
        return response
    except Exception as exc:
        return_data = {
                "error": str(exc)
            }
        response = build_response('failure', return_data)
        return response


def transcation_wallet(user,amount,transaction_type):
    try:
        wallet = user.account.wallet
        if wallet.status:
            with transaction.atomic():
                serializer_class = WalletTransactionSerializer
                if transaction_type == 'deposit':
                    wallet.balance = wallet.balance + int(amount)
                else:
                    wallet.balance = wallet.balance - int(amount)
                wallet.save() 
                trx = Transcation.objects.create(transaction_type=transaction_type, transaction_by=wallet.account, amount = amount)
            wallet_serializer = serializer_class(wallet, context={'trx_type': transaction_type})
            return_data = {
                "deposit" : wallet_serializer.data
            }
            status = "success"
        else:
            return_data = {
                "error:" : 'Wallet is not enabled, please enable the wallet 1st to proceed further'
            }
            status = "failure"
        response = build_response(status, return_data)
        return response
    except Exception as exc:
        return_data = {
            "error:" : str(exc)
            }
        response = build_response('failure', return_data)
        return response


def disable_wallet(user):
    try:
        wallet = user.account.wallet
        if wallet.status:
            wallet.status = False
            wallet.save()
            serializer_wallet = WalletDisableSerializer(wallet)
            status = 'success'
            return_data = {
                "wallet:" : serializer_wallet.data
            }
        else:
            status = 'failure'
            return_data = {
                "error:" : "The wallet is already disabled"
            }
        response = build_response(status, return_data)
        return response
    except Exception as exc:
        return_data = {
            "errors:" : str(exc)
        }
        response = build_response('failure', return_data)
        return response

