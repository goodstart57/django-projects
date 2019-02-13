from django.shortcuts import render
from datetime import date

import requests
import random
import time
import os

def index(request):
    context = {
        "msg": "안녕하세요",
        "name": "이재서",
    }
    return render(request, "index.html", context)

def is_val(request):
    today = date.today()
    context = {
        "msg": "맞다." if today == date(today.year, 2, 14) else "아니다."
    }
    return render(request, "msg.html", context)

def cube(request, number):
    return render(request, "cube.html", {"msg": number ** 3})

def ispal(request, string):
    return render(request, "msg.html", {"msg": "예" if string == string[::-1] else "아니요"})

def show_rimage(request):
    return render(request, "rimage.html")

def artii_new(request):
    return render(request, "artii_new.html")

def artii(request):
    string = request.GET.get("string")
    font_list = open("pages/assets/data/artii_font.txt", 'r').readlines()
    f_ind = random.randint(0, 417)
    font = font_list[f_ind].strip("\n")
    url = "http://artii.herokuapp.com/make?text={string}&font={font}".format(string=string, font=font)
    artii_res = requests.get(url)
    return render(request, "artii.html", {"result": artii_res.text})

def artii_all(request, string):
    font_list = list(map(lambda x: x.strip("\n"), open("pages/assets/data/artii_font.txt", 'r').readlines()))
    result = []
    for i in range(1, 419):
        with open(f"pages/assets/data/bigs{i}.txt", "r") as f:
            result.append((i, "".join(f.readlines())))
    print(result[0])
    print(result[0][1])
    return render(request, "artii.all.html", {"result": result})

def ppg_new(request):
    return render(request, "papago_new.html")

def ppg_trans(request):
    result = request.GET.get("word")
    url = f"https://openapi.naver.com/v1/papago/n2mt"
    print(url)
    res = requests.post(
        url=url,
        data={
            "source": "ko",
            "target": "en",
            "text": result,
        },
        headers={
            "X-Naver-Client-Id": os.getenv("N_ID"),
            "X-Naver-Client-Secret": os.getenv("N_PW"),
        }
    )
    result = res.json().get("message").get("result").get("translatedText")
    context = {
        "result": result
    }
    return render(request, "papago_trans.html", context)