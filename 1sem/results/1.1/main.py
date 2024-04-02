import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import lab_1

def main():
    input_path = os.path.dirname(os.path.realpath(__file__))+"/input"
    output_path = os.path.dirname(os.path.realpath(__file__))+"/output"
    M = 3
    agent = lab_1.Resampling(input_path, output_path)
    agent.upscale_array(M)  

if __name__ == '__main__':
    main()

