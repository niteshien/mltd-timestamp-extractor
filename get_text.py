import cv2
import os
from multiprocessing import Pool
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim



def rearrange_image_timestamp(binary_folder: str, original_folder: str, similarity_threshold: float = 0.8):
    binary_filenames = sorted([f for f in os.listdir(binary_folder) if (f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png'))])
    prev_binary_image = None
    prev_binary_image_path = None

    for idx, binary_filename in enumerate(binary_filenames):
        binary_image_path = os.path.join(binary_folder, binary_filename)
        
        with Image.open(binary_image_path) as im:
            binary_im_array = np.array(im)  # 将 PIL.Image 图像转换为 NumPy 数组
            
            if prev_binary_image is not None:
                similarity = ssim(binary_im_array, prev_binary_image)

                if similarity >= similarity_threshold:
                    # 获取前一张二值化图片文件名的开始时间戳
                    start_timestamp = prev_binary_image_path[-len(binary_filename):-len(binary_filename)+12]

                    # 删除前一张二值化图片和对应的原图
                    original_image_path = os.path.join(original_folder, os.path.basename(prev_binary_image_path))
                    os.remove(prev_binary_image_path)
                    os.remove(original_image_path)

                    # 重命名后一张二值化图片和对应的原图，使用前一张图片的开始时间戳
                    new_binary_filename = start_timestamp + binary_filename[12:]
                    new_binary_image_path = os.path.join(binary_folder, new_binary_filename)
                    os.rename(binary_image_path, new_binary_image_path)
                    binary_image_path = new_binary_image_path

                    original_image_path = os.path.join(original_folder, binary_filename)
                    new_original_image_path = os.path.join(original_folder, new_binary_filename)
                    os.rename(original_image_path, new_original_image_path)

            prev_binary_image = binary_im_array.copy()
            prev_binary_image_path = binary_image_path


def get_text_stamp(time_stamp):
    start_stamp, end_stamp = time_stamp

    formatted_numbers = []
    for number in (start_stamp, end_stamp):
        number_str = f'{number:08d}'
        number_with_underscores = f'{number_str[0]}_{number_str[1:3]}_{number_str[3:5]}_{number_str[5:]}'
        formatted_numbers.append(number_with_underscores)

    name = f'{formatted_numbers[0]}__{formatted_numbers[1]}'
    return name


def extract_text(args):
    video_path, output_dir, milliseconds, time_stamps, x_start, y_start, text_width, text_height, end_arrange, idx = args
    video = cv2.VideoCapture(video_path)

    start, end = milliseconds[idx]
    end = end - end_arrange
    video.set(cv2.CAP_PROP_POS_MSEC, end)  # 设置视频的播放位置
    success, frame = video.read()

    if success:
        cropped_frame = frame[y_start:y_start+text_height, x_start:x_start+text_width]
        name = get_text_stamp(time_stamps[idx])
        output_path = f"{output_dir}/{name}_{end_arrange}.jpg"
        cv2.imwrite(output_path, cropped_frame)

    video.release()


# 多线程截取文本图像，实际上并没有快太多。
def run_multiprocess_extract_text(video_path, output_dir, milliseconds, time_stamps, x_start, y_start, text_width, text_height, end_arrange=500):
    # end_arrange 参数用于调整截图提前量，默认提前500ms截取
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    num_processes = 8  # 进程数，建议与CPU核心数量相匹配
    with Pool(num_processes) as pool:
        pool.map(extract_text, [(video_path, output_dir, milliseconds, time_stamps, x_start, y_start, text_width, text_height, end_arrange, idx) for idx in range(len(milliseconds))])


def are_images_similar(image_path1: str, image_path2: str, similarity_threshold: float = 0.8) -> bool:
    with Image.open(image_path1) as im1, Image.open(image_path2) as im2:
        im_array1 = np.array(im1)
        im_array2 = np.array(im2)

    similarity = ssim(im_array1, im_array2)
    if similarity >= similarity_threshold:
        print("两张图片相似度超过阈值，原函数中它们会触发重命名。")
    else:
        print("两张图片相似度未超过阈值。")
    print(f"图片相似度为 {similarity:.3f}")
    return similarity >= similarity_threshold



def filename_to_srt(input_path: str):
    # 获取输入路径下的所有图片文件名
    image_filenames = [f for f in os.listdir(input_path) if (f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png'))]
    
    result = []
    
    for image_filename in image_filenames:
        # 去掉下划线
        no_underscore_name = image_filename.replace('_', '')

        # 去掉后缀名和最后四位字符
        stripped_name = no_underscore_name[:16]
        
        
        
        # 将字符串从中间分成两半
        half_len = len(stripped_name) // 2
        start_stp_str = stripped_name[:half_len]
        end_stp_str = stripped_name[half_len:]
        
        # 将两半转换成整数
        start_stp = int(start_stp_str)
        end_stp = int(end_stp_str)
        
        # 将整数合并到一个元组里，并添加到结果列表中
        result.append((start_stp, end_stp))
    
    return result


'''
# 单线程截取文本图像，速度较慢，每秒2~3张图片。
def extract_text_singleprocess(video_path, output_dir, milliseconds, x_start, y_start, text_width, text_height):
    video = cv2.VideoCapture(video_path)
    for idx, (start, end) in enumerate(milliseconds):
        video.set(cv2.CAP_PROP_POS_MSEC, end)  # 设置视频的播放位置
        success, frame = video.read()

        if success:
            cropped_frame = frame[y_start:y_start+text_height, x_start:x_start+text_width]
            output_path = f"{output_dir}/output_frame_{idx}.jpg"
            cv2.imwrite(output_path, cropped_frame)

    video.release()
'''