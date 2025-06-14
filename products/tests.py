from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category

class ProductViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.category1 = Category.objects.create(name='Cat1')
        self.category2 = Category.objects.create(name='Cat2')
        self.product1 = Product.objects.create(
            name="Alpha Product",
            price=10.00,
            description="Test Alpha",
            category=self.category1
        )
        self.product2 = Product.objects.create(
            name="Beta Product",
            price=20.00,
            description="Test Beta",
            category=self.category2
        )

    def test_all_products_view(self):
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_detail_view(self):
        url = reverse('product_detail', args=[self.product1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_add_product_view_as_superuser(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('add_product')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Test POST
        response = self.client.post(url, {
            'name': 'New Product',
            'price': 20.00,
            'description': 'New Desc',
            'category': self.category1.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

    def test_add_product_view_as_normal_user(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('add_product')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect (not allowed)

    
    def test_edit_product_view_as_superuser(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('edit_product', args=[self.product1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Test POST
        response = self.client.post(url, {
            'name': 'Updated Product',
            'price': 15.00,
            'description': 'Updated Desc',
            'category': self.category1.id
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after edit
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Updated Product')

    def test_edit_product_view_as_normal_user(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('edit_product', args=[self.product1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Should redirect (not allowed)

    def test_delete_product_view_as_superuser(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('delete_product', args=[self.product1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Test POST
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Should redirect after delete
        self.assertFalse(Product.objects.filter(id=self.product1.id).exists())

    def test_delete_product_view_as_normal_user(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('delete_product', args=[self.product1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Should redirect (not allowed)


    def test_sort_products_by_price(self):
        url = reverse('products') + '?sort=price&direction=asc'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertLessEqual(products[0].price, products[-1].price)

    def test_filter_products_by_category(self):
        url = reverse('products') + f'?category={self.category1.name}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        for product in products:
            self.assertEqual(product.category, self.category1)

    def test_search_products(self):
        url = reverse('products') + '?q=Alpha'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertTrue(any('Alpha' in product.name for product in products))
