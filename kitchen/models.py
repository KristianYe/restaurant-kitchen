from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=63, unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="dish_types",
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("kitchen:dish-type-detail", kwargs={"pk": self.pk})


class Cook(AbstractUser):
    years_of_experience = models.IntegerField()
    user_image = models.ImageField(upload_to="cooks", null=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.username})"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    name = models.CharField(max_length=63, unique=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="ingredients",
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("kitchen:ingredient-detail", kwargs={"pk": self.pk})


class Dish(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    ingredients = models.ManyToManyField(Ingredient, related_name="dishes")
    dish_type = models.ForeignKey(
        DishType, on_delete=models.SET_NULL, related_name="dishes", null=True
    )
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="dishes"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_dishes",
        on_delete=models.SET_NULL,
        null=True
    )
    image = models.ImageField(upload_to="dishes", null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"

    def __str__(self) -> str:
        return f"{self.name}: {self.price}"

    def get_absolute_url(self):
        return reverse("kitchen:dish-detail", kwargs={"pk": self.pk})
