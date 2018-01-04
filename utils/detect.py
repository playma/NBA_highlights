import cv2


def search_json(obj_list, key, value):
    data = None
    for obj in obj_list:
        if obj[key] == value:
            data = obj
            break
    return data

def sift(query, train):
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(query,None)
    kp2, des2 = sift.detectAndCompute(train,None)
    # BFMatcher with default params
    bf = cv2.BFMatcher()

    if type(des1) != type(des2):
        return []

    matches = bf.knnMatch(des1,des2, k=2)
    # Apply ratio test
    good = []
    if len(matches[0]) != 2:
        return []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
    return good

def detect_by_number(frame, bbox_data, sec, number_template):
    b_data = search_json(bbox_data, 'time', str(sec))
    person_data = search_json(b_data['data'], 'type', 'person')

    detected = False
    detected_pos = []
    for (p_id, pos) in enumerate(person_data['positions']):
        #cv2.rectangle(frame, (pos['x1'], pos['y1']),(pos['x2'], int((pos['y1']+pos['y2'])/2)),(0,255,0),3)
        upperbody = frame[pos['y1']:int((pos['y1']+pos['y2'])/2), pos['x1']:pos['x2']]
        upperbody_gray = cv2.cvtColor(upperbody, cv2.COLOR_BGR2GRAY)
        ret,upperbody_binary = cv2.threshold(upperbody_gray, 127,255,cv2.THRESH_BINARY)

        good = sift(number_template, upperbody_binary)

        if len(good) >= 7:
            cv2.rectangle(frame, (pos['x1'], pos['y1']),(pos['x2'], int((pos['y1']+pos['y2'])/2)),(255,0,0),3)
            match = True
            pos['value'] = len(good)
            detected_pos.append(pos)
    return detected, detected_pos
