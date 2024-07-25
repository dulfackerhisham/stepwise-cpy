from django import forms
from accounts.models import Profile

class AddressForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fname', 'lname', 'phone', 'email', 'country', 'address', 'city', 'state', 'pincode']