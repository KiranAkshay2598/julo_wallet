from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from walletapp.models import Wallet, Account


class WalletTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcustomer1')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.account = Account.objects.create(customer_xid="testcustomer1", user=self.user)
        self.wallet = Wallet.objects.create(account=self.account)
        self.wallet.status = True
        self.wallet.save()

    def test_registration_success(self):
        data = {"customer_xid": "testcustomer2"}
        response = self.client.post("/api/v1/init", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_failure(self):
        response = self.client.post("/api/v1/init", data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_view_post(self):
        self.wallet.status = False
        self.wallet.save()
        response = self.client.post("/api/v1/wallet")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wallet_view_post_failure(self):
        response = self.client.post("/api/v1/wallet")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_view_get(self):
        response = self.client.get("/api/v1/wallet")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wallet_view_get_failure1(self):
        self.wallet.status = False
        self.wallet.save()
        response = self.client.get("/api/v1/wallet")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wallet_view_patch(self):
        data = {'is_disabled': True}
        response = self.client.patch("/api/v1/wallet", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wallet_view_patch_failure(self):
        self.wallet.status = False
        self.wallet.save()
        response = self.client.patch("/api/v1/wallet")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deposit(self):
        data = {"amount": 1000, 'reference_id':'test_ref_id_1'}
        response = self.client.post("/api/v1/wallet/deposits", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_deposit_failure(self):
        response = self.client.post("/api/v1/wallet/deposits")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deposit_failure1(self):
        data = {"amount": 1000, 'reference_id':'test_ref_id_1'}
        self.wallet.status = False
        self.wallet.save()
        response = self.client.post("/api/v1/wallet/deposits", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_withdrawl(self):
        self.wallet.balance = 1000
        self.wallet.save()
        data = {"amount": 300, 'reference_id':'test_ref_id_1'}
        response = self.client.post("/api/v1/wallet/withdrawals", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_withdrawl_failure(self):
        response = self.client.post("/api/v1/wallet/withdrawals")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_withdrawl_failure1(self):
        data = {"amount": 300, 'reference_id':'test_ref_id_1'}
        self.wallet.status = False
        self.wallet.save()
        response = self.client.post("/api/v1/wallet/withdrawals", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
