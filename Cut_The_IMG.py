import PIL
from PIL import Image
from pathlib import *

dir_path = Path(input('Введите путь к папке с файлами: '))
img_type = input("Введите формат изображения вида '*.jpg': ")
img_new_sizex = input("Введите нужную ширину для изображений (X): ")  # 775
img_new_sizey = input("Введите нужную высоту для изображений (Y): ")  # 531
img_cache = list(map(str, dir_path.glob(img_type)))

for i in range(0, len(img_cache)):
	file_name = img_cache[i]
	file_name.replace(" ", "")
	try:
		original = Image.open(file_name)
	except FileNotFoundError:
		print("Файл не найден ")

	width, height = original.size

	if height > width:
		ori_tans = original.transpose(PIL.Image.ROTATE_90)
		size = (int(img_new_sizex), int(img_new_sizey))
		ori_tans.thumbnail(size)
		ori_tans.save(file_name)
		print("Фаил " + file_name + " сохранился")

	else:
		size = (int(img_new_sizex), int(img_new_sizey))
		original.thumbnail(size)
		try:
			original.save(file_name)
		except AttributeError:
			print("Фаил уже сохранен нужно переоткрыть - " + file_name)
