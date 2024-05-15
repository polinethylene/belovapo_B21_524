import numpy as np
import os
from PIL import Image

class Contour:
    def __init__(self, input_array, output_path):
        self.data = {}
        self.output_path = output_path
        self.load_img(input_array, True)
        self.Gx = np.array([[-1.0, -2.0, -1.0], [0.0, 0.0, 0.0], [1.0, 2.0, 1.0]])
        self.Gy = np.array([[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]])

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
    
    def contour_detection(self, name, np_img, output_path, thr):
        print("Processing image "+name)
        padded_img = np.pad(np_img, 1, mode='constant', constant_values=255)
        G = np.zeros_like(np_img)
        Gx_ = np.zeros_like(np_img, dtype=float)
        Gy_ = np.zeros_like(np_img, dtype=float)

        H, W = padded_img.shape
        for i in range(H - 2):
            for j in range(W - 2):
                gx = np.sum(np.multiply(self.Gx, padded_img[i:i + 3, j:j + 3])) 
                gy = np.sum(np.multiply(self.Gy, padded_img[i:i + 3, j:j + 3])) 
                Gx_[i,j] = gx
                Gy_[i,j] = gy
                G[i, j] = np.sqrt(gx ** 2 + gy ** 2)  
        
        # np.putmask(G, G > 255, 255)
        # np.putmask(G, G < 0, 0)
        G_n = (G * (255.0/G.max())).astype(np.uint8)
        gx_n = (Gx_ * (255.0/Gx_.max())).astype(np.uint8)
        gy_n= (Gy_ * (255.0/Gy_.max())).astype(np.uint8)
        
        output_image = Image.fromarray(G_n)
        output_image.save(output_path+"/"+"g_"+name)
        output_image = Image.fromarray(gx_n)
        output_image.save(output_path+"/"+"gx_"+name)
        output_image = Image.fromarray(gy_n.astype(np.uint8))
        output_image.save(output_path+"/"+"gy_"+name)
        res_image = np.where(G > thr, 255, 0)
        output_image = Image.fromarray(res_image.astype(np.uint8))
        output_image.save(output_path+"/"+name)

    def contour_detection_array(self, thr):
        for name, img in self.data.items():
            np_img = np.array(img)
            gray_img = self.grayScale(np_img)
            output_image = Image.fromarray(gray_img)
            output_image.save(self.output_path+"/"+"gray"+name)
            self.contour_detection(name, gray_img, self.output_path,thr)

def main():
    input_path = os.path.dirname(os.path.realpath(__file__))+"/input"
    output_path = os.path.dirname(os.path.realpath(__file__))+"/output"
    thr = 120

    agent = Contour(input_path, output_path)
    agent.contour_detection_array(thr)

if __name__ == '__main__':
    main()