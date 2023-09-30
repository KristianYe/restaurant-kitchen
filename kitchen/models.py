from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Cook(AbstractUser):
    years_of_experience = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.username})"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return f"{self.name}"


class Dish(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    ingredient = models.ManyToManyField(Ingredient, related_name="dishes")
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE, related_name="dishes")
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dishes")

    class Meta:
        ordering = ["name"]
        verbose_name = "Dish"
        verbose_name_plural = "Dishes"

    def __str__(self) -> str:
        return f"{self.name}: {self.price}"
