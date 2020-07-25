import os
from urllib import request
from django.db import models
from django.conf import settings
from django.core.files import File


class ImageModel(models.Model):
    image_file = models.ImageField(upload_to='images', verbose_name='Файл')
    image_url = models.URLField(verbose_name='Ссылка')

    def save(self, *args, **kwargs):
        self.get_remote_image()
        super().save(*args, **kwargs)

    def get_remote_image(self):
        if self.image_url and not self.image_file:
            result = request.urlretrieve(self.image_url)
            self.image_file.save(
                    os.path.basename(self.image_url),
                    File(open(result[0], 'rb'))
                    )
            self.save()