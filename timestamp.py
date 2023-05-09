# 转换为整数
def convert_timestamps(timestamps):
    timestamps = [filename.replace('.jpg', '') for filename in timestamps] # 去掉后缀名，仅保留时间戳
    timestamps = [int(item) for item in timestamps]
    return timestamps


def format_timecode(timestamp):
    """
    将时间戳格式化为srt格式的时间码
    """
    # 在左边添加若干0，变成长度为9的字符串
    timestamp_str = str(timestamp).zfill(9)
    # 变成00:00:03,480
    timestamp_str = timestamp_str[:2] + ":" + timestamp_str[2:4] + ":" + timestamp_str[4:6] + "," + timestamp_str[6:]
    return timestamp_str


# 读取文件名以得到新的srt信息
def filename_process(input_path):
    intervals = []
    return intervals


def create_srt_data(intervals):
    """
    根据时间戳区间创建srt格式的字幕数据
    """
    srt_data = ""
    for i, interval in enumerate(intervals):
        start_time, end_time = interval
        # 将时间戳格式化为srt格式的时间码
        start_time = format_timecode(start_time)
        end_time = format_timecode(end_time)
        # 变成00:00:03,480 --> 00:00:04,520
        timecode = str(start_time) + " --> " + str(end_time)
        # 添加字幕序号和时间码
        srt_data += f"{i+1}\n{timecode}\n\n"
    return srt_data


def write_srt(path, srt_name, srt_data):
    """
    将srt格式的字幕数据写入文件
    """
    with open(f"{path}/{srt_name}.srt", "w", encoding="utf-8") as f:
        f.write(srt_data)