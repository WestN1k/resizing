import os
from django.shortcuts import reverse, render
from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView, DetailView, CreateView
from django.core.files.base import ContentFile
from . import scale_image
from .forms import AddNewImageForm, EditImageForm
from .models import ImageModel


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
            scaled_image = scale_image.resize_image(self.object.get_absolute_path(), form.cleaned_data.get('width'), form.cleaned_data.get('height'))
            if scaled_image:
                    self.object.image_resize_file.save(self.object.filename(), ContentFile(scaled_image.getvalue()), save=True)
        return self.form_invalid(form)
