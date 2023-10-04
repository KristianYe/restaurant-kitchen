from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Ingredient, DishType, Dish


class UpdateViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password", years_of_experience=10
        )

    def test_ingredient_model_attempt_to_edit_with_wrong_user(self):
        test_model = Ingredient.objects.create(
            name="Test Ingredient", added_by=self.user
        )
        wrong_user = get_user_model().objects.create_user(
            username="wrong_user", password="password", years_of_experience=10
        )

        self.client.force_login(wrong_user)

        url = reverse("kitchen:ingredient-update", args=[test_model.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_dish_type_model_attempt_to_edit_with_wrong_user(self):
        test_model = DishType.objects.create(
            name="Test Dish Type", created_by=self.user
        )
        wrong_user = get_user_model().objects.create_user(
            username="wrong_user", password="password", years_of_experience=10
        )

        self.client.force_login(wrong_user)

        url = reverse("kitchen:dish-type-update", args=[test_model.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_dish_model_attempt_to_edit_with_wrong_user(self):
        test_model = Dish.objects.create(
            name="Test Dish",
            created_by=self.user,
            description="test",
            price=10,
        )
        wrong_user = get_user_model().objects.create_user(
            username="wrong_user", password="password", years_of_experience=10
        )

        self.client.force_login(wrong_user)

        url = reverse("kitchen:dish-update", args=[test_model.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_cook_model_attempt_to_edit_with_wrong_user(self):
        wrong_user = get_user_model().objects.create_user(
            username="wrong_user", password="password", years_of_experience=10
        )

        self.client.force_login(wrong_user)

        url = reverse("kitchen:cook-update", args=[self.user.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
