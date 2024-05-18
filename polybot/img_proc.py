import random
from pathlib import Path
from matplotlib.image import imread, imsave


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

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
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self):
        height = len(self.data)
        width = len(self.data[0])

        # Transpose the image (swap rows with columns)
        transposed_data = [[self.data[j][i] for j in range(height)] for i in range(width)]

        # Reverse the rows to complete the rotation
        for i in range(width):
            transposed_data[i] = transposed_data[i][::-1]

        # Update the image data with the rotated data
        self.data = transposed_data


    def salt_n_pepper(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                rand = random.random()
                if rand < 0.2:
                    self.data[i][j] = 255  # Salt
                elif rand > 0.8:
                    self.data[i][j] = 0  # Pepper

    def concat(self, other_img, direction='horizontal'):
        if direction == 'horizontal':
            if len(self.data) != len(other_img.data):
                raise RuntimeError("Images have different heights and cannot be concatenated horizontally.")
            self.data = [self_row + other_row for self_row, other_row in zip(self.data, other_img.data)]
        elif direction == 'vertical':
            if len(self.data[0]) != len(other_img.data[0]):
                raise RuntimeError("Images have different widths and cannot be concatenated vertically.")
            self.data += other_img.data
        else:
            raise ValueError("Invalid direction. Direction must be 'horizontal' or 'vertical'.")

    def segment(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j] > 100:
                    self.data[i][j] = 255  # White
                else:
                    self.data[i][j] = 0  # Black


my_img = Img('/home/abdallah/Pictures/Screenshots/img1.png')
another_img = Img('/home/abdallah/Pictures/Screenshots/img2.png')
my_img.concat(another_img , 'horizontal')
my_img.save_img()   # concatenated image was saved in 'path/to/image_filtered.jpg'