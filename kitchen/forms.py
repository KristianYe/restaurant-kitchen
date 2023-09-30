from django import forms
from django.contrib.auth import get_user_model

from kitchen.models import Ingredient, DishType, Dish


class DishForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    dish_type = forms.ModelChoiceField(
        queryset=DishType.objects.all(),
        widget=forms.Select
    )

    class Meta:
        model = Dish
        fields = "__all__"