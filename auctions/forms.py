from datetime import date
import select
from attr import attrs
from django import forms
from django.conf import settings

from auctions.models import Listing, Comment
from .choices import CATEGORY_CHOICES
from django.forms.models import inlineformset_factory

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
    listingCategory = forms.ChoiceField(
        widget=forms.Select(),  
        choices = CATEGORY_CHOICES,
        required=False,
    )

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

    listingBid = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'id':'bid_current_value',
        }),
        max_digits=10,
        decimal_places=2,
        required=False,
    )

    listingImageFile = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'id':'formFile',
            'class':'form-control',
            # 'max-width':'50%',
            # 'height':'50%',
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

    auctionImageFile = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'id':'formFile',
            'class':'form-control',
            'type': 'file',
            'required':'false',
        }),
        required=False,
    )

class CommentsForm(forms.Form):
    commentsCategory = forms.ChoiceField(
        widget=forms.Select(),  
        choices = CATEGORY_CHOICES,
        required=False,
    )    

    commentsContent = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-sm',
            'rows': '3',
            'columns': '100',
        }),
        required=False,
    )

#CommentsFormset = inlineformset_factory(Listing, Comments, extra = 1)

class CategoriesForm(forms.Form):
    categoriesCategory = forms.ChoiceField(
        widget=forms.Select(attrs={'onchange':'loadListing()'}),
        choices = CATEGORY_CHOICES,
        required=False,
    )

    categoriesTitle = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'autofocus':'',
        }),
        max_length=100,
        required=False,
    )

    categoriesContent = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-sm',
            'rows': '3',
            'columns': '100',
        }),
        required=False,
    )

    categoriesPrice = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
        }),
        max_digits=10,
        decimal_places=2,
        required=False,
    )

    categoriesBid = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'id':'bid_current_value',
        }),
        max_digits=10,
        decimal_places=2,
        required=False,
    )

    categoriesImage = forms.ImageField(
        required=False,
    )
