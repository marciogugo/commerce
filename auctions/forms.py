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
            'autofocus':'',
        }),
        max_length=100,
        required=False,
    )

    listingContent = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-sm',
            'rows': '3',
            'columns': '100',
        }),
        required=False,
    )

    listingPrice = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
        }),
        max_digits=10,
        decimal_places=2,
        required=False,
    )

    listingStock = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
        }),
        required=False,
    )

    listingStatus = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm',
        }),
        choices=LISTING_STATUS,
        required=False,
    )

    listingStartDate = forms.DateField(
        widget=forms.DateInput(attrs={
            'placeholder':'dd/mm/yyyy',
            'type':'text', #type date in html5 does not support placeholder attribute
            'onfocus': "(this.type='date')",
            'class': 'form-control dateinput form-control-sm',
        }),
        #format='%m/%d/%Y',
        input_formats=settings.DATE_INPUT_FORMATS,
        initial=date.today,
        required=False,
    )

    listingEndDate = forms.DateField(
        widget=forms.DateInput(attrs={
            'placeholder':'dd/mm/yyyy',
            'type':'text', #type date in html5 does not support placeholder attribute
            'onfocus': "(this.type='date')",
            'class': 'form-control form-control-sm',
        }),
        #format='%d-%m-%Y',
        input_formats=settings.DATE_INPUT_FORMATS,
        initial=date.today,
        required=False,
    )

    listingImageFile = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'id':'formFile',
            'class':'form-control',
            'type': 'file',
            'onchange':'preview()',
            'required':'false',
        }),
        required=False,
    )

class AuctionForm(forms.Form):
    auctionTitle = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'autofocus':'',
        }),
        max_length=100,
        required=False,
    )

    auctionContent = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-sm',
            'rows': '3',
            'columns': '100',
        }),
        required=False,
    )

    auctionPrice = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
        }),
        max_digits=10,
        decimal_places=2,
        required=False,
    )

    auctionBid = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
        }),
        max_digits=10,
        decimal_places=2,
        required=False,
    )

    auctionImageFile = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'id':'formFile',
            'class':'form-control',
            'type': 'file',
            'required':'false',
        }),
        required=False,
    )
