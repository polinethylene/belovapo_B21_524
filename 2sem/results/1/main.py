import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import lab_2

def main():
    input_path = os.path.dirname(os.path.realpath(__file__))+"/input"
    output_path = os.path.dirname(os.path.realpath(__file__))+"/output"
    agent = lab_2.Binarization(input_path, output_path) 
    agent.array_toGrayScale()

if __name__ == '__main__':
    main()