"""
URL configuration for amri_fashion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import handler404

from django.contrib.sitemaps.views import sitemap
from products.sitemaps import StaticSitemap, ProductSitemap
from django.views.generic import TemplateView


# Sitemap configuration
sitemaps = {
    'static': StaticSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path('products/', include('products.urls')),
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
    path('profiles/', include('profiles.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('contact/', include('contact.urls')),
    path('faq/', include('faq.urls')),
    path("sitemap.xml/", sitemap, {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom 404 error handler
handler404 = 'amri_fashion.views.handler404'
