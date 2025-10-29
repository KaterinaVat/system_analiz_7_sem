import numpy as np
import argparse

input_str = '1,2/n1,3/n3,4/n2,5'

def define_matrix(input_str):
    try:
        s = input_str.split('/n')
        max_ind = -1
        pairs = []
        for pair in s:
            if not pair:
                continue
            v1, v2 = pair.split(',')
            if int(v1)<0 or int(v2)<0:
                assert(f'Ошика: отрицательный индекс вершины: {v1, v2}')
                assert("Индексы вершины должны быть положительными числами")
                return None
            pairs.append([int(v1), int(v2)])
            max_ind = max(max_ind, int(v1), int(v2))
        if max_ind<=0:
                return np.array([], dtype=int)
        matrix = np.zeros((max_ind, max_ind), dtype = int)
        return matrix, pairs
    except ValueError:
        print('Ошибка: нечисловое значение в индексе вершин')
        return None, None
    

def adjency_matrix(matrix, pairs):
    matrix_sm = matrix.copy()
    for pair in pairs:
        matrix_sm[pair[0]-1][pair[1]-1] = 1
        matrix_sm[pair[1]-1][pair[0]-1] = 1
    return matrix_sm

def control_matrix_step_1(matrix_c,pairs, current_c):
    add_v = []
    proccessed_pairs = []
    for pair in pairs:
        if pair[0]==current_c:
            matrix_c[pair[0]-1][pair[1]-1]=1
            add_v.append(pair[1])
            proccessed_pairs.append(pair)
        elif pair[1]==current_c:
            matrix_c[pair[1]-1][pair[0]-1]=1
            add_v.append(pair[0])
            proccessed_pairs.append(pair)

    for pair in proccessed_pairs:
        pairs.remove(pair)

    return matrix_c, pairs, add_v   
def control_matrix_step_2(matrix_c, pairs, add_v):
    proccessed_pairs = []
    add_n_v = []
    for v in add_v:
        current_c = v  
        for pair in pairs:
            if pair[0]==current_c:
                matrix_c[pair[0]-1][pair[1]-1]=1
                add_n_v.append(pair[1])
                proccessed_pairs.append(pair)
            elif pair[1]==current_c:
                matrix_c[pair[1]-1][pair[0]-1]=1
                add_n_v.append(pair[0])
                proccessed_pairs.append(pair)
    for pair in proccessed_pairs:
        pairs.remove(pair)
    return matrix_c, pairs, add_n_v  
def control_matrix(matrix, pairs, e_r):

    try:
        matrix_c = matrix.copy()
        current_c = e_r
        add_v = []
        matrix_c, pairs, add_v = control_matrix_step_1(matrix_c, pairs, current_c)
        while len(pairs)!=0:
            matrix_c, pairs, add_v = control_matrix_step_2(matrix_c, pairs, add_v)
   
        return matrix_c
    except ValueError:
        print('Ошибка: нечисловое значение в индексе вершин')
        return None           
         
def print_matrix(matrix, ind):
    print(' ')
    if matrix is None:
        print("Матрица пуста")
        return
    if ind == 'adj':
        print("Матрица смежности графа:")
    if ind == 'control':
        print("Матрица отношения - управления")
    if ind == 'comply':
        print("Матрица отношения - подчинения")
    if ind == 'control indirectly':
        print("Матрица отношения - опосредственного упраления")
    if ind == 'comply indirectly':
        print("Матрица отношения - опосредственного подчинения")
    if ind == 'cooperative':
        print("Матрица отношения - соподчинения")
    print("   ", end="")
    for i in range(1, len(matrix)+1):
        print(f"{i:3}", end=' ')
    print()

    for i, row in enumerate(matrix, 1):
        print(f"{i:2}", end = " ")
        for val in row:
            print(f"{val:3}", end = " ")
        print()

def control_indirectly_matrix(control_matrix):
    if control_matrix is None:
        assert("Матрица управления пуста")
        return None
    n = len(control_matrix)
    indir_matrix = np.zeros((n,n), dtype = int)
    for i in range(n):
        for j in range(n):
            if control_matrix[i,j]==1:
                for k in range(n):
                    if control_matrix[i,k]==1:
                        indir_matrix[i,k]=1
    return indir_matrix

def comply_cooperative_matrix(control_matrix):
    if control_matrix is None:
        assert("Матрица управления пуста")
        return None
    n = len(control_matrix)
    comply_coop_matrix = np.zeros((n,n), dtype = int)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if control_matrix[i,j]==1 and control_matrix[i,k]==1 and j!=k:
                    comply_coop_matrix[j,k]=1
                    comply_coop_matrix[k,j]=1
    return comply_coop_matrix

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_str', help='Путь к CSV файлу')
    parser.add_argument('e_r', help='Идентификатор вершины графа')
    args = parser.parse_args()
    matrix, pairs = define_matrix(args.input_str)
    m = adjency_matrix(matrix, pairs)
    print_matrix(m, 'adj')

    m_c = control_matrix(matrix, pairs, e_r = 3)
    print_matrix(m_c, 'control')

    m_comply = m_c.T
    print_matrix(m_comply, 'comply')

    m_indir = control_indirectly_matrix(m_c)
    print_matrix(m_indir, 'control indirectly')

    m_comply_indir = m_indir.T
    print_matrix(m_comply_indir, 'comply indirectly')

    m_coop_comply = comply_cooperative_matrix(m_c)
    print_matrix(m_coop_comply, 'cooperative')


if __name__ == "__main__":
    main()