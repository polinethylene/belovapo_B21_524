import numpy as np
import os
from PIL import Image

class Binarization:
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

    def array_toGrayScale(self):
        for name, img in self.data.items():
            np_img = np.array(img)
            gray_img = self.grayScale(np_img)
            output_image = Image.fromarray(gray_img)
            output_image.save(self.output_path+"/"+name)

    def grayScale(self, np_img):
        return np.uint8(0.3 * np_img[:, :, 0] + 0.59 * np_img[:, :, 1] + 0.11 * np_img[:, :, 2])

    def calc_mean_and_std_matrix(self, np_img, w):
        H, W = np_img.shape[:2]
        NP = H*W
        padded_img = np.pad(np_img, ((w, w), (w, w)), mode='constant', constant_values=255)
        mean = np.zeros((H, W))
        std = np.zeros((H, W))
        for i in range(w, H+w):
            for j in range(w, W+w):
                block = padded_img[i-w:i+w+1, j-w:j+w+1]
                mean[i-w,j-w] = block.mean()
                std[i-w,j-w] = block.std()
                # std[i-w,j-w] = np.sqrt(np.sum(block-mean[i-w,j-w])/NP)
        return mean,std

    def niBlack_binarization(self, name, np_img, w, k, output_path, glob_max=-1, glob_min=-1):
        print("Processing image "+name)
        H, W = np_img.shape
        res_img = np.zeros((H, W), dtype=np.uint8)
        padded_img = np.pad(np_img, ((w, w), (w, w)), mode='constant', constant_values=255)
        # mean, std = self.calc_mean_and_std_matrix(np_img, w)
        # print("Calculated matrix")
        if glob_max == -1: 
            glob_max = max(np_img)
        if glob_min == -1: 
            glob_min = min(np_img)
        
        for i in range(w, H+w):
            for j in range(w, W+w):
                if np_img[i-w,j-w] >= glob_max:
                    res_img[i-w,j-w] = 255
                    continue
                if np_img[i-w,j-w] <= glob_min:
                    res_img[i-w,j-w] = 0
                    continue

                block = padded_img[i-w:i+w+1, j-w:j+w+1]
                mean = block.mean()
                std = block.std()
                t = (mean + k * std)
                if (np_img[i-w,j-w] < t):
                    res_img[i-w,j-w] = 0
                else:
                    res_img[i-w,j-w] = 255

        output_image = Image.fromarray(res_img)
        output_image.save(output_path+"/"+name)
 
    def binarize(self, w,k, glob_max=-1, glob_min=-1):
        for name, img in self.data.items():
            np_img = np.array(img)
            gray_img = self.grayScale(np_img)
            self.niBlack_binarization(name, gray_img, w, k, self.output_path, glob_max, glob_min)