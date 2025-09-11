import unittest
from task import adjacency_matrix
import numpy as np


class TestMatrix(unittest.TestCase):
    def setUp(self):
        pass

    def test_okey_matrix(self):
        '''
        Проверка с матрицей 0 1 1
                            1 0 0
                            1 0 0
        '''
        okay_matrix = np.array([[0, 1, 1], 
                                  [1, 0, 0], 
                                  [1, 0, 0]])
        matrix = adjacency_matrix(csv_link= "input3.csv")
        self.assertIsNotNone(matrix, "Матрица не должна быть None")
        print("Матрица смежности непуста")
        self.assertIsInstance(matrix, np.ndarray, "Матрица типа numpy array")
        self.assertEqual(matrix.shape, (3,3), "Размерность матрицы 3 на 3")
        print("Матрица имеет верную размерность")
        np.testing.assert_array_equal(matrix, okay_matrix)
        print("Матрица имеет верные элементы")
        

    def test_unknown_file(self):
        print("Прочитаем неизвестный файл")
        unknown_matrix = adjacency_matrix(csv_link="unknown.csv")
        self.assertIsNone(unknown_matrix)

    def test_empty_file(self):
        print("Прочитаем пустой файл")
        unknown_matrix = adjacency_matrix(csv_link="unknown.csv")
        self.assertIsNone(unknown_matrix)

    def test_negative_ind(self):
        print("Считывание отрицательных значений индексов")
        negative_ind_matrix= adjacency_matrix('input5.csv')
        self.assertIsNone(negative_ind_matrix)

if __name__ == '__main__':
    unittest.main()