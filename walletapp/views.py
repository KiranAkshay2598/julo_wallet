from django.db.models.fields import reverse_related
from django.shortcuts import render
from rest_framework.views import APIView
from walletapp import serializers
from walletapp.services import *
from walletapp.serializers import *
from rest_framework.response import Response

class InitialiseWallet(APIView):
    serializer_class = InitSerializer

    def post(self, request):
        serializer = InitSerializer(data=request.POST)
        if serializer.is_valid():
            response = initialise_wallet(serializer.validated_data)
            if response['status'] == "success":
                status=201
            else:
                status=400
            return Response(response, status=status)
        else:
            return Response(serializer.errors,status=400)


class WalletView(APIView):
    def get(self, request):
        response = view_wallet(user=request.user, only_view=True)
        if response['status'] == 'success':
            status = 200
        else:
            status = 400
        return Response(response, status=status)

    def post(self, request):
        response = view_wallet(user=request.user)
        if response['status'] == 'success':
            status = 201
        else:
            status = 400
        return Response(response, status=status)

    def patch(self, request):
        user = request.user
        response = disable_wallet(user)
        if response['status'] == 'success':
            status = 200
        else:
            status = 400
        return Response(response, status=status)
    



class DepositToWallet(APIView):
    def post(self, request):
        user = request.user
        amount = request.POST.get('amount')
        if not amount:
            return Response("Ammount is a required field", status=400)
        response = transcation_wallet(user, amount, 'deposit')
        if response['status'] == 'success':
            status = 200
        else:
            status = 400
        return Response(response, status=status)


class WithdrawalFromWallet(APIView):
    def post(self, request):
        user = request.user
        amount = request.POST.get('amount')
        if not amount:
            return Response("Amount is a required field", status=400)
        response = transcation_wallet(user, amount, 'withdraw')
        if response['status'] == 'success':
            status = 200
        else:
            status = 400
        return Response(response, status=status)



    
