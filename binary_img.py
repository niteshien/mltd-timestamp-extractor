from PIL import Image, ImageOps
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim
import re


# 二值化指定目录下的所有图片文件
def process_images(input_path, output_path, grey, mode):
    for file_name in os.listdir(input_path):
        if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
            # 打开图片
            file_path = os.path.join(input_path, file_name)
            im = Image.open(file_path)

            # 如果 mode 为 "black_font"，则反色图片
            if mode == "black_glyph":
                im = ImageOps.invert(im)
            elif mode == "white_glyph":
                pass

            # 将图片转换为灰度图像
            im_gray = im.convert('L')

            # 将灰度图像二值化
            im_bw = im_gray.point(lambda x: 0 if x < grey else 255, "1")

            # 保存二值化后的图片
            new_file_name = os.path.splitext(file_name)[0] + '.jpg'
            new_file_path = os.path.join(output_path, new_file_name)
            im_bw.save(new_file_path)


# 输入二值化图片，根据黑白像素比例判断是否为非文字
def is_black_or_white_image(im_bw, white_ratio_threshold=0.3):
    im_gray = im_bw.convert('L')  # 转换为灰度图像
    im_array = np.array(im_gray)  # 将灰度图像转换为 NumPy 数组

    width, height = im_bw.size
    total_pixels = width * height

    white_pixels = np.sum(im_array == 255)  # 计算白色像素的数量
    black_pixels = np.sum(im_array == 0)  # 计算黑色像素的数量

    if black_pixels == total_pixels:
        # print("black")
        return True  # 图像为纯黑
    else:
        white_ratio = white_pixels / total_pixels
        if white_ratio >= white_ratio_threshold:
            # print("white ratio of block " + str(white_ratio))
            return True  # 图像为白块
        else:
            # print("white ratio of text " + str(white_ratio))
            return False  # 图像为文字


def find_similar_image_groups(directory, ssim_threshold=0.8):
    image_groups = []
    group = []
    prev_image = None

    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            image_path = os.path.join(directory, filename)
            with Image.open(image_path) as im:
                im_array = np.array(im)  # 将 PIL.Image 图像转换为 NumPy 数组

                if is_black_or_white_image(im):
                    if group:
                        start = int(re.findall(r'\d+', group[0])[0])
                        end = int(re.findall(r'\d+', group[-1])[0])
                        image_groups.append((start, end))
                        group = []
                    prev_image = None
                    continue  # 如果图像为非文字，跳过不处理

                if prev_image is not None:
                    similarity = ssim(im_array, prev_image)
                    if similarity >= ssim_threshold:
                        group.append(filename)
                    else:
                        if group:
                            start = int(re.findall(r'\d+', group[0])[0])
                            end = int(re.findall(r'\d+', group[-1])[0])
                            image_groups.append((start, end))
                        group = [filename]
                else:
                    group.append(filename)
                prev_image = im_array.copy()

    if group:
        start = int(re.findall(r'\d+', group[0])[0])
        end = int(re.findall(r'\d+', group[-1])[0])
        image_groups.append((start, end))

    return image_groups