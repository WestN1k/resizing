import os
import urllib.request
from django.contrib import messages
from django.shortcuts import render, reverse
from django.conf import settings
from django.core.files import File
from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView, DetailView, CreateView, FormView
from .forms import AddNewImageForm, EditImageForm
from .models import ImageModel

from PIL import Image


# можно было сделать через ListView, но тяжелее контролировать
class IndexView(TemplateView):
    template_name = 'resize/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['images'] = ImageModel.objects.all()
        return context

class AddNewImageView(CreateView):
    template_name = 'resize/add_new_image.html'
    form_class = AddNewImageForm
    model = ImageModel
    
    def get_success_url(self):
        return reverse('edit_image', kwargs={'pk': self.object.pk})


class EditImageView(FormMixin, DetailView):
    # queryset = ImageModel.objects.all()
    template_name = 'resize/edit_image.html'
    model = ImageModel
    pk_url_kwarg = 'pk'
    form_class = EditImageForm

    # перегрузка страницы, для обновления изображения
    def get_success_url(self):
        return reverse('edit_image', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() # для получения атрибутов объекта
        form = self.get_form()
        if form.is_valid():
            # width, height = get_size_image(self.object.image_file)
            resize_image(self.object.image_file, form.cleaned_data.get('width'), form.cleaned_data.get('height'))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def get_size_image(path_to_image):
    original_image = Image.open(path_to_image)
    return original_image.size


def resize_image(path_to_image, width=None, height=None) -> bool:
    original_image = Image.open(path_to_image)
    width_orig, height_orig = get_size_image(path_to_image)
    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, height_orig)
    elif height:
        max_size = (width_orig, height)
    else:
        raise RuntimeError('Width or height required!')

    output_folder_path = os.path.join(settings.MEDIA_ROOT, 'images', 'mini')

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # придумать, как передавать имя изображения для создания миниатюры + как правильно передать путь до папки с миниатюрами.
    # нужен обработчик для понятия есть ли миниатюра, для ее вывода на edit page (возможно templatetags!!!)
    output_image_path = os.path.join(output_folder_path, '1_mini.jpg')

    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image_path)
 
    scaled_image = Image.open(output_image_path)
    width, height = scaled_image.size

    return True