import numpy as np
import sys
import os
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from task1.task import main


def process_entropy_calculation(input_str, vert):
    verticals = len(set([ v for v in input_str if v not in ',\n' ]))
    k=5
    max_count_rel = k-1
    count_relation = np.array([[0 for _ in range(5)] for _ in range(verticals)])

    res = main(input_str, vert)
    matrix = [res[0], res[1], res[2], res[3], res[4]]

    # заполнение количества исходящих связей для каждой вершины
    for j in range(5):
        for i in range(verticals):
            count_relation[i,j] = sum(res[j][i])

    # вероятность появления отношения
    proba_relation = count_relation.copy() / max_count_rel
    enthropy = [-sum(row)*np.log2(sum(row)) for row in proba_relation]
    enthropy = sum(enthropy)
    
    enthropy_ref = 1 / (np.exp(1) * np.log(2)) * verticals * k
    enthropy_norm = enthropy / enthropy_ref
    
    return enthropy, enthropy_norm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='Входная строка')
    parser.add_argument('--root', type=str, required=True, help='Корневая вершина')
    
    args = parser.parse_args()
    
    input_str = args.input
    vert = args.root
    
    enthropy, enthropy_norm = process_entropy_calculation(input_str, vert)
    
    print('Энтропии структуры графа - ', enthropy)
    print('Нормализированная энтропия - ', enthropy_norm)

if __name__ == "__main__":
    main()