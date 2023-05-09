import subprocess


# 合成ffmpeg命令，每隔n帧截取一次
def get_extraction_command(input_file, width, height, x_start, y_start, interval, output_path):
    command = 'ffmpeg -i ' + str(input_file) + ' -vf "crop=' + \
        str(width) + ':' + str(height)  + ':' + str(x_start)  + ':' + str(y_start) + \
        ",select='not(mod(n\," + str(interval) + '))\'" -vsync vfr -start_number 1 -q:v 2 ' + \
        str(output_path) + '\\' + '%08d' + '.jpg'
    return command


# 将按顺序命名的图片，转化为时间戳
def convert_real_frame(step, intervals):
    real_frames = []
    for i, interval in enumerate(intervals):
        frame_strat, frame_end = interval
        if(frame_strat != 1):
            frame_strat = frame_strat * step
        else:
            frame_strat = 1
        frame_end = frame_end * step
        f = (int(frame_strat), int(frame_end))
        real_frames.append(f)
    return real_frames


def convert_to_hms_int(num):
    num = num/1000
    hours = int(num // 3600)
    num %= 3600
    minutes = int(num // 60)
    num %= 60
    seconds = int(num)
    milliseconds = int((num - seconds) * 1000)
    return hours * 10000000 + minutes * 100000 + seconds * 1000 + milliseconds


def convert_to_millisecond(input_file, real_frames):
    command = f"ffprobe -v error -select_streams v:0 -show_entries packet=pts_time,duration_time -of csv=print_section=0 {input_file}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf-8')

    all_seconds = []
    while True:
        line = process.stdout.readline().strip()
        if not line:
            break
        second, duration = line.split(',')
        all_seconds.append(second)

    milliseconds = []
    for frame_start, frame_end in real_frames:
        if frame_start - 1 < len(all_seconds) and frame_end - 1 < len(all_seconds):
            start_millisecond = int(float(all_seconds[frame_start - 1]) * 1000)
            end_millisecond = int(float(all_seconds[frame_end - 1]) * 1000)
            milliseconds.append((start_millisecond, end_millisecond))
        else:
            print(f"无法获取时间戳：({frame_start}, {frame_end})")
    return milliseconds


def convert_time_stamp(milliseconds):
    time_stamp = []
    for start_time, end_time in milliseconds:
        start_time = convert_to_hms_int(start_time)
        end_time = convert_to_hms_int(end_time)
        time_stamp.append((start_time, end_time))
    return time_stamp
        