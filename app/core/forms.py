from django import forms

from core.models import HomePage


class HomePageForm(forms.ModelForm):
    class Meta:
        model = HomePage
        fields = '__all__'
        labels = {
            'name': 'Website Title',
            'description': 'Website Short Description',
        }