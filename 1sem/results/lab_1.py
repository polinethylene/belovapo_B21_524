import numpy as np
import os
from PIL import Image

class Resampling:
    def __init__(self, input_array, output_path):
        self.data = {}
        self.output_path = output_path
        self.load_img(input_array, True)

    def load_img(self, path, is_folder):
        if is_folder:
            for filename in os.listdir(path):
                if filename.endswith(('.png', '.bmp')):
                    image_path = os.path.join(path, filename)
                    self.data[filename] = Image.open(image_path)
        else:
            self.data[os.path.basename(path)] = Image.open(path)

    def show_img(self):
        for img in self.data:
            img.show()

    def upscale_array(self, M):
        for name, img in self.data.items():
            self.upscale(name, img, M, self.output_path)

    def descale_array(self, N):
        for name, img in self.data.items():
            self.descale(name, img, N, self.output_path)

    def rescale_once_array(self, M, N):
        for name, img in self.data.items():
            self.rescale_once(name, img, M, N, self.output_path)

    def rescale_twice_array(self, M, N):
        for name, img in self.data.items():
            self.rescale_twice(name, img, M, N, self.output_path)

    def upscale(self, name, img, M, output_path):
        print("Processing image "+name+" for upscaling")
        np_img = np.array(img)
        H, W = np_img.shape[:2]
        new_H = H * M
        new_W = W * M
        output_array = np.zeros((new_H, new_W, np_img.shape[2]), dtype=np_img.dtype)
        for y in range(new_H):
            for x in range(new_W):
                orig_y = y // M
                orig_x = x // M
                output_array[y, x] = np_img[orig_y, orig_x]

        output_image = Image.fromarray(output_array)
        output_image.save(output_path+"/"+name)

    def descale(self, name, img, N, output_path):
        print("Processing image "+name+" for descaling")
        np_img = np.array(img)
        H, W = np_img.shape[:2]
        new_H = H // N
        new_W = W // N
        output_array = np.zeros((new_H, new_W, np_img.shape[2]), dtype=np_img.dtype)
        for y in range(new_H):
            for x in range(new_W):
                orig_y = y * N
                orig_x = x * N
                output_array[y, x] = np_img[orig_y, orig_x]

        output_image = Image.fromarray(output_array)
        output_image.save(output_path+"/"+name)

    def rescale_once(self, name, img, M, N, output_path):
        print("Processing image "+name+" for rescaling once")
        np_img = np.array(img)
        H, W = np_img.shape[:2]
        new_H = H * M // N
        new_W = W * M // N
        output_array = np.zeros((new_H, new_W, np_img.shape[2]), dtype=np_img.dtype)
        for y in range(new_H):
            for x in range(new_W):
                orig_y = y * N // M
                orig_x = x * N // M
                output_array[y, x] = np_img[orig_y, orig_x]

        output_image = Image.fromarray(output_array)
        output_image.save(output_path+"/"+name)

    def rescale_twice(self, name, img, M, N, output_path):
        print("Processing image "+name+" for rescaling twice")
        np_img = np.array(img)
        H, W = np_img.shape[:2]
        new_H = H * M
        new_W = W * M
        output_array = np.zeros((new_H, new_W, np_img.shape[2]), dtype=np_img.dtype)
        for y in range(new_H):
            for x in range(new_W):
                orig_y = y // M
                orig_x = x // M
                output_array[y, x] = np_img[orig_y, orig_x]

        H, W = output_array.shape[:2]
        new_H = H // N
        new_W = W // N
        output_2_array = np.zeros((new_H, new_W, np_img.shape[2]), dtype=np_img.dtype)
        for y in range(new_H):
            for x in range(new_W):
                orig_y = y * N
                orig_x = x * N
                output_2_array[y, x] = output_array[orig_y, orig_x]

        output_image = Image.fromarray(output_2_array)
        output_image.save(output_path+"/"+name)