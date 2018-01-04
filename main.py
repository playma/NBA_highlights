import json

import cv2

from utils import detect, scoreboard

video_path = "/home/playma/4t/Public/2017_MMAI_Final_Project/NBA.2017.12.16.UTA@CLE.720p.mp4"
bbox_path = "./source/bbox_v2.json"
number_template_path = "./source/23.jpg"
output_path = "./output/data.json"

def main():
    # Setting
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Input
    bbox_data = json.load(open(bbox_path))
    number_template = cv2.imread(number_template_path, 0)

    # Output file
    output_file = open(output_path, 'w')

    prev_score = 0
    frame_idx = 0
    #frame_idx = 14026.260187814032 #start time
    step = 1*fps 
    
    obj_list = []  
    while(cap.isOpened()):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()

        if ret==True:
            msec = cap.get(cv2.CAP_PROP_POS_MSEC)
            sec = msec/1000
            print(sec)

            obj = {}
            obj['time'] = sec
            obj['data'] = []

            # Scoreboard
            score, score_change = scoreboard.get_info(frame, prev_score)
            obj['score'] = score
            obj['score_change'] = score_change
            prev_score = score
            
            # Detect player
            detected, detected_pos = detect.detect_by_number(frame, bbox_data, sec, number_template)
            detect_by_number = {}
            detect_by_number['type'] = "detect_by_number"
            detect_by_number['detected'] = detected
            detect_by_number['position'] = detected_pos

            obj['data'].append(detect_by_number)

            obj_list.append(obj)
            frame_idx += step
            #if sec > 600: break
        else:
            break

    json_str = json.dumps(obj_list, sort_keys=True, indent=4)
    output_file.write(json_str)

    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
