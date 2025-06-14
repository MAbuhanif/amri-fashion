from django.db import models

from django.utils import timezone


class Contact(models.Model):
    class Meta:
        verbose_name_plural = 'Contact Requests'

    SUBJECTS = (
        ('General Inquiry', 'General Inquiry'),
        ('Technical Inquiry', 'Technical Inquiry'),
        ('Pricing Inquiry', 'Pricing Inquiry'),
        ('Business Inquiry', 'Business Inquiry'),
        ('Trouble using the site', 'Trouble using the site'),
        ('Account Issues', "Account Issues"),
        ('Other', "Other"),
    )

    name = models.CharField(max_length=254)
    email = models.EmailField()
    subject = models.CharField(choices=SUBJECTS, max_length=254,)
    message = models.TextField(max_length=1024)
    date_created = models.DateTimeField(default=timezone.now)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return self.email
