import os

import pillow_heif
from PIL import Image

import settings


class ImgResizer:
	def __init__(self):
		self.img_path = settings.IMG_PATH

	def resize(self):
		"""
		画像をリサイズする
		:return:
		"""
		for file in os.listdir(self.img_path):
			if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.heic')):
				print(file)
				file = os.path.join(self.img_path, file)
				try:
					if file.lower().endswith('.heic'):
						heif_file = pillow_heif.read_heif(file)
						img = Image.frombytes(
							heif_file.mode,
							heif_file.size,
							heif_file.data,
							"raw",
							heif_file.mode,
							heif_file.stride,
						)
					else:
						img = Image.open(file)

					# ファイルサイズの取得
					file_size = os.path.getsize(file)
					print(file_size)
					if file_size < settings.FILE_SIZE_MIN:
						self.save_img(img, file)
						continue

					# 画像サイズを半分にリサイズ
					width, height = img.size
					print(f"width : {width}, height : {height}")
					resized_img = img.resize((width // 2, height // 2))

					# リサイズされた画像を保存
					self.save_img(resized_img, file)
				except Exception as e:
					print(e)

	def save_img(self, img, file):


		file_name = os.path.basename(file)
		output_file = os.path.join(settings.IMG_PATH, f"re{file_name}")

		img.save(output_file, 'JPEG')