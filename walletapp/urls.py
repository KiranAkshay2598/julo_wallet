from django.urls import path
from walletapp import views


urlpatterns = [
    path('api/v1/init', views.InitialiseWallet.as_view(), name='intialisewallet'),
    path('api/v1/wallet', views.WalletView.as_view(), name='wallet'),
    path('api/v1/wallet/deposits', views.DepositToWallet.as_view(), name='addmoneytowallet'),
    path('api/v1/wallet/withdrawals',
         views.WithdrawalFromWallet.as_view(), name='usemoneyfromwallet'),
]
