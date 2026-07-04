from django import forms
from menu.models import FoodItem, Category


class FoodItemForm(forms.ModelForm):

    class Meta:
        model = FoodItem
        fields = "__all__"

        widgets = {
            "category": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "is_available": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "is_featured": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
            "image",
            "description",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
        }