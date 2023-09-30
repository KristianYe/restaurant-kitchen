from django.urls import path

from kitchen.views import (
    index,
    DishListView,
    DishTypeListView,
    CookListView,
    DishDetailView,
    DishTypeDetailView,
    CookDetailView,
    DishCreateView,
    DishTypeCreateView,
    IngredientCreateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>", DishDetailView.as_view(), name="dish-detail"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-types/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish-types/<int:pk>", DishTypeDetailView.as_view(), name="dish-type-detail"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/<int:pk>", CookDetailView.as_view(), name="cook-detail"),
    path("ingredient_create/", IngredientCreateView.as_view(), name="ingredient-create")
    ]

app_name = "kitchen"
