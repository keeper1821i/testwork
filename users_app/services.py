from PIL import Image

from django.db.models.functions import Sin, Radians, Cos, ATan2, Sqrt


def watermark_photo(input_image_path):
    """Функция добавления водяного знака"""
    position = (0, 0)
    base_image = Image.open('media/' + input_image_path)
    watermark = Image.open('media/water_mark.jpg')

    base_image.paste(watermark, position)
    base_image.save('media/' + input_image_path)


def distance_on_sphere(lat1, lon1, lat2, lon2):
    """Функция рассчета расстояния между пользователя по координатам"""
    phi1 = Radians(lat1)
    phi2 = Radians(lat2)
    delta_phi = Radians(lat2 - lat1)
    delta_lambda = Radians(lon2 - lon1)
    radius = 6371

    a = Sin(delta_phi / 2) ** 2 + Cos(phi1) * Cos(phi2) * Sin(delta_lambda / 2) ** 2
    c = 2 * ATan2(Sqrt(a), Sqrt(1 - a))

    d = radius * c
    return d

