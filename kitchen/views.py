from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, QuerySet
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from kitchen.forms import (
    DishForm,
    DishSearchForm,
    DishTypeSearchForm,
    CookSearchForm,
    IngredientSearchForm,
)
from kitchen.models import Cook, Dish, DishType, Ingredient


@login_required
def index(request) -> HttpResponse:
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    context = {
        "num_cooks": num_cooks,
        "num_dish_types": num_dish_types,
        "num_dishes": num_dishes,
    }

    return render(request, "kitchen/index.html", context=context)


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Adding SearchForm to the context for use in html template
        and saving previous data in search field
        """

        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(initial={"name": name})
        return context

    def get_queryset(self) -> QuerySet:
        """Filtering dishes by name, received from DishSearchForm"""

        queryset = Dish.objects.all()
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")
    template_name = "kitchen/dish_form.html"

    def form_valid(self, form) -> "model form":
        """Auto set current logged-in user to created dish"""

        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"

    def get_object(self, queryset=None) -> "model instance":
        """
        Only creator can update dish
        This function checks that logged-in user == creator
        """

        obj = super().get_object(queryset)

        if obj.created_by != self.request.user:
            raise Http404("You don't have access to this page")

        return obj


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")

    def get_object(self, queryset=None) -> "model instance":
        """
        Only creator can delete dish
        This function checks that logged-in user == creator
        """

        obj = super().get_object(queryset)

        if obj.created_by != self.request.user:
            raise Http404("You don't have access to this page")

        return obj


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Adding SearchForm to the context for use in html template
        and saving previous data in search field
        """

        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(initial={"name": name})
        return context

    def get_queryset(self) -> QuerySet:
        """Filtering dish types by name, received from DishSearchForm"""

        queryset = DishType.objects.all().annotate(Count("dishes"))
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = ["name"]
    template_name = "kitchen/dish_type_form.html"
    context_object_name = "dish_type"
    success_url = reverse_lazy("kitchen:dish-type-list")

    def form_valid(self, form) -> "model form":
        """Auto set current logged-in user to created dish type"""

        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = ["name"]
    template_name = "kitchen/dish_type_form.html"
    context_object_name = "dish_type"

    def get_object(self, queryset=None) -> "model instance":
        """
        Only creator can update dish type
        This function checks that logged-in user == creator
        """

        obj = super().get_object(queryset)

        if obj.created_by != self.request.user:
            raise Http404("You don't have access to this page")

        return obj


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    template_name = "kitchen/dish_type_detail.html"
    context_object_name = "dish_type"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Adding bool value to context to check
        if there are any created dishes with specific dish type
        """

        context = super().get_context_data(**kwargs)
        created_dishes = bool(list(self.get_object().dishes.all()))
        context["created_dishes"] = created_dishes
        return context


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")
    context_object_name = "dish_type"

    def get_object(self, queryset=None) -> "model instance":
        """
        Only creator can delete dish type
        This function checks that logged-in user == creator
        """

        obj = super().get_object(queryset)

        if obj.created_by != self.request.user:
            raise Http404("You don't have access to this page")

        return obj


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Adding SearchForm to the context for use in html template
        and saving previous data in search field
        """

        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = CookSearchForm(initial={"name": name})
        return context

    def get_queryset(self) -> QuerySet:
        """Filtering cooks by name or username, received from DishSearchForm"""

        queryset = get_user_model().objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                Q(first_name__icontains=form.cleaned_data["name"])
                | Q(last_name__icontains=form.cleaned_data["name"])
                | Q(username__icontains=form.cleaned_data["name"])
            )
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Adding bool value to context to check
        if there are any created dishes by specific cook
        """

        context = super().get_context_data(**kwargs)
        created_dishes = bool(list(self.get_object().created_dishes.all()))
        context["created_dishes"] = created_dishes
        return context


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = ["user_image"]

    def get_object(self, queryset=None) -> "model instance":
        """
        Only a specific cook can update himself
        This function checks that logged-in user == cook
        """

        obj = super().get_object(queryset)

        if obj != self.request.user:
            raise Http404("You don't have access to this page")

        return obj


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = ["name"]
    success_url = reverse_lazy("kitchen:ingredient-list")

    def form_valid(self, form) -> "model form":
        """Auto set current logged-in user to created ingredient"""

        form.instance.added_by = self.request.user
        return super().form_valid(form)


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Adding SearchForm to the context for use in html template
        and saving previous data in search field
        """

        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(initial={"name": name})
        return context

    def get_queryset(self) -> QuerySet:
        """Filtering ingredients by name, received from DishSearchForm"""

        queryset = Ingredient.objects.all()
        form = IngredientSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class IngredientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ingredient

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Adding bool value to context to check
        if there are any created dishes with specific ingredient
        """

        context = super().get_context_data(**kwargs)
        dishes_with_obj = bool(list(self.get_object().dishes.all()))
        context["dishes_with_obj"] = dishes_with_obj
        return context


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = ["name"]

    def get_object(self, queryset=None) -> "model instance":
        """
        Only creator can update ingredient
        This function checks that logged-in user == creator
        """

        obj = super().get_object(queryset)

        if obj.added_by != self.request.user:
            raise Http404("You don't have access to this page")

        return obj


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")

    def get_object(self, queryset=None) -> "model instance":
        """
        Only creator can delete ingredient
        This function checks that logged-in user == creator
        """

        obj = super().get_object(queryset)

        if obj.added_by != self.request.user:
            raise Http404("You don't have access to this page")

        return obj
