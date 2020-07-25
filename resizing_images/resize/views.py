import os
import urllib.request
from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
from django.core.files import File
from django.views.generic import TemplateView, FormView, DetailView, CreateView
from .forms import AddNewImageForm, EditImageForm
from .models import ImageModel


class IndexView(TemplateView):
    template_name = 'resize/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['images'] = ImageModel.objects.all()
        get_images()
        return context

class AddNewImageView(CreateView):
    template_name = 'resize/add_new_image.html'
    form_class = AddNewImageForm
    model = ImageModel


class EditImageView(DetailView):
    template_name = 'resize/edit_image.html'
    model = ImageModel
    pk_url_kwarg = 'image_name'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = EditImageForm()
        return context

def get_images():
    print(os.path.join(settings.MEDIA_ROOT, 'images'))


# def upload_image_from_url(url):
#     image = urllib.request.urlretrieve(url)
#     animal = Animal.objects.create(name='Dog')
#     fname = os.path.basename(url)

#     with open(image[0]) as fp:
#         animal.photo.save(fname, File(fp))
#         animal.save()