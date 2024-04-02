import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import lab_1

def main():
    input_path = os.path.dirname(os.path.realpath(__file__))+"/input"
    output_path = os.path.dirname(os.path.realpath(__file__))+"/output"
    M_1 = 5
    N_1 = 2
    agent = lab_1.Resampling(input_path, output_path)
    agent.rescale_twice_array(M_1, N_1)

if __name__ == '__main__':
    main()

