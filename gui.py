import json, os, subprocess, chardet
import tkinter as tk
from tkinter import filedialog, Text

class App(tk.Tk):




    def __init__(self):
        super().__init__()
        project_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(project_path, "config.json")
        
        self.title('视频字幕提取')
        self.geometry('500x300')
        
        # 读取配置信息
        with open(config_path, encoding='utf-8') as f:
            self.config = json.load(f)

        # 分辨率标签
        self.res_label = tk.Label(self, text='分辨率')
            
        # 游戏选择
        games = list(self.config.keys())
        self.game_var = tk.StringVar(value=games[0])
        self.game_label = tk.Label(self, text='游戏名称')
        self.game_dropdown = tk.OptionMenu(self, self.game_var, *games)
        
        # 分辨率选择
        first_game = self.game_var.get()
        first_game_config = self.config[first_game]
        resolutions_config = first_game_config.get('resolution', {})
        resolutions = list(resolutions_config.keys())
        self.res_var = tk.StringVar(value=resolutions[0])
        self.res_dropdown = tk.OptionMenu(self, self.res_var, *resolutions)

        # 绑定游戏选择事件
        self.game_var.trace('w', self.update_resolutions) 
        
        # 视频路径
        self.video_label = tk.Label(self, text='视频文件')
        self.video_entry = tk.Entry(self)
        self.video_button = tk.Button(self, text='选择', command=self.select_video)
        
        # 提取按钮
        self.extract_button = tk.Button(self, text='提取字幕', command=self.extract)
        
        # 状态
        self.status = tk.Label(self, text='')
        
        # 布局
        self.game_label.grid(row=0, column=0)
        self.game_dropdown.grid(row=0, column=1)
        
        self.res_label.grid(row=1, column=0)
        self.res_dropdown.grid(row=1, column=1)
        
        self.video_label.grid(row=2, column=0)
        self.video_entry.grid(row=2, column=1)
        self.video_button.grid(row=2, column=2)
        
        self.extract_button.grid(row=3, column=1)

        self.output_text = Text(self, height=10, width=70) 
        self.output_text.config(state=tk.DISABLED)
        self.output_text.grid(row=5, column=0, columnspan=3)

    def update_resolutions(self, *args):
        # 获取当前选择的游戏
        current_game = self.game_var.get()

        # 根据游戏从config中读取分辨率选择
        resolutions_config = self.config[current_game].get('resolution', {})
        resolutions = list(resolutions_config.keys())

        # 更新分辨率选择菜单
        self.res_var.set(resolutions[0]) 
        self.res_dropdown['menu'].delete(0, 'end')

        for resolution in resolutions:
            self.res_dropdown['menu'].add_command(label=resolution, command=tk._setit(self.res_var, resolution))
        
    def select_video(self):
        filename = filedialog.askopenfilename()
        self.video_entry.delete(0, tk.END)
        self.video_entry.insert(0, filename)
        
    def extract(self):
        # 获取选择的游戏、分辨率
        game = self.game_var.get()
        resolution = self.res_var.get()
        video_path = self.video_entry.get()
        
        # 调用main.py时添加参数
        project_path = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(project_path, "main.py")
        p = subprocess.Popen(['python', main_path,  
                        '-i', video_path,
                        '-g', game, 
                        '-r', resolution], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT)
        output = p.communicate()[0]
        encoding = chardet.detect(output)['encoding']
        if encoding:
            output = output.decode(encoding)
        else:
            output = output.decode('utf-8', errors='replace')
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('1.0', output)
        self.output_text.config(state=tk.DISABLED)
        
if __name__ == '__main__':
    app = App()
    app.mainloop()