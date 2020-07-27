from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


# переписывает файл на сервере, если он существует
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name