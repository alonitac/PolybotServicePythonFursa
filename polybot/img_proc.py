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
        new_arr = []
        for c in range(len(self.data[0])):
            new_col = []
            # make new row from the columns
            for r in range(len(self.data) - 1, -1, -1):
                new_col.append(self.data[r][c])
            new_arr.append(new_col)
        self.data = new_arr

    def salt_n_pepper(self):
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                # take a random floating number between 0 and 1 (inclusive)
                choice = random.randint(0, 100) / 100
                # give the maximum intensity to the current pixel
                if choice < 0.2:
                    self.data[r][c] = 255
                # give the minimum intensity to the current pixel
                elif choice > 0.8:
                    self.data[r][c] = 0

    def concat(self, other_img, direction='horizontal'):
        # checking if heights are equal
        if len(self.data) != len(other_img.data):
            raise RuntimeError("ERROR: height of given image not as the current image")

        # checking if widths are equal
        # assuming the image is rectangular or square shape
        if len(self.data[0]) != len(other_img.data[0]):
            raise RuntimeError("ERROR: the width of the given image not as the current image")
        # for r in range(len(self.data)):
        #     if len(self.data[r]) != len(other_img.data):
        #         pass

        # if the direction is horizontal then we want to connect each row
        # for the other image to each row in the current image's
        # corresponding row
        if direction == 'horizontal':
            for i, row in enumerate(self.data):
                row += other_img.data[i]
        # if the direction is vertical then we want to connect all the
        # other image at the end of the current image
        elif direction == 'vertical':
            for row in other_img.data:
                self.data.append(row)

    def segment(self):
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                # give 255 to pixels greater than 100, 0 otherwise
                if self.data[r][c] > 100:
                    self.data[r][c] = 255
                else:
                    self.data[r][c] = 0

