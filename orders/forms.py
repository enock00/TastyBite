from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
               "customer_name",
               "phone",
               "email",
               "delivery_zone",
               "address",
        ]

        widgets = {
            "customer_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Full Name"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone Number"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email (Optional)"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Delivery Address"
            }),

            "delivery_zone": forms.Select(attrs={
                "class": "form-control"
}),
        }