def vp(video_file, filename):
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import cv2
    import os
    import glob

    from my_module.frame_split import frame_split

    frame_split(video_file)

    # 画像ファイルを格納，時系列にソート
    files = glob.glob("image_wave２/*.png")
    files.sort()

    # 画像を読み込み，green成分を抽出
    images = [cv2.imread(files[i]) for i in range(len(files))]
    # cv2の画像は["高さ", "幅", "BGR"]で格納されている
    images_green = [pd.DataFrame(images[j][:, :, 1]) for j in range(len(images))]


    # parameter 頬の部分を指定
    in1 = 300
    in2 = 350
    co1 = 1000
    co2 = 1100

    # メディアンフィルタによる平滑化
    images_green_median = [cv2.medianBlur(images_green[i].iloc[in1: in2, co1:co2].values, ksize=5) for i in
                           range(len(images_green))]

    # 平均値を算出
    img_mean = [images_green_median[i].mean() for i in range(len(images_green_median))]

    # サンプリング周波数
    fs = 60

    # 心拍数のグラフを保存する
    end_time = round(len(img_mean) / fs)
    time = np.arange(0, end_time, end_time / len(img_mean))
    plt.plot(time, img_mean)
    plt.xlabel("time(s)", size=15)
    plt.savefig("pulse_graph_url")