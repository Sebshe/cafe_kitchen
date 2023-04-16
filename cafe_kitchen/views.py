from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView

from cafe_kitchen.forms import DishTypeSearchForm, DishTypeForm, CookSearchForm, CookUpdateForm, DishSearchForm, \
    DishForm
from cafe_kitchen.models import DishType, Dish, Cook


class MainView(TemplateView):
    template_name = 'cafe_kitchen/index.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['dish_types_count'] = DishType.objects.count()
        context['dishes_count'] = Dish.objects.count()
        context['cooks_count'] = Cook.objects.count()
        return context


class DishTypeListView(LoginRequiredMixin, ListView):
    model = DishType
    template_name = 'cafe_kitchen/dish_type_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(num_dishes=Count('dishes'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DishTypeSearchForm(self.request.GET or None)

        return context


class DishTypeCreateView(LoginRequiredMixin, CreateView):
    model = DishType
    template_name = 'cafe_kitchen/dish_type_form.html'
    form_class = DishTypeForm
    success_url = reverse_lazy('cafe_kitchen:types-of-dish')


class DishTypeDetailView(LoginRequiredMixin, DetailView):
    model = DishType
    template_name = 'cafe_kitchen/dish_type_detail.html'


class DishTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = DishType
    template_name = 'cafe_kitchen/dish_type_form.html'
    form_class = DishTypeForm

    def form_valid(self, form):
        return HttpResponseRedirect(self.object.get_absolute_url())


class DishTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = DishType
    template_name = 'cafe_kitchen/dish_type_confirm_delete.html'
    success_url = reverse_lazy('cafe_kitchen:types-of-dish')


class CookListView(LoginRequiredMixin, ListView):
    model = Cook
    template_name = 'cafe_kitchen/cook_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            queryset = Cook.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query)
            )
        else:
            queryset = Cook.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = CookSearchForm(self.request.GET or None)
        return context


class CookDetailView(LoginRequiredMixin, DetailView):
    model = Cook
    template_name = 'cafe_kitchen/cook_detail.html'


class CookUpdateView(LoginRequiredMixin, UpdateView):
    model = Cook
    template_name = 'cafe_kitchen/cook_update_form.html'
    form_class = CookUpdateForm

    def form_valid(self, form):
        return HttpResponseRedirect(self.object.get_absolute_url())


class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    template_name = 'cafe_kitchen/dish_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = DishSearchForm(self.request.GET or None)
        return context


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    template_name = 'cafe_kitchen/dish_form.html'
    form_class = DishForm
    success_url = reverse_lazy('cafe_kitchen:dishes')


class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = Dish
    template_name = 'cafe_kitchen/dish_form.html'
    form_class = DishForm

    def form_valid(self, form):
        return HttpResponseRedirect(self.object.get_absolute_url())


class DishDetailView(LoginRequiredMixin, DetailView):
    model = Dish
    template_name = 'cafe_kitchen/dish_detail.html'


class DishDeleteView(LoginRequiredMixin, DeleteView):
    model = Dish
    template_name = 'cafe_kitchen/dish_confirm_delete.html'
    success_url = reverse_lazy('cafe_kitchen:dishes')
