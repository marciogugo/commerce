from attr import attrs
from django import forms

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
            'id':'listingTitle',
            'class': 'form-control',
            'autofocus':'',
        }),
        max_length=100,
    )

    listingContent = forms.CharField(
        widget=forms.Textarea(attrs={
            'id':'listingContent',
            'class': 'form-control',
            'rows': '3',
            'columns': '200',
        }),
    )

    listingPrice = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        max_digits=5,
        decimal_places=2,
    )

    listingStock = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
    )

    listingStatus = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        choices=LISTING_STATUS,
    )

    listingStartDate = forms.DateField(
        widget=forms.SelectDateWidget(attrs={
            'class': 'form-control',
        }),
    )

    listingEndDate = forms.DateField(
        widget=forms.SelectDateWidget(attrs={
            'class': 'form-control',
        }),
    )

    listingImage = forms.ImageField(
        
    )
