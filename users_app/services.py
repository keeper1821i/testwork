from PIL import Image


def watermark_photo(input_image_path):
    """Функция добавления водяного знака"""
    position = (0, 0)
    base_image = Image.open('media/' + input_image_path)
    watermark = Image.open('media/water_mark.jpg')

    base_image.paste(watermark, position)
    base_image.save('media/' + input_image_path)

