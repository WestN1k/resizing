from django import forms
from django.core.exceptions import ValidationError
from .models import ImageModel
import urllib


class AddNewImageForm(forms.ModelForm):
    image_url = forms.URLField(label='ссылка', required=False)
    image_file = forms.ImageField(label='Файл', required=False)

    # проверка, должно быть заполнено только одно поле
    def clean(self):
        if self.cleaned_data.get('image_url') and self.cleaned_data.get('image_file'):
            raise forms.ValidationError("Должно быть заполнено только одно поле")

        if not self.cleaned_data.get('image_url') and not self.cleaned_data.get('image_file'):
            raise forms.ValidationError("Должно быть заполнено одно поле")

        if self.cleaned_data.get('image_url'):
            try:
                urllib.request.urlopen(self.cleaned_data.get('image_url'))
            except urllib.error.HTTPError as e:
                print(e)
                raise forms.ValidationError("Ошибка доступа к изображению (возможно такого изображения не существует)")
            except urllib.error.URLError as e:
                print(e)
                raise forms.ValidationError("Неизвестная ошибка соединения")

        return self.cleaned_data

    class Meta:
        model = ImageModel
        fields = ['image_url', 'image_file', ]


class EditImageForm(forms.Form):
    width = forms.IntegerField(min_value=1, max_value=5000, label="Ширина", required=False)
    height = forms.IntegerField(min_value=1, max_value=5000, label="Высота", required=False)
