from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class StaticSitemap(Sitemap):
    def items(self):
        return ['products']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.all()
