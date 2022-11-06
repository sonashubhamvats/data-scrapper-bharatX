import pytesseract
import cv2
from PIL import Image
from pdf2image import convert_from_path
import numpy as np
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from difflib import SequenceMatcher
import os
import time
pytesseract.pytesseract.tesseract_cmd ='../Tesseract-OCR/tesseract.exe'

def tiny_file_rename(newname, folder_of_download, time_to_wait=60):
    time_counter = 0
    filename = max([f for f in os.listdir(folder_of_download)], key=lambda xa :   os.path.getctime(os.path.join(folder_of_download,xa)))
    while '.part' in filename:
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise Exception('Waited too long for file to download')
    filename = max([f for f in os.listdir(folder_of_download)], key=lambda xa :   os.path.getctime(os.path.join(folder_of_download,xa)))
    os.rename(os.path.join(folder_of_download, filename), os.path.join(folder_of_download, newname))


#constants
husband_hindi='pati'
father_hindi="pita"
entity_field_hindi="nirvachaka ka nama"
alt_entity_field_hindi="nama"
alt_husband_hindi='pati ka nama'
alt_father_hindi="pita ka nama"


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#returns a viable format of data for one entity
def refine_format(txt):
    txt=(transliterate(txt, sanscript.DEVANAGARI, sanscript.ITRANS))
    eng_txt=txt.lower()
    labels=eng_txt.split('\n')
    name_found=False
    info_bout_person={}
    for raw in labels:
        if len(raw.strip())>0:
            split_colon=raw.split(':')
            if(len(split_colon)==2):
                key=split_colon[0]
                val=split_colon[1].strip()
                if max(similar(key,entity_field_hindi),similar(key,alt_entity_field_hindi))>0.7:
                    info_bout_person['name']=val
                ratio_husband=max(similar(key,husband_hindi),
                         similar(key,alt_husband_hindi))
                ratio_father=max(similar(key, father_hindi),
                                 similar(key, alt_father_hindi))
                if ratio_husband>ratio_father and ratio_husband>0.7:
                    info_bout_person['husband-name'] = val
                elif ratio_father>0.7:
                    info_bout_person['father-name']=val
    return info_bout_person

#get a larger dataset of all the pages in the file
def get_info_about_all():
    print("Changing the name of the file...")
    tiny_file_rename("test-main.pdf", '../testElectoralRoll')
    time.sleep(3)
    pages = convert_from_path('../testElectoralRoll/test-main.pdf', grayscale=True)
    print("Parsing done for pages of the pdf file..")
    print("Total pages to process ", len(pages)-3)
    consolidated_info=[]
    for j in range(2,len(pages)-1):
        print('Processing for page no - ',j)
        p_3=np.array(pages[j])

        # detecting the lines in the image
        low_threshold = 100
        high_threshold = 200
        edges = cv2.Canny(p_3, low_threshold, high_threshold)

        # I came upon the values through trial and error
        rho = 1
        theta = np.pi / 180
        threshold = 20
        min_line_length = 460  # minimum number of pixels making up a line
        max_line_gap = 10  # maximum gap in pixels between connectable line segments
        line_image = np.copy(p_3) * 0

        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

        cnt, h = cv2.findContours(line_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for i in range(len(cnt)):
            area = cv2.contourArea(cnt[i])
            if(area>10000 and area<100000):
                x,y,w,h = cv2.boundingRect(cnt[i])
                crop= p_3[ y:h+y,x:w+x]
                data = Image.fromarray(crop)
                text = pytesseract.image_to_string(data, lang="hin")
                info=refine_format(text)
                consolidated_info.append(info)
        print('Processing done for page no - ', j)
    os.remove("../testElectoralRoll/test-main.pdf")
    return consolidated_info


