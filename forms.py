from django import forms

class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=[('doctor', 'Doctor'), ('patient', 'Patient')])
