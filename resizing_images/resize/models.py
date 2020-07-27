import os
from urllib import request
from django.db import models
from django.core.files import File
from .storage import OverwriteStorage


class ImageModel(models.Model):
    image_file = models.ImageField(upload_to='images', verbose_name='Оригинальное изображение')
    image_url = models.URLField(verbose_name='Ссылка на изображение')
    image_resize_file = models.ImageField(upload_to='images/mini', storage=OverwriteStorage(), verbose_name='Измененное изображение', null=True)

    class Meta:
        ordering = ['pk', ]

    def save(self, *args, **kwargs):
        self.get_remote_image()
        super().save(*args, **kwargs)

    # если задан URL, то скачать изображение с URLа и сохранить в image_file
    def get_remote_image(self):
        if self.image_url and not self.image_file:
            result = request.urlretrieve(self.image_url)
            self.image_file.save(
                    os.path.basename(self.image_url),
                    File(open(result[0], 'rb'))
                    )

    # возвращает имя файла
    def filename(self):
        return os.path.basename(self.image_file.name)

    def get_absolute_path(self):
        return self.image_file.path

    def __str__(self):
        return self.filename()
