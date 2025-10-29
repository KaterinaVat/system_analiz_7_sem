import numpy as np
from typing import Tuple, List
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from task0.task import print_adjency_matrix
import argparse

def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]], 
    List[List[bool]],
    List[List[bool]],
    List[List[bool]]
]:
    
    def define_matrix(input_str: str) -> Tuple[np.ndarray, List[List[int]]]:

        try:
            s_list = input_str.split('\n')
            max_ind = 0
            pairs = []
            for pair in s_list:
                if not pair.strip():
                    continue
                v1, v2 = pair.split(',')
                v1_int, v2_int = int(v1), int(v2)
                if v1_int < 0 or v2_int < 0:
                    raise ValueError("Отрицательный индекс вершины")
                pairs.append([v1_int, v2_int])
                max_ind = max(max_ind, v1_int, v2_int)
            
            if max_ind <= 0:
                return np.array([], dtype=int), []
            
            matrix = np.zeros((max_ind, max_ind), dtype=int)
            return matrix, pairs
            
        except ValueError as e:
            raise ValueError(f"Ошибка в данных: {e}")
    
    def control_matrix_step_1(matrix_c: np.ndarray, pairs: List[List[int]], current_c: int) -> Tuple[np.ndarray, List[List[int]], List[int]]:
        add_v = []
        processed_pairs = []
        
        for pair in pairs[:]:
            if pair[0] == current_c:
                matrix_c[pair[0]-1][pair[1]-1] = 1
                add_v.append(pair[1])
                processed_pairs.append(pair)
            elif pair[1] == current_c:
                # Для ориентированного графа только прямое управление
                matrix_c[pair[1]-1][pair[0]-1] = 0  # Не добавляем обратную связь
        
        for pair in processed_pairs:
            if pair in pairs:
                pairs.remove(pair)
                
        return matrix_c, pairs, add_v
    
    def control_matrix_step_2(matrix_c: np.ndarray, pairs: List[List[int]], add_v: List[int]) -> Tuple[np.ndarray, List[List[int]], List[int]]:
        processed_pairs = []
        add_n_v = []
        
        for v in add_v:
            current_c = v
            for pair in pairs[:]:
                if pair[0] == current_c:
                    matrix_c[pair[0]-1][pair[1]-1] = 1
                    add_n_v.append(pair[1])
                    processed_pairs.append(pair)
        
        for pair in processed_pairs:
            if pair in pairs:
                pairs.remove(pair)
                
        return matrix_c, pairs, add_n_v
    
    def build_control_matrix(matrix: np.ndarray, pairs: List[List[int]], e_r: int) -> np.ndarray:
        try:
            matrix_c = matrix.copy()
            current_c = e_r
            add_v = []
            
            matrix_c, pairs, add_v = control_matrix_step_1(matrix_c, pairs, current_c)
            
            while pairs and add_v:
                matrix_c, pairs, add_v = control_matrix_step_2(matrix_c, pairs, add_v)
            
            return matrix_c
            
        except Exception as e:
            raise ValueError(f"Ошибка построения матрицы управления: {e}")
    
    def control_indirectly_matrix(control_matrix: np.ndarray) -> np.ndarray:
        if control_matrix is None or len(control_matrix) == 0:
            return np.array([], dtype=int)
            
        n = len(control_matrix)
        closure = control_matrix.copy().astype(bool)
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if closure[i][k] and closure[k][j]:
                        closure[i][j] = True

        indirect_only = closure & (~control_matrix.astype(bool))
        return indirect_only.astype(int)
    
    def comply_cooperative_matrix(control_matrix: np.ndarray) -> np.ndarray:
        if control_matrix is None or len(control_matrix) == 0:
            return np.array([], dtype=int)
            
        n = len(control_matrix)
        comply_coop_matrix = np.zeros((n, n), dtype=int)
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if control_matrix[k][i] and control_matrix[k][j] and i != j:
                        comply_coop_matrix[i][j] = 1
                        comply_coop_matrix[j][i] = 1
                        
        return comply_coop_matrix
    
    def convert_to_bool_matrix(matrix: np.ndarray) -> List[List[bool]]:
        if len(matrix) == 0:
            return []
        return [[bool(cell) for cell in row] for row in matrix]
    
    try:
        e_int = int(e)
        matrix, pairs = define_matrix(s)
        
        if len(matrix) == 0:
            empty_matrix: List[List[bool]] = []
            return (empty_matrix, empty_matrix, empty_matrix, empty_matrix, empty_matrix)
        
        m_control = build_control_matrix(matrix, pairs.copy(), e_int)
        m_comply = m_control.T
        m_control_indir = control_indirectly_matrix(m_control)
        m_comply_indir = m_control_indir.T
        m_cooperative = comply_cooperative_matrix(m_control)
        return (
            convert_to_bool_matrix(m_control),
            convert_to_bool_matrix(m_comply), 
            convert_to_bool_matrix(m_control_indir),
            convert_to_bool_matrix(m_comply_indir),
            convert_to_bool_matrix(m_cooperative)
        )
        
    except Exception as ex:
        raise ValueError(f"Ошибка выполнения: {ex}")

if __name__ == "__main__":
    #test_input = "1,2\n1,3\n3,4\n3,5\n5,6\n6,7"
    #root_node = "1"

    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Входные данные')
    parser.add_argument('e_r', help='Идентификатор вершины графа')
    args = parser.parse_args()
    
    result = main(args.input, args.e_r)
    print("Матрица управления:")
    print_adjency_matrix(result[0])
    print("Матрица подчинения:")
    print_adjency_matrix(result[1])
    print("Матрица опосредственного управления:")
    print_adjency_matrix(result[2])
    print("Матрица опосредственного подчинения:")
    print_adjency_matrix(result[3])
    print("Матрица соподчинения:")
    print_adjency_matrix(result[4])


    
