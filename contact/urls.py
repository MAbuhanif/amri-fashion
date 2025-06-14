from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactFormCreateView.as_view(), name='contact-form'),
    path('list/', views.ContactListView.as_view(), name='contact-list'),
    path(
        '<pk>/update',
        views.ContactUpdateView.as_view(),
        name='contact-update'),

    path(
        '<int:pk>/delete',
        views.ContactDeleteView.as_view(),
        name='contact-delete'
        ),

    path('success/', views.ContactSuccess, name='contact-success'),

]
