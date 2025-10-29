import unittest
import os
from task import AdjacencyMatrix

class TestMatrix(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые файлы
        self.create_test_files()
    
    def tearDown(self):
        # Удаляем тестовые файлы после тестов
        self.remove_test_files()
    
    def create_test_files(self):
        # Создаем файл input3.csv
        with open("input3.csv", "w") as f:
            f.write("1,2\n1,3\n")
        
        # Создаем пустой файл
        with open("empty.csv", "w") as f:
            pass
        
        # Создаем файл с отрицательными индексами
        with open("input5.csv", "w") as f:
            f.write("1,-2\n")
    
    def remove_test_files(self):
        files = ["input3.csv", "empty.csv", "input5.csv"]
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def test_okey_matrix(self):
        '''
        Проверка с матрицей 0 1 1
                            1 0 0
                            1 0 0
        '''
        okay_matrix = [[0, 1, 1], 
                       [1, 0, 0], 
                       [1, 0, 0]]
        
        # Создаем объект класса AdjacencyMatrix
        adj_obj = AdjacencyMatrix(file_link="input3.csv", input_str='None')
        matrix = adj_obj.adjacency_matrix()
        
        self.assertIsNotNone(matrix, "Матрица не должна быть None")
        print("Матрица смежности непуста")
        self.assertIsInstance(matrix, list, "Матрица должна быть списком")
        self.assertEqual(len(matrix), 3, "Размерность матрицы 3 на 3")
        print("Матрица имеет верную размерность")
        self.assertEqual(matrix, okay_matrix)
        print("Матрица имеет верные элементы")
        
    def test_unknown_file(self):
        print("Прочитаем неизвестный файл")
        adj_obj = AdjacencyMatrix(file_link="unknown.csv", input_str='None')
        unknown_matrix = adj_obj.adjacency_matrix()
        self.assertIsNone(unknown_matrix)

    def test_empty_file(self):
        print("Прочитаем пустой файл")
        adj_obj = AdjacencyMatrix(file_link="empty.csv", input_str='None')
        empty_matrix = adj_obj.adjacency_matrix()
        self.assertEqual(empty_matrix, [])

    def test_negative_ind(self):
        print("Считывание отрицательных значений индексов")
        adj_obj = AdjacencyMatrix(file_link='input5.csv', input_str='None')
        negative_ind_matrix = adj_obj.adjacency_matrix()
        self.assertIsNone(negative_ind_matrix)

    def test_string_input(self):
        '''Тест ввода строкой'''
        print("Тест ввода строкой")
        input_string = "1,2\n1,3\n2,3"
        expected_matrix = [[0, 1, 1],
                          [1, 0, 1],
                          [1, 1, 0]]
        
        adj_obj = AdjacencyMatrix(file_link='None', input_str=input_string)
        matrix = adj_obj.adjacency_matrix()
        
        self.assertIsNotNone(matrix, "Матрица не должна быть None")
        self.assertEqual(matrix, expected_matrix)

if __name__ == '__main__':
    unittest.main()