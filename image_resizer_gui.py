import os
import settings
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image
import re
import pillow_heif


class ImageResizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("200x50")

        self.output_folder = settings.OUTPUT_FOLDER
        self.file_size_min = settings.FILE_SIZE_MIN

        # ドロップ領域の作成
        self.drop_label = tk.Label(self.root, text="Drag & Drop Images Here", font=("Helvetica", 16), pady=50)
        self.drop_label.pack(fill=tk.BOTH, expand=True)

        # ドロップイベントの設定
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        files = event.data

        print("on_drop")
        print("files : " + files)

        pattern = r"{.+?}|[^ ]+"
        file_paths = re.findall(pattern, files)

        print(file_paths)

        # 出力先フォルダが存在しない場合は作成
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        for file in file_paths:
            # 画像ファイルかどうかを確認
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.heic')):
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
                    if file_size < self.file_size_min:
                        self.save_img(img, file)
                        continue

                    # 画像サイズを半分にリサイズ
                    width, height = img.size
                    resized_img = img.resize((width // 2, height // 2))

                    # リサイズされた画像を保存
                    self.save_img(resized_img, file)

                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")

    def save_img(self, img: Image, file: str):
        try:
            # 保存先ファイル名の生成
            file_name, file_ext = os.path.splitext(os.path.basename(file))
            output_file = os.path.join(self.output_folder, f"{file_name}s.jpg")

            print(f"file_name : {file_name}")

            # リサイズされた画像を保存
            img.save(output_file, 'JPEG')

            print(f"Saved: {output_file}")

        except Exception as e:
            print(f"Error saving {file}: {str(e)}")
