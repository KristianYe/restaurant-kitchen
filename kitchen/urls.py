from django.urls import path

from kitchen.views import index, DishListView, DishTypeListView, CookListView

urlpatterns = [
    path("", index, name="index"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("cooks/", CookListView.as_view(), name="cook-list")
]

app_name = "kitchen"
