import requests
import os
import cv2
import easyocr
import matplotlib.pyplot as plt
from flask import Flask, redirect, render_template, url_for
import re

app = Flask(__name__)
app.debug = True
"""
def obr():
    image = "obr3.jpg"
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image)
    list1=[]
    for item in result:
        list1.append(item[1])

    print(list1)
    img = cv2.imread(image)
    for detection in result:
        top_left = tuple([int(val) for val in detection[0][0]])
        bottom_right = tuple([int(val) for val in detection[0][2]])
        text = detection[1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.rectangle(img, top_left, bottom_right, (0,255,0),5)
        img = cv2.putText(img, text, top_left, font, 1, (255,0,0),2, cv2.LINE_AA)
    #plt.figure(figsize=(10,10))
    #plt.imshow(img)
    #plt.show()  
    wanted = "kahootit"
    result_final = list(filter(lambda x: wanted in x, list1))
    print (result_final)
    return (result_final)
"""
x=0

@app.route("/")
def answer():
    global x

    try:
        if x==0: 
            #url = str(obr())
            #kahoot_id = url.split('quiz')[1][:-2][3:]
            kahoot_id = "eafc6258-072e-4375-99c0-2f4f5e422469"
            print(kahoot_id)
        x=0
        answers_url = 'https://create.kahoot.it/rest/kahoots/{kahoot_id}/card/?includeKahoot=true'.format(kahoot_id=kahoot_id)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        request = requests.get(answers_url).json()
        kjson = open(dir_path + "\kahooter.json","w+")
        kjson.write(str(request))   
        kjson.close()
        test_html = []
        test2_html = []
        for q in request['kahoot']['questions']:
            for choice in q['choices']:
                if choice['correct']:
                    break
            print('Q: {:<70} A: {} '.format(q['question'].replace('&nbsp;', ' '), choice['answer'].replace('&nbsp;', ' ')))
            question_html = q['question']
            answer_html = choice['answer']
            question_html= re.sub('<b>|</b>|<latex>|</latex>', '', question_html)
            answer_html= re.sub('<b>|</b>|<latex>|</latex>', '', answer_html)
            test_html.append(question_html)      
            test2_html.append(answer_html)   
 
        return render_template ("index.html", test_html=test_html, test2_html=test2_html) 
    except Exception as e:
        print(e)
        x = 1
        print("Failed to recognize QuizID, try entering it manually")
        answer(input())
    print ()
    
    
    

if __name__=="__main__":
    app.run() 