import subprocess, os, shutil, json, sys
from extract_pics import get_extraction_command, convert_time_stamp, convert_real_frame, convert_to_millisecond
from binary_img import process_images, find_similar_image_groups
from timestamp import create_srt_data, write_srt
from get_text import run_multiprocess_extract_text, rearrange_image_timestamp, filename_to_srt


def main():
    '''必须设置的参数'''
    # 输入视频路径。建议视频长度在20分钟以下。
    input_file = "D:/videos/recording/MLTD/part2.mp4" # 运行结束后，会在视频目录创建同名的.srt文件。

    # 目前支持的 游戏/分辨率 参数请见config.json文件。若没有对应的参数，请自行定位并填写。
    game = "MLTD"
    resolution = "2400*1080"

    # 是否跳过时轴图片截取
    is_extraction_done = False  # 默认False，调试用，首次运行必须为False。若针对同一段视频反复运行，可改为True跳过部分步骤以节省时间。






    '''无需改动'''
    #其他参数
    project_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_path, "img", "raw")
    bw_path = os.path.join(project_path, "img", "bw")
    srt_name, _ = os.path.splitext(os.path.basename(input_file))
    input_dir = os.path.dirname(input_file)
    text_raw_dir = os.path.join(project_path, "img", "text_raw")
    text_bw_dir = os.path.join(project_path, "img", "text_bw")
    config_path = os.path.join(project_path, "config.json")
    
    try:
        with open(config_path, "r", encoding='utf-8') as f:
            config = json.load(f)
        if game not in config:
            raise KeyError(f"config.json中不存在'{game}'这一游戏，请打开config.json添加相关参数。")
        elif resolution not in config[game]:
            raise KeyError(f"config.json中不存在'{game}'在'{resolution}'分辨率下的参数，请打开config.json添加相关参数。")
        params = config[game][resolution]
        width = params["width"]
        height = params["height"]
        x_start = params["x_start"]
        y_start = params["y_start"]
        interval = config[game]["interval"]
        text_width = params["text_width"]
        text_height = params["text_height"]
        grey = config[game]["grey"]
        mode = config[game]["mode"]

    except KeyError as e:
        print(str(e))
        sys.exit(1)


    if not is_extraction_done:
        if os.path.exists(bw_path):
            shutil.rmtree(bw_path)
        os.makedirs(bw_path)
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        os.makedirs(output_path)
        if os.path.exists(text_raw_dir):
            shutil.rmtree(text_raw_dir)
        
        os.makedirs(text_raw_dir)
        if os.path.exists(text_bw_dir):
            shutil.rmtree(text_bw_dir)
        os.makedirs(text_bw_dir)
        
        command = get_extraction_command(input_file, width, height, x_start, y_start, interval, output_path)
        subprocess.run(command)
        print("时轴图片截取完成")
        process_images(output_path, bw_path, grey, mode)
        print("二值化完成")

    continue_time = find_similar_image_groups(bw_path)
    print("连续图像识别完毕")
    real_frames = convert_real_frame(interval, continue_time)
    milliseconds = convert_to_millisecond(input_file, real_frames)
    time_stp = convert_time_stamp(milliseconds)
    print("时间戳转换完成")

    run_multiprocess_extract_text(input_file, text_raw_dir, milliseconds, time_stp, x_start, y_start, text_width, text_height, end_arrange=500)
    process_images(text_raw_dir, text_bw_dir, grey, mode)
    print("文本图片截取完成")

    rearrange_image_timestamp(text_bw_dir, text_raw_dir)
    filename_intervals = filename_to_srt(text_raw_dir)
    srt_data = create_srt_data(filename_intervals)
    write_srt(input_dir, srt_name, srt_data)
    print("SRT时间轴写入完成")

    print("All done!")
    print("Your subtitle file is " + str(input_dir) + "/" + str(srt_name) + ".srt")



if __name__ == '__main__':
    main()


'''
实际上，截取时轴图片和二值化这两个步骤，没必要将图片保存到硬盘中
一段半小时的60fps视频，以6帧间隔截取首字，最后加起来产生的图片不过40万张
将这些数据全部放到内存里，占用也不会超过200MiB
但我懒得优化了，所以就这样吧
'''