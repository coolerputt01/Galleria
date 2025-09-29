from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import User, VerificationToken,Badge,Theme,UserTheme
import uuid
# Create your tests here.

class UserTestCase(TestCase):
  def setUp(self):
    User.objects.create(email="olumideadekolu9@gmail.com",display_name="coolerputt001",bio="Thank you LORD")
    
  def test_user_account(self):
    user = User.objects.get(display_name="coolerputt001")
    print("User created: ",user)
    

class VerificationTokenTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="olumideadekolu9@gmail.com",
            display_name="TestUser",
            password="password123"
        )

    def test_token_creation(self):
        token = VerificationToken.create_token(user=self.user)
        self.assertIsNotNone(token.token)  # Token UUID exists
        self.assertEqual(token.user, self.user)  # Token linked to correct user
        self.assertFalse(token.is_expired())  # Newly created token not expired

    def test_token_expiration(self):
        token = VerificationToken.create_token(user=self.user, expiry_minutes=0)
        self.assertTrue(token.is_expired())  # Should be expired immediately

    def test_multiple_tokens_for_user(self):
        token1 = VerificationToken.create_token(user=self.user)
        token2 = VerificationToken.create_token(user=self.user)
        self.assertEqual(self.user.verification_tokens.count(), 2)

    def test_token_unique(self):
        token = VerificationToken.create_token(user=self.user)
        # Tokens should be UUIDs, automatically unique
        self.assertIsInstance(token.token, type(uuid.uuid4()))

    def test_token_expiry_logic(self):
        token = VerificationToken.create_token(user=self.user, expiry_minutes=1)
        # Simulate time past expiry
        token.expires_at = timezone.now() - timedelta(seconds=1)
        token.save()
        self.assertTrue(token.is_expired())