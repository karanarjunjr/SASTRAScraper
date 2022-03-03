from django import forms

class Email(forms.Form):
    Email = forms.EmailField(
        label="",
        help_text="",
        widget=forms.EmailInput(
            attrs={
                'placeholder' : 'regno@sastra.ac.in',
                'class' : 'form-control mb-4',
                'autofocus' : 'autofocus',
                'required' : 'required',
                'id' : 'inputEmail'
            }
        ), 
        max_length=100
    )