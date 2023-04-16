import os

from django.contrib.auth import get_user_model
from django import forms
from django.conf import settings
from django.db.models import Q

from .models import DishType, Dish, Cook


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "placeholder": "Search by name...",
            }
        )
    )


class DishTypeForm(forms.ModelForm):
    name = forms.CharField(
        label='Title',
        required=True,
        widget=forms.TextInput(
                                attrs={
                                    'placeholder': 'Enter name here...'
                                }
                            )
                            )

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'accept': 'image/*'
            }
        )
    )

    class Meta:
        model = DishType
        fields = ['image', 'name', 'description']

    def save(self, commit=True):
        dish_type = super(DishTypeForm, self).save(commit=False)

        if self.cleaned_data["image"]:
            image = self.cleaned_data["image"]
            file_ext = os.path.splitext(image.name)[1]

            new_image_name = f"{dish_type.name}{file_ext}"
            file_path = os.path.join(settings.MEDIA_ROOT, "types_of_dish", new_image_name)

            with open(file_path, 'wb') as new_image_file:
                new_image_file.write(image.read())

            dish_type.image = os.path.join("types_of_dish", new_image_name)

        if commit:
            dish_type.save()

        return dish_type


class CookSearchForm(forms.Form):
    search = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={
        'class': 'form-control mr-sm-2',
        'type': 'search',
        'placeholder': 'Search by first name, last name or username',
        'aria-label': 'Search'
    }))

    def search_cooks(self):
        query = self.cleaned_data.get('search')
        cooks = Cook.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )
        return cooks


class CookUpdateForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'accept': 'image/*'
            }
        )
    )

    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = Cook
        fields = ['image', 'first_name', 'last_name', 'email', 'bio', 'years_of_experience',]
        labels = {
            'years_of_experience': 'Years of Experience',
            'first_name': 'First Name',
            'last_name': "Last Name"
        }

    def save(self, commit=True):
        cook = super(CookUpdateForm, self).save(commit=False)

        if self.cleaned_data["image"]:
            image = self.cleaned_data["image"]
            file_ext = os.path.splitext( image.name )[1]
            username = cook.username.replace(".", "_")
            new_image_name = f"{username}{file_ext}"
            file_path = os.path.join(settings.MEDIA_ROOT, "avatar", new_image_name)

            with open(file_path, 'wb') as new_image_file:
                new_image_file.write(image.read())

            cook.image = os.path.join("avatar", new_image_name)

        if commit:
            cook.save()

        return cook


class DishSearchForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "placeholder": "Search by name...",
            }
        )
    )


class DishForm(forms.ModelForm):
    name = forms.CharField(
        label='Title',
        required=True,
        widget=forms.TextInput(
                                attrs={
                                    'placeholder': 'Enter name here...'
                                }
                            )
        )

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
                'accept': 'image/*'
            }
        )
    )

    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    price = forms.DecimalField(
        required=True,
        max_digits=10,
        decimal_places=2
    )

    dish_type = forms.ModelChoiceField(
        queryset=DishType.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    class Meta:
        model = Dish
        fields = ['image', 'name', 'price', 'description', 'dish_type', 'cooks']

    def save(self, commit=True):
        dish = super(DishForm, self).save(commit=False)

        if self.cleaned_data["image"]:
            image = self.cleaned_data["image"]
            file_ext = os.path.splitext(image.name)[1]

            new_image_name = f"{dish.name}{file_ext}"
            file_path = os.path.join(settings.MEDIA_ROOT, "dish", new_image_name)

            with open(file_path, 'wb') as new_image_file:
                new_image_file.write(image.read())

            dish.image = os.path.join("dish", new_image_name)

            if commit:
                dish.save()

        return dish

