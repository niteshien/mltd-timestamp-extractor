# MLTD时间轴提取器
本项目旨在从 **偶像大师百万现场剧场时光（アイドルマスター ミリオンライブ! シアターデイズ）** 的游戏视频中提取时间轴，以便借助其他工具生成 SRT 字幕文件。同时，该项目还提供了用于提取**偶像大师闪耀色彩（アイドルマスター シャイニーカラーズ）** 和 **东京七姐妹（Tokyo 7th Sisters）** 游戏的相关参数。

您可以根据需要自行修改或添加参数，以满足更多游戏的字幕提取需求。

## 预编译版本

对于不需要自行编译的用户,可以直接在[Releases](https://github.com/niteshien/mltd-timestamp-extractor/releases)页面下载打包好的可执行文件，无需安装任何依赖，即可直接使用。

## 配置参数

需要修改游戏名称、分辨率等参数的用户,请打开`config.json`文件，根据`config_description.txt`的说明配置参数。

## 开发说明

如果您需要自行编译或修改源代码，请遵循以下步骤:

1. 安装Python依赖
```
pip install -r requirements.txt
```

2. 安装 [FFmpeg](https://www.ffmpeg.org/)，并将安装路径添加到环境变量中。

3. 启动图形界面
```
python gui.py
```

4. 运行结束后，会在视频文件所在的路径生成仅包含时间轴信息的同名SRT字幕文件。

## (可选)OCR提取原字幕

1. 下载并安装 [硬字幕提取工具10.0](https://zhuanlan.zhihu.com/p/559874793)。

2. 备份软件目录下的 `config.ini` 和 `log.txt` 文件。如果软件卡死没有其他解决方法，可以尝试覆盖这两个文件。

3. 双击运行软件。此时软件窗口左上角标题栏应显示“視頻截圖、刪合窗”。

4. 按照“**硬字幕提取工具10.0 用户使用手册.docx**”中的指引，申请 OCR 的 API 并配置给软件。建议勾选“識別為單行”和“極速曡圖”。

5. 点击左上的 "Browse" 按钮，选择本项目所在目录下的 ``./img/text_raw``。软件会自动加载图片，并读取时间轴信息。（必须选择未经处理的 `text_raw`，选择 `text_bw` 可能会导致软件崩溃）

   如果软件未能成功获取时间轴信息，可以在“系統設置”中打开“生成.TXT”选项，稍后手动与字幕文件合并。

6. 按照手册指引，完成 OCR。您可以在 `./img/text_raw` 目录下找到 `123.srt` 文件（和相应的 txt 文件）。

## 支持与问题反馈

遇到问题欢迎在[Issues 页面](https://github.com/niteshien/mltd-timestamp-extractor/issues) 提交反馈。也可以通过以下联系方式与我取得联系。


## 联系信息

- 微博: [@米拉博雷亞斯](https://weibo.com/u/7733258030)
- 哔哩哔哩: [@Nitebaka](https://space.bilibili.com/5584028)
- 邮箱: niteshien@outlook.com

## 许可证

本项目采用 [MIT 许可证](LICENSE)。
