from django import forms
from .models import URL


class URLForm(forms.ModelForm):
    custom_code = forms.CharField(required=False, help_text="Optional custom short link")

    class Meta:
        model = URL
        fields = ["original_url", "custom_code"]
