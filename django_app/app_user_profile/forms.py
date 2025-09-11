from django import forms
from .models import Profile


class ProfileModelForm(forms.ModeForm):
    first_name=forms.CharField()
    last_name=forms.CharField()
    class Meta:
        model=Profile
        fields=[
            'first_name',
            'last_name',
            # 'info',
        ]
