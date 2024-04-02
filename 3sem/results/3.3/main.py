import sys
import os
import numpy as np
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import lab_3

def make_cross_kernel(size):
    kernel = np.ones((size, size), dtype=np.uint8)
    for i in range(kernel.shape[0]):
        kernel[i, kernel.shape[0]//2] = 0
        kernel[kernel.shape[0]//2,i] = 0
    return kernel

def make_cross_kernel_diag(size):
    kernel = np.ones((size, size), dtype=np.uint8)
    for i in range(kernel.shape[0]):
        kernel[i, i] = 0
        kernel[i,kernel.shape[0]-i-1] = 0
    return kernel

def main():
    input_path = os.path.dirname(os.path.realpath(__file__))+"/input"
    output_path = os.path.dirname(os.path.realpath(__file__))+"/output"
    agent = lab_3.Filtration(input_path, output_path)
    kernel_1 = np.zeros((5, 5), dtype=np.uint8)
    kernel_2 = make_cross_kernel(7)
    kernel_3 = make_cross_kernel_diag(7)

    agent.median_filtration_array(kernel_1, "")
    agent.median_filtration_array(kernel_2, "cross_")
    agent.median_filtration_array(kernel_3, "diag_")

if __name__ == '__main__':
    main()