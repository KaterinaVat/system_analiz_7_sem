import csv
import numpy as np
import argparse
from typing import Union, List

class AdjacencyMatrix:
    def __init__(self, file_link: str, input_str: str) -> None:
        self.file_link = file_link
        self.input_str = input_str

    def adjacency_matrix(self) -> Union[List[List[int]], None]:
        if self.file_link != 'None':
            return self._from_file()
        elif self.input_str != 'None':
            return self._from_string()
        return None

    def _from_file(self) -> Union[List[List[int]], None]:
        max_ind = 0
        pairs = []
        try:
            with open(self.file_link, newline='') as csv_file:
                pairreader = csv.reader(csv_file, delimiter=' ')
                for pair in pairreader:
                    if not pair:
                        continue
                    v1, v2 = pair[0].split(',')
                    
                    if int(v1) < 0 or int(v2) < 0:
                        print(f'Ошибка: отрицательный индекс вершины: {v1}, {v2}')
                        print("Индексы вершины должны быть положительными числами")
                        return None
                    pairs.append([int(v1), int(v2)])
                    max_ind = max(max_ind, int(v1), int(v2))

            if max_ind <= 0:
                return []
            
            matrix_sm = [[0] * max_ind for _ in range(max_ind)]  

            for pair in pairs:
                matrix_sm[pair[0]-1][pair[1]-1] = 1
                matrix_sm[pair[1]-1][pair[0]-1] = 1
            return matrix_sm  
                
        except FileNotFoundError:
            print(f"Ошибка: файл {self.file_link} не найден")
            return None
        except ValueError:
            print('Ошибка: нечисловое значение в индексе вершин')
            return None
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    def _from_string(self) -> Union[List[List[int]], None]:
        try:
            s = self.input_str.split('\n') 
            max_ind = 0
            pairs = []
            for pair in s:
                if not pair.strip():
                    continue
                v1, v2 = pair.split(',')
                if int(v1) < 0 or int(v2) < 0:
                    print(f'Ошибка: отрицательный индекс вершины: {v1}, {v2}') 
                    print("Индексы вершины должны быть положительными числами")
                    return None
                pairs.append([int(v1), int(v2)])
                max_ind = max(max_ind, int(v1), int(v2))
            
            if max_ind <= 0:
                return []
            
            matrix = [[0] * max_ind for _ in range(max_ind)]
            
            for pair in pairs:
                matrix[pair[0]-1][pair[1]-1] = 1
                matrix[pair[1]-1][pair[0]-1] = 1
            
            return matrix  
            
        except ValueError:
            print('Ошибка: нечисловое значение в индексе вершин')
            return None

def print_adjency_matrix(matrix: List[List[int]]) -> None:
    if matrix is None:
        print("Матрица не создана")
        return
    if len(matrix) == 0:
        print("Пустая матрица")
        return
        
    print("   ", end="")
    for i in range(1, len(matrix)+1):
        print(f"{i:3}", end=' ')
    print()

    for i, row in enumerate(matrix, 1):
        print(f"{i:2}", end=" ")
        for val in row:
            print(f"{val:3}", end=" ")
        print()

def preprocess_input(inp: str) -> Union[AdjacencyMatrix, None]:
    if '.csv' in inp:
        return AdjacencyMatrix(file_link=inp, input_str='None')
    else:
        return AdjacencyMatrix(file_link='None', input_str=inp)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Входные данные')
    args = parser.parse_args()
    
    try:
        ad = preprocess_input(args.input)
        if ad is None:
            print("Не удалось создать объект матрицы")
            return
            
        matrix_sm = ad.adjacency_matrix()
        print("Матрица смежности:")
        if matrix_sm is not None:
            print_adjency_matrix(matrix_sm)
            
    except Exception as e:
        print(f'Ошибка: {e}')

if __name__ == "__main__":
    main()