import cv2
import os

def create_frames(path, resolution):
    video_name = os.path.splitext(os.path.basename(path))[0]
    frames_dir = f"./frames/{video_name+str(resolution)}/"
    
    # tries to create new dir in frames dir
    try:
        os.mkdir(frames_dir)
    except:
        pass

    video = cv2.VideoCapture(path)
    frame = 1
    ret = True

    while ret:
        ret, image = video.read()

        # quits frame gen if cv cannot retrieve image
        if not ret:
            break

        # creates frame based on given resolution
        xRes, yRes = resizeEq(image, resolution)
        image = cv2.resize(image, dsize=(xRes,yRes))
        frame_path = frames_dir + f"frame{frame}.jpg"
        cv2.imwrite(frame_path, image)

        print(f'Generated frame: {frame}', end="\r", flush=True)
        frame += 1

    return frames_dir

# returns resized values of x and y based on given resolution
def resizeEq(image, maxDim):
    x = image.shape[1]
    y = image.shape[0]
    if y >= x:
        x = int((x/y) * maxDim)
        y = maxDim
    else:
        y = int((y/x) * maxDim)
        x = maxDim
    return (x,y)