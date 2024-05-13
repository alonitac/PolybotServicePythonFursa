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

        # Calculate center of the image
        center_x = width // 2
        center_y = height // 2

        # Create a new array to hold the rotated image
        rotated_data = [[0] * height for _ in range(width)]

        # Iterate over each pixel in the original image
        for y in range(height):
            for x in range(width):
                # Calculate new position after rotation
                new_x = center_x + (y - center_y)
                new_y = center_y - (x - center_x)

                # Assign pixel value from original image to new position in rotated image
                rotated_data[new_y][new_x] = self.data[y][x]

        # Update self.data with the rotated image
        self.data = rotated_data

    def salt_n_pepper(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                rand = random.random()
                if rand < 0.2:
                    self.data[i][j] = 255  # Salt
                elif rand > 0.8:
                    self.data[i][j] = 0  # Pepper

    def concat(self, other_img, direction='horizontal'):
        if len(self.data) != len(other_img.data):
            raise RuntimeError("Images have different heights and cannot be concatenated horizontally.")

        self.data = [self_row + other_row for self_row, other_row in zip(self.data, other_img.data)]

        
    def segment(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j] > 100:
                    self.data[i][j] = 255  # White
                else:
                    self.data[i][j] = 0  # Black