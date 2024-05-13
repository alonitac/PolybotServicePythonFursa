from pathlib import Path
from matplotlib.image import imread, imsave
import random


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        try:
            self.path = Path(path)
        except ValueError as e:
            print('PATH not found')
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        try:
            new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
            imsave(new_path, self.data, cmap='gray')
            return new_path
        except ValueError as e:
            print('save image failed')

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j - 1] - row[j]))

            self.data[i] = res

    def rotate(self):
        N = len(self.data[0])
        for i in range(N // 2):
            for j in range(i, N - i - 1):
                temp = self.data[i][j]
                self.data[i][j] = self.data[N - 1 - j][i]
                self.data[N - 1 - j][i] = self.data[N - 1 - i][N - 1 - j]
                self.data[N - 1 - i][N - 1 - j] = self.data[j][N - 1 - i]
                self.data[j][N - 1 - i] = temp

    def salt_n_pepper(self):
        N= len(self.data)
        for i in range (N):
            for j in range (len(self.data[0])):
                random_float = random.random()
                if random_float < 0.2:
                    self.data[i][j] = 255
                if random_float > 0.8:
                    self.data[i][j] = 0

    def concat(self, other_img, direction='horizontal'):
        if len(self.data[0]) != len(other_img.data[0]) or len(self.data) != len(other_img.data):
            raise RuntimeError()
        for i in range(len(other_img.data)):
            for j in range(len(other_img.data[i])):
                self.data[i].append(other_img.data[i][j])

    def segment(self):
        N = len(self.data)
        for i in range(N):
            for j in range(len(self.data[0])):
                if self.data[i][j] > 100:
                    self.data[i][j] = 255
                else:
                    self.data[i][j] = 0
