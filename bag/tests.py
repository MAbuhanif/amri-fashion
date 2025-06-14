from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product


# ------------ VIEWS TESTING ------------


class bagViewTestCase(TestCase):
    """
    Test case for testing bag views.
    """

    def setUp(self):
        """
        Makes two sample users, one with superuser status and one without.
        Next, makes a sample product object
        """

        username1 = "testUser"
        email1 = "testuser@test.com"
        password = "default123"
        first_name = "Test"
        last_name = "User"

        username2 = "testUserStaff"
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

        name = "test_product"
        description = "test_product_description"
        price = '999.99'
        created_at = timezone.now()
        product1 = Product.objects.create(
            name=name,
            description=description,
            price=price,
            created_at=created_at
            )

        product1.save()

    def test_bag_render_context(self):
        """
        Tests that the bag page is rendered properly
        and the correct context is passed in
        """

        response = self.client.get('/bag/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'bag/bag.html', 'base.html'
            )
        self.assertTemplateUsed(
            response, 'bag/bag.html'
            )

    def test_bag_add(self):
        """
        Adds the test product to the bag, tests whether it has been
        added successfully. Then attempts to add a duplicate item to
        the bag, checks that it is not successful.
        """

        # Get the most recently created product (test product)
        product1 = Product.objects.latest('pk')

        # Try to add the test product to the bag
        response = self.client.post(('/bag/add/1/'), {
            'product_id': 1,
            'quantity': 1,
            'redirect_url': '/',
        }, follow=True)

        # Check that the bag action executes successfully
        self.assertEqual(response.status_code, 200)

        # Check that the test item (id = 1) was added to the bag
        session = self.client.session
        self.assertEqual(session['bag'], {'1': 1})

        # Try to add the test product to the bag again
        response = self.client.post(('/bag/add/1/'), {
            'product_id': 1,
            'quantity': 1,
            'redirect_url': '/',
        })

        # Check that we are redirected
        self.assertEqual(response.status_code, 302)

        # Check that the exception is raised
        self.assertRaises(
            Exception, msg=f'{product1.name} is already in your bag!'
            )

        # Check that a duplicate item was not added to the bag
        self.assertEqual(session['bag'], {'1': 1})

    def test_bag_remove(self):
        """
        Adds the test product to the bag, checks that it was added.
        Then deletes the product from the bag, checks that the
        bag is empty. Next, attempts to delete a non-existant item
        from the bag, checks that it is unsuccessful.
        """

        # Try to add the test product to the bag
        response = self.client.post(('/bag/add/1/'), {
            'product_id': 1,
            'quantity': 1,
            'redirect_url': '/',
        }, follow=True)

        # Check that the bag add action executes successfully
        self.assertEqual(response.status_code, 200)

        # Check that the test item (id = 1) was added to the bag
        session = self.client.session
        self.assertEqual(session['bag'], {'1': 1})

        # Try to remove the test product from the bag
        response = self.client.post('/bag/remove/1/', follow=True)

        # Check that the bag remove action executes successfully
        self.assertEqual(response.status_code, 200)

        # Check that the bag is empty, meaning deletion was successful
        session = self.client.session
        self.assertEqual(session['bag'], {})

        # Try to remove the test product from the bag
        # while the bag is empty
        response = self.client.post('/bag/remove/1/')

        # Check that we are redirected
        self.assertEqual(response.status_code, 302)

        # Check that the error message is raised
        self.assertRaises(
            Exception, msg="Oops, that didn't work, please try again."
            )