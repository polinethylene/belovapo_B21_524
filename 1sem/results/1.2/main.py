import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import lab_1

def main():
    input_path = os.path.dirname(os.path.realpath(__file__))+"/input"
    output_path = os.path.dirname(os.path.realpath(__file__))+"/output"
    N = 3
    agent = lab_1.Resampling(input_path, output_path)
    agent.descale_array(N) 

if __name__ == '__main__':
    main()

