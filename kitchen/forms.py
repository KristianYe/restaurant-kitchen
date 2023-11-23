from django import forms
from django.contrib.auth import get_user_model

from kitchen.models import Ingredient, DishType, Dish


class DishForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        label="Ingredients (hold 'ctrl' to select multiple ingredients)"
    )
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        label="Cooks (hold 'ctrl' to select multiple cooks)"
    )
    dish_type = forms.ModelChoiceField(
        queryset=DishType.objects.all(), widget=forms.Select
    )
    image = forms.ImageField(required=False)

    class Meta:
        model = Dish
        fields = "__all__"
        exclude = ["created_by"]


class SearchByNameMixin(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class DishTypeSearchForm(SearchByNameMixin, forms.Form):
    pass


class CookSearchForm(SearchByNameMixin, forms.Form):
    pass


class DishSearchForm(SearchByNameMixin, forms.Form):
    pass


class IngredientSearchForm(SearchByNameMixin, forms.Form):
    pass
