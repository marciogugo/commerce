from datetime import date
from attr import attrs
from django import forms
from django.conf import settings

LISTING_STATUS = [
    ('A', 'Available'),
    ('U', 'Unavailable'),
    ('S', 'Sold out')
]

class RegisterForm(forms.Form):
    registerFirstName = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'autofocus':'',
        }),
        max_length=40, 
        required=False,
    )

    registerLastName = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'autofocus':'',
        }),
        max_length=40, 
        required=False,
    )

    registerUsername = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus':'',
        }),
        max_length=40, 
    )

    registerEmail = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-mail',
            'autofocus':'',
        }),
        max_length=100, 
    )

    registerPassword = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder': 'Password',
            'autofocus':'',
        }),
        max_length=100, 
    )

    registerConfPassword = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder': 'Confirm Password',
            'autofocus':'',
        }),
        max_length=100, 
    )


class ListingForm(forms.Form):
    listingTitle = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'autofocus':'False',
        }),
        max_length=100,
    )

    listingContent = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-sm',
            'rows': '3',
            'columns': '100',
        }),
    )

    listingPrice = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
        }),
        max_digits=5,
        decimal_places=2,
    )

    listingStock = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
        }),
    )

    listingStatus = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm',
        }),
        choices=LISTING_STATUS,
    )

    listingStartDate = forms.DateField(
        widget=forms.DateInput(attrs={
            'placeholder':'%m/%d/%Y',
            'type':'text', #type date in html5 does not support placeholder attribute
            'onfocus': "(this.type='date')",
            'class': 'form-control dateinput form-control-sm',
        },
        format='%m/%d/%Y',),
        input_formats=settings.DATE_INPUT_FORMATS,
        initial=date.today,
    )

    listingEndDate = forms.DateField(
        widget=forms.DateInput(attrs={
            'placeholder':'mm/dd/yyyy',
            'type':'text', #type date in html5 does not support placeholder attribute
            'onfocus': "(this.type='date')",
            'class': 'form-control form-control-sm',
        },
        format='%m-%d-%Y',),
        initial=date.today
    )

    listingImage = forms.ImageField(
        widget=forms.FileInput(attrs={
            'id':'formFile',
            'class':'form-control',
            'type': 'file',
            'onchange':'preview()',
        })
    )
