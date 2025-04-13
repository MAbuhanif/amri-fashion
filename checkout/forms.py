from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels, and set autofocus on the first field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # Set autofocus on the first field
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # Iterate through fields to set placeholders and classes
        for field_name, field in self.fields.items():
            placeholder = f"{placeholders[field_name]}{' *' if field.required else ''}"
            field.widget.attrs.update({
                'placeholder': placeholder,
                'class': 'stripe-style-input',
            })
            field.label = False