import re

import pytesseract
from PIL import Image

# Scoreboard position
x, y, w, h = 243, 614, 795, 41

def get_info(frame, prev_score=0):
    scoreboard_img = frame[y:y+h, x:x+w]
    scoreboard_img = Image.fromarray(scoreboard_img)
    ocr_result = pytesseract.image_to_string(scoreboard_img)
    ocr_result_split = ocr_result.split()

    if len(ocr_result_split)>0 and ocr_result_split[0].lower()=="jazz" and ocr_result_split[2].lower()=="cavaliers":
        score = ocr_result_split[3]
        socre = score.replace("o", "0")
        score = score.replace("O", "0")
        score = re.sub("[^0-9]", "", score)

        if len(score) > 0:
            score = int(score)
            diff = score - prev_score
            if diff>0 and diff<=3:
                score_change = score - prev_score
                return score, score_change
    return prev_score, 0
