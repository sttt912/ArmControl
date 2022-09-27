import sys
import cv2

window_title = "ArmCamera"

def show_camera(ids):
    video_capture = cv2.VideoCapture(ids, cv2.CAP_V4L2)

    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(
                window_title, cv2.WINDOW_AUTOSIZE )
            # Window
            while True:
                ret_val, frame = video_capture.read()

                if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                    cv2.imshow(window_title, frame)
                else:
                    break
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break

        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Not open camera")


if __name__ == "__main__":
    while True:
        print("Enter cammera id:")
        camera_id = int(input())
        if camera_id>=0 and camera_id<=5:
            show_camera(camera_id)
        else:
            print("Invalid camera index")