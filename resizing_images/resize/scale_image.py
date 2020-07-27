from io import BytesIO
from PIL import Image


# возвращает ширину, высоту изображения
def get_size_image(path_to_image) -> (int, int):
    original_image = Image.open(path_to_image)
    return original_image.size


# изменение размера изображения с сохранением пропорций
def resize_image(path_to_image, width=None, height=None) -> BytesIO:
    try:
        original_image = Image.open(path_to_image)
    except FileNotFoundError as e:
        print(e)

    width_orig, height_orig = get_size_image(path_to_image)

    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, height_orig)
    elif height:
        max_size = (width_orig, height)
    else:
        raise RuntimeError('Width or height required!')

    original_image.thumbnail(max_size, Image.ANTIALIAS) # уменьшение изображения, Image.ANTIALIAS - высокое качество изображения
    thumb_io = BytesIO()
    original_image.save(thumb_io, original_image.format, quality=80)

    return thumb_io