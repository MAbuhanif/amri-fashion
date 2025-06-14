from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from checkout.models import Order
from django.utils import timezone
from django.urls import reverse


# ------------ MODEL TESTING ------------

class TestUserProfile(TestCase):
    """Tests the UserProfile model in the profiles app."""

    def setUp(self):
        """
        Makes a sample user & uses signal to create a linked
        UserProfile object
        """

        username1 = "testUserStaff"
        email1 = "testuser@test.com"
        password = "default123"
        first_name = "Test"
        last_name = "User"

        user1 = User.objects.create(
            username=username1,
            email=email1,
            password=password,
            first_name=first_name,
            last_name=last_name
            )

        user1.save()

    def test_str(self):
        """Tests the string method on the userprofile."""
        # Retrieves the most recently created profile and gets its string
        profile1 = UserProfile.objects.latest('pk')
        profile_string = str(profile1.user.username)

        # Cofirms the profile string is correct.
        self.assertEqual((profile_string), (profile1.user.username))


# ------------ VIEWS TESTING ------------

class ProfilesViewTestCase(TestCase):
    """
    Test case for testing profiles views.
    """

    def setUp(self):
        """
        Creates two sample users, one of whom has staff & superuser
        privileges (testUserStaff) and another who does not (testUser).
        Then creates a sample order.
        """

        username1 = "testUserStaff"
        email1 = "testuser@test.com"
        password = "default123"
        first_name = "Test"
        last_name = "User"

        username2 = "testUser"
        email2 = "testuser2@test.com"
        password = "default123"
        first_name = "Test"
        last_name = "User"

        user1 = User.objects.create(
            username=username1,
            email=email1,
            password=password,
            first_name=first_name,
            last_name=last_name
            )

        user2 = User.objects.create(
            username=username2,
            email=email2,
            password=password,
            first_name=first_name,
            last_name=last_name
            )

        user2.is_staff = True
        user2.is_superuser = True

        user1.save()
        user2.save()

        order_number = 000000000000
        user_profile = UserProfile.objects.latest('pk')
        full_name = 'test_name'
        email = 'test_email'
        phone_number = '0000000000'
        country = 'US'
        postcode = '42424'
        town_or_city = 'test_town'
        street_address1 = 'test_street'
        date = timezone.now()
        order_total = '99.99'
        grand_total = '99.99'
        original_bag = 'test_original_bag'
        stripe_pid = 'test_stripe_pid'

        order1 = Order.objects.create(
            order_number=order_number,
            user_profile=user_profile,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            country=country,
            postcode=postcode,
            town_or_city=town_or_city,
            street_address1=street_address1,
            date=date,
            order_total=order_total,
            grand_total=grand_total,
            original_bag=original_bag,
            stripe_pid=stripe_pid
            )

        order1.save()

    
    def test_profile_render_context(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    