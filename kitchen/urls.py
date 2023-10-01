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
    toggle_assign_to_dish,
    DishUpdateView,
    DishTypeUpdateView, DishDeleteView, DishTypeDeleteView
)

urlpatterns = [
    path("", index, name="index"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/create/", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("dishes/<int:pk>/toggle-assign/", toggle_assign_to_dish, name="toggle-dish-assign"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-types/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish-types/<int:pk>/", DishTypeDetailView.as_view(), name="dish-type-detail"),
    path("dish-types/<int:pk>/update/", DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish-types/<int:pk>/delete/", DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("ingredient_create/", IngredientCreateView.as_view(), name="ingredient-create")
    ]

app_name = "kitchen"
