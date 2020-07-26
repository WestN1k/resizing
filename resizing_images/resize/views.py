import os
import urllib.request
from io import BytesIO
from django.contrib import messages
from django.shortcuts import render, reverse
from django.conf import settings
from django.core.files import File
from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView, DetailView, CreateView
from .forms import AddNewImageForm, EditImageForm
from .models import ImageModel
from django.core.files.base import ContentFile
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
            scaled_image = resize_image(self.object.get_absolute_path(), form.cleaned_data.get('width'), form.cleaned_data.get('height'))
            if scaled_image:
                if self.object.image_resize_file:
                    self.object.image_resize_file = ContentFile(scaled_image.getvalue())
                    self.object.save()
                else:
                    self.object.image_resize_file.save(self.object.filename(), ContentFile(scaled_image.getvalue()), save=False)
        return self.form_invalid(form)


# возвращает ширину, высоту изображения
def get_size_image(path_to_image):
    original_image = Image.open(path_to_image)
    return original_image.size


# изменение размера изображения с сохранением пропорций
def resize_image(path_to_image, width=None, height=None) -> BytesIO:
    try:
        original_image = Image.open(path_to_image)
    except FileNotFoundError as e:
        print(e)
        return False

    width_orig, height_orig = get_size_image(path_to_image)
    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, height_orig)
    elif height:
        max_size = (width_orig, height)
    else:
        raise RuntimeError('Width or height required!')

    # уменьшение изображения, Image.ANTIALIAS для сохранения высокого качества изображения
    original_image.thumbnail(max_size, Image.ANTIALIAS)
    thumb_io = BytesIO()
    original_image.save(thumb_io, original_image.format, quality=80)

    return thumb_io