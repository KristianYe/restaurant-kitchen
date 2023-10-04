from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Ingredient, DishType, Dish


class CreateModelsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password", years_of_experience=10
        )
        self.client.force_login(self.user)

    def test_dish_type_created_by_auto_populated(self):
        response = self.client.post(
            reverse("kitchen:dish-type-create"),
            {"name": "Test Dish Type"}
        )

        self.assertEqual(response.status_code, 302)

        created_object = DishType.objects.first()

        self.assertEqual(created_object.created_by, self.user)

    def test_dish_created_by_auto_populated(self):
        test_dish_type = DishType.objects.create(name="test")
        test_ingredient = Ingredient.objects.create(name="test")
        response = self.client.post(
            reverse("kitchen:dish-create"),
            {
                "name": "Test Dish",
                "description": "test",
                "price": 10,
                "dish_type": test_dish_type.pk,
                "ingredients": [test_ingredient.pk]
            }
        )

        self.assertEqual(response.status_code, 302)

        created_object = Dish.objects.first()

        self.assertEqual(created_object.created_by, self.user)


    def test_ingredient_added_by_auto_populated(self):
        response = self.client.post(
            reverse("kitchen:ingredient-create"),
            {"name": "test"}
        )

        self.assertEqual(response.status_code, 302)

        created_object = Ingredient.objects.first()

        self.assertEqual(created_object.added_by, self.user)
