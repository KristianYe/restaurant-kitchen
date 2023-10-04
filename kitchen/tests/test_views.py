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


class ListViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password", years_of_experience=10
        )
        self.dish_type = DishType.objects.create(name="test")
        self.ingredient = Ingredient.objects.create(name="test")
        self.dish = Dish.objects.create(
            name="Test Dish",
            created_by=self.user,
            description="test",
            price=10,
        )
        self.client.force_login(self.user)

    def test_dish_type_searching_feature(self) -> None:
        DishType.objects.create(name="another_test")

        form_data = {"name": "another"}
        response = self.client.get(reverse('kitchen:dish-type-list'), data=form_data)
        queryset = DishType.objects.filter(name__icontains="another")
        self.assertEqual(
            list(response.context["dish_type_list"]), list(queryset)
        )

    def test_ingredient_searching_feature(self) -> None:
        Ingredient.objects.create(
            name="one_more_test",
        )

        form_data = {"name": "more"}
        response = self.client.get(reverse("kitchen:ingredient-list"), data=form_data)
        queryset = Ingredient.objects.filter(name__icontains="more")
        self.assertEqual(list(response.context["ingredient_list"]), list(queryset))

    def test_dishes_searching_feature(self) -> None:
        Dish.objects.create(
            name="third dish",
            created_by=self.user,
            description="test",
            price=10,
        )
        form_data = {"name": "ird "}
        response = self.client.get(reverse("kitchen:dish-list"), data=form_data)
        queryset = Dish.objects.filter(name__icontains="ird ")
        self.assertEqual(list(response.context["dish_list"]), list(queryset))


    def test_cooks_searching_feature(self) -> None:
        get_user_model().objects.create_user(
            username="last_test",
            first_name="hello",
            last_name="world",
            password="password",
            years_of_experience=10
        )

        form_data = {"name": "last_"}
        response = self.client.get(reverse("kitchen:cook-list"), data=form_data)
        queryset = get_user_model().objects.filter(username__icontains="last")
        self.assertEqual(list(response.context["cook_list"]), list(queryset))
        form_data = {"name": "hel"}
        response = self.client.get(reverse("kitchen:cook-list"), data=form_data)
        queryset = get_user_model().objects.filter(first_name__icontains="hel")
        self.assertEqual(list(response.context["cook_list"]), list(queryset))
        form_data = {"name": "world"}
        response = self.client.get(reverse("kitchen:cook-list"), data=form_data)
        queryset = get_user_model().objects.filter(last_name__icontains="world")
        self.assertEqual(list(response.context["cook_list"]), list(queryset))
