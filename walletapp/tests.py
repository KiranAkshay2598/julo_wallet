from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from walletapp.models import Wallet, Account


class WalletTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password="some_strong_psw")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.account = Account.objects.create(full_name="testkiran", user=self.user)
        self.wallet = Wallet.objects.create(account=self.account, balance=0)
        self.wallet.status = True
        self.wallet.save()

    def test_registration_success(self):
        data = {"username": "testcaseregister",
                "password": "some_strong_psw",
                "fullname": "Test Name"}
        response = self.client.post("/api/v1/init", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_failure(self):
        data = {"username": "test_user",
                "password": "some_strong_psw",
                "fullname": "Test Name"}
        response = self.client.post("/api/v1/init", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_failure1(self):
        data = {"password": "some_strong_psw", "fullname": "Test Name"}
        response = self.client.post("/api/v1/init", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"username": "testcaseregister", "fullname": "Test Name"}
        response = self.client.post("/api/v1/init", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"username": "testcaseregister", "password": "some_strong_psw"}
        response = self.client.post("/api/v1/init", data)
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
        response = self.client.patch("/api/v1/wallet")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wallet_view_patch_failure(self):
        self.wallet.status = False
        self.wallet.save()
        response = self.client.patch("/api/v1/wallet")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deposit(self):
        data = {"amount": 1000}
        response = self.client.post("/api/v1/wallet/deposits", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deposit_failure(self):
        response = self.client.post("/api/v1/wallet/deposits")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deposit_failure1(self):
        data = {"amount": 1000}
        self.wallet.status = False
        self.wallet.save()
        response = self.client.post("/api/v1/wallet/deposits", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_withdrawl(self):
        data = {"amount": 300}
        response = self.client.post("/api/v1/wallet/withdrawals", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_withdrawl_failure(self):
        response = self.client.post("/api/v1/wallet/withdrawals")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_withdrawl_failure1(self):
        data = {"amount": 1000}
        self.wallet.status = False
        self.wallet.save()
        response = self.client.post("/api/v1/wallet/withdrawals", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
