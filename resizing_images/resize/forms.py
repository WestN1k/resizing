from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import ImageModel


class AddNewImageForm(forms.ModelForm):
    image_url = forms.URLField(label='ссылка', required=False)
    image_file = forms.ImageField(label='Файл', required=False)

    def clean(self):
        if self.cleaned_data.get('image_url') and self.cleaned_data.get('image_file'):
            raise forms.ValidationError("Должно быть заполнено одно поле")
        
        if not self.cleaned_data.get('image_url') and not self.cleaned_data.get('image_file'):
            raise forms.ValidationError("Должно быть заполнено одно поле")

        return self.cleaned_data

    class Meta:
        model = ImageModel
        fields = ['image_url', 'image_file', ]


class EditImageForm(forms.Form):
    width = forms.IntegerField(min_value=1, max_value=5000, required=False)
    height = forms.IntegerField(min_value=1, max_value=5000, required=False)