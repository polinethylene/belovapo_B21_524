import numpy as np
import os
from PIL import Image

class Filtration:
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

    def median_filtration(self, name, np_img, kernel, output_path, prefix):
        if kernel.shape[0] % 2 == 0:
            return
        print("Processing image "+name)
        H, W = np_img.shape

        p = kernel.shape[0] // 2
        padded_img = np.pad(np_img, p, mode='constant', constant_values=255)

        res_img = np.zeros_like(np_img)

        for i in range(p, H + p):
            for j in range(p, W + p):
                block = padded_img[i-p:i+p+1, j-p:j+p+1]
                kerneled_block = np.ma.masked_array(block, mask=kernel)
                res_img[i-p, j-p] = np.ma.median(kerneled_block)

        output_image = Image.fromarray(res_img)
        output_image.save(output_path+"/"+prefix+name)

        # xor_result = np.bitwise_xor(np_img, output_image)
        abs_diff = np.abs(np.int32(np_img) - np.int32(output_image))
        output_image = Image.fromarray(np.uint8(abs_diff))
        output_image.save(output_path+"/"+"diff_"+prefix+name)
 
    def median_filtration_array(self, kernel, prefix):
        for name, img in self.data.items():
            np_img = np.array(img)
            # gray_img = self.grayScale(np_img)
            # kernel = np.ones((3, 3), dtype=np.uint8)
            self.median_filtration(name, np_img, kernel, self.output_path, prefix)