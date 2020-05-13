# フレーム分割
def frame_split(video_file):
    import cv2
    from tqdm import tqdm

    cap = cv2.VideoCapture(video_file)

    # 総フレーム数を取得する。
    total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # フレームを格納する配列
    images = []

    i = 0
    tqdm(desc="Splitting Frame")
    for _ in tqdm(range(int(total_frame))):
        flag, frame = cap.read()  # Capture frame-by-frame
        if flag == False:
            break
        images.append(frame)
        i += 1
    cap.release()
    return images
