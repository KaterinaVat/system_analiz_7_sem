import csv
import numpy as np
import argparse


def adjacency_matrix(csv_link):
    max_ind = 0
    pairs = []
    try:
        with open(csv_link, newline = '') as csv_file:
            pairreader = csv.reader(csv_file, delimiter = ' ')
            for pair in pairreader:
                if not pair:
                    continue
                ind0, ind1 = pair[0].split(',')
                
                if int(ind0)<0 or int(ind1)<0:
                    print(f'Ошика: отрицательный индекс вершины: {ind0, ind1}')
                    print("Индексы вершины должны быть положительными числами")
                    return None
                pairs.append([int(ind0), int(ind1)])
                max_ind = max(max_ind, int(ind0), int(ind1))

            if max_ind<=0:
                return np.array([], dtype=int)
            matrix_sm = np.zeros((max_ind, max_ind), dtype = int)

            for pair in pairs:
                matrix_sm[pair[0]-1][pair[1]-1] = 1
                matrix_sm[pair[1]-1][pair[0]-1] = 1
            return matrix_sm
    except FileNotFoundError:
        print(f"Ошибка: файл {csv_link} не найден")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None
    except ValueError:
        print('Ошибка: нечисловое значение в индексе вершин')
        return None
    
def print_adjency_matrix(matrix):
    if matrix is None:
        print("Матрица не создана")
        return
    print("Матрица смеждности графа:")
    print("   ", end="")
    for i in range(1, len(matrix)+1):
        print(f"{i:3}", end=' ')
    print()

    for i, row in enumerate(matrix, 1):
        print(f"{i:2}", end = " ")
        for val in row:
            print(f"{val:3}", end = " ")
        print()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='Путь к CSV файлу')
    args = parser.parse_args()

    matrix_sm = adjacency_matrix(args.file_path)
    if matrix_sm is not None:
        print_adjency_matrix(matrix_sm)

if __name__ == "__main__":
    main()