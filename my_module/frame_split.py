# フレーム分割
def frame_split(video_file='./image_wave.wmv', image_dir='./image_wave２/',
                image_file='image_wave２-%s.png'):
    import os
    import shutil
    import cv2

    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    i = 0

    cap = cv2.VideoCapture(video_file)
    while (cap.isOpened()):
        flag, frame = cap.read()  # Capture frame-by-frame
        if flag == False:
            break
        cv2.imwrite(image_dir + image_file % str(i).zfill(6), frame)

        #print('Save', image_dir + image_file % str(i).zfill(6))

        i += 1

    cap.release()
