def vp(img_set):
    import numpy as np
    import pandas as pd
    import cv2

    from my_module.frame_split import frame_split
    from my_module.signal_fft import signal_fft


    images = frame_split(img_set)

    # imagesからG成分を抽出する
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

    # 15sの窓でパワースペクトル算出
    time_interval = 15
    loop_len = list(range(round(len(img_mean) / (fs * time_interval))))
    fft_result = []
    for n, i in enumerate(loop_len):
        if n == 0:
            img = img_mean[:time_interval * fs]
            fft_result.append(signal_fft(img, fs))
        else:
            img = img_mean[time_interval * fs * n: time_interval * fs * (n + 1)]
            fft_result.append(signal_fft(img, fs))

    # 周波数フィルタリング（0.7-2.5Hzの値のみ抽出）
    data = []
    for j in range(len(fft_result)):
        fft_data = [fft_result[j][0][n] for n, i in enumerate(fft_result[j][1]) if 0.7 < i < 2.5]
        data.append(fft_data)
    try:
        frequ = [i for n, i in enumerate(fft_result[0][1]) if 0.7 < i < 2.5]
    except IndexError:
        message = "この動画では心拍数を計測できませんでした。"
        return message

    data = np.array(data)
    # ピークのindexを取得
    peak_index = [np.array(data[i]).argmax() for i in range(len(data))]

    # 取得したindexから該当の周波数を取得し心拍数に変換
    heart_rate = [round(frequ[i] * fs) for i in peak_index]

    return np.mean(heart_rate)