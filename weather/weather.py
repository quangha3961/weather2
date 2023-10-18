from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk,messagebox
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz
from PIL import Image, ImageTk
import threading
import requests
import re
from datetime import datetime, timedelta
from datetime import datetime
from datetime import date
from functools import partial

root = tk.Tk()
root.title("Weather")
root.geometry("890x470+320+150")

def login():
    username = username_entry.get()
    password = password_entry.get()

    url = 'https://qldt.ptit.edu.vn/api/auth/login'
    payload = {
        'username':username,
        'password': password,
        'grant_type': 'password'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    r = requests.post(url, data=payload, headers=headers)

    if r.status_code!=200:
        result_label.config(text="Login failed")
    else:
        token = "Bearer " + r.json()['access_token']
        result_label.config(text="Login successful")
        data_url = 'https://qldt.ptit.edu.vn/api/sch/w-locdstkbtuanusertheohocky'
        date_header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Authorization': token,
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': '__zi=3000.SSZzejyD2CeYdgEpqWm8sIZ9eUVCGWR1QvMpxTDGHDDzXFUobL95bZ21yBwILGcJC8Mxl91N3PaqXx6s.1; _ga=GA1.3.649927060.1691975008; _ga_GXEC6VM3ZH=GS1.3.1696241093.1.1.1696241130.0.0.0; _gid=GA1.3.1341155159.1696550973; _ga_WF3VN29N2R=GS1.3.1696550974.29.0.1696550974.0.0.0; ASP.NET_SessionId=4pst5e4zv4udscqkv1fiieqf',
            'Host': 'qldt.ptit.edu.vn',
            'Idpc': '-6425855506493750551',
            'Origin': 'https://qldt.ptit.edu.vn',
            'Pragma': 'no-cache',
            'Referer': 'https://qldt.ptit.edu.vn/',
            'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }

        data_payload = {
            "filter": {
                "hoc_ky": 20231,
                "ten_hoc_ky": ""
            },
            "additional": {
                "paging": {
                    "limit": 100,
                    "page": 1
                },
                "ordering": [
                    {
                        "name": None,
                        "order_type": None
                    }
                ]
            }
        }

        response = requests.post(data_url, json=data_payload, headers=date_header)
        data = response.json()

        # Tao tu dien
        schedule = {}

        # lay thong tin qua tung tuan
        for week in data['data']['ds_tuan_tkb']:
            week_info = week['thong_tin_tuan']
            # Chuyển đổi giá trị week_info thành định dạng ngày tháng
            date_parttern = r"\d{2}/\d{2}/\d{4}"
            datess = re.findall(date_parttern, week_info)
            week_start = datetime.strptime(datess[0], '%d/%m/%Y').date()
            week_end = datetime.strptime(datess[1], '%d/%m/%Y').date()
            # danh sach buoi hoc trong tuan
            week_schedule = []

            # lay thong tin tung buoi hoc
            for lesson in week['ds_thoi_khoa_bieu']:
                thu = lesson['thu_kieu_so']
                day = week_start + timedelta(days=thu-2)
                course = lesson['ten_mon']
                start = lesson['tiet_bat_dau']

                # gio bat dau va ket thuc
                start_time = data['data']['ds_tiet_trong_ngay'][start - 1]['gio_bat_dau']
                end_time = data['data']['ds_tiet_trong_ngay'][start - 1]['gio_ket_thuc']

                # tao ban ghi cho buoi hoc
                lesson_info = {
                    'thu': thu,
                    'ngay': day,
                    'mon': course,
                    'start_time': start_time,
                    'end_time': end_time
                }

                # them ban ghi vao danh sach buoi hoc
                week_schedule.append(lesson_info)

            # luu danh sach buoi hoc vao tu dien
            schedule[week_info] = week_schedule
        date1 = date.today()
        dates = [date1 + timedelta(days=i) for i in range(7)]  
        
        def get_tkb(data):
            root3 = tk.Toplevel()
            root3.title("Thời khóa biểu")
            root3.geometry("500x235+510+260")
            root3.resizable(False, False)
            for item in data:
                label = tk.Label(root3, text=f'{item[0]}\n{item[1]} - {item[2]}')
                label.pack()
            root3.mainloop()
        for week, sessions in schedule.items():
            data_t,data_t1,data_t2,data_t3,data_t4,data_t5,data_t6=[],[],[],[],[],[],[]
            for session in sessions:
                for t in range(7):
                    if session['ngay'] == dates[t]:
                        a=session["mon"]
                        b=session['start_time']
                        c=session['end_time']
                        if t==0: 
                            l1.config(bg="red")
                            data_t.append((a,b,c))
                        if t==1: 
                            l2.config(bg="red")
                            data_t1.append((a,b,c))
                        if t==2: 
                            l3.config(bg="red")
                            data_t2.append((a,b,c))
                        if t==3: 
                            l4.config(bg="red")
                            data_t3.append((a,b,c))
                        if t==4: 
                            l5.config(bg="red")
                            data_t4.append((a,b,c))
                        if t==5: 
                            l6.config(bg="red")
                            data_t5.append((a,b,c))
                        if t==6: 
                            l7.config(bg="red")
                            data_t6.append((a,b,c))
            if len(data_t)>0:
                open1=Button(firstframe,text="open",bg="red",fg="#fff",command=lambda data_t=data_t:get_tkb(data_t))
                open1.place(x=20,y=100)               
            if len(data_t1)>0:
                open2=Button(secondframe,text="open",bg="red",fg="#fff",command=lambda data_t1=data_t1:get_tkb(data_t1))
                open2.place(x=20,y=100)
            if len(data_t2)>0:
                open3=Button(thirdframe,text="open",bg="red",fg="#fff",command=lambda data_t2=data_t2:get_tkb(data_t2))
                open3.place(x=20,y=100)
            if len(data_t3)>0:
                open4=Button(fourthframe,text="open",bg="red",fg="#fff",command=lambda data_t3=data_t3:get_tkb(data_t3))
                open4.place(x=20,y=100)
            if len(data_t4)>0:
                open5=Button(fifthframe,text="open",bg="red",fg="#fff",command=lambda data_t4=data_t4:get_tkb(data_t4))
                open5.place(x=20,y=100)
            if len(data_t5)>0:
                open6=Button(sixthframe,text="open",bg="red",fg="#fff",command=lambda data_t5=data_t5:get_tkb(data_t5))
                open6.place(x=20,y=100)
            if len(data_t6)>0:
                open7=Button(seventhframe,text="open",bg="red",fg="#fff",command=lambda data_t6=data_t6:get_tkb(data_t6))
                open7.place(x=20,y=100)
        root2.destroy()

def bt_ptit():
    global root2
    root2 = tk.Toplevel()
    root2.title("Login")
    root2.geometry("500x235+510+260")
    root2.resizable(False, False)

    image_icon2 = PhotoImage(file="weather/image/logo2.png")
    root2.iconphoto(True, image_icon2) 

    username_label = Label(root2, text="Username:")
    username_label.place(x=140, y=50)

    password_label = Label(root2, text="Password:")
    password_label.place(x=140, y=80)

    global username_entry
    username_entry = Entry(root2)
    username_entry.place(x=240, y=50)

    global password_entry
    password_entry = Entry(root2, show="*")  
    password_entry.place(x=240, y=80)

    login_button = Button(root2, text="Login", command=login)
    login_button.place(x=240, y=120)

    global result_label
    result_label = Label(root2, text="")
    result_label.place(x=225, y=150)


def getWeather():
    threading.Thread(target=getWeather_thread).start()
    

def getWeather_thread():
    city=textfield.get()

    geolocator=Nominatim(user_agent="geiapiExercises")
    location=geolocator.geocode(city)
    obj=TimezoneFinder()

    result=obj.timezone_at(lng=location.longitude,lat=location.latitude)
    timezone.config(text=result)
    long_lat.config(text=f"{round(location.latitude,4)}°N,{round(location.longitude,4)}°E")

    home=pytz.timezone(result)
    local_time=datetime.now(home)
    current_time=local_time.strftime("%I:%M %p")
    clock.config(text=current_time)

    #weather
    api="https://api.openweathermap.org/data/3.0/onecall?lat="+str(location.latitude)+"&lon="+str(location.longitude)+"&units=metric&exclude=hourly&appid=49ae2e9c5214489d95f13b5e43087667"
    json_data=requests.get(api).json()

    #current
    temp=json_data['current']['temp']
    humidity=json_data['current']['humidity']
    pressure=json_data['current']['pressure']
    wind=json_data['current']['wind_speed']
    description=json_data['current']['weather'][0]['description']

    t.config(text=(temp,"°C"))
    h.config(text=(humidity,"%"))
    p.config(text=(pressure,"hPa"))
    w.config(text=(wind,"m/s"))
    d.config(text=description)

    #firstcell
    firstdayimage=json_data['daily'][0]['weather'][0]['icon']
    
    photo1=ImageTk.PhotoImage(file=f"weather\icon\{firstdayimage}.png")
    firstimage.config(image=photo1)
    firstimage.image=photo1

    #secondcell
    seconddayimage=json_data['daily'][1]['weather'][0]['icon']
    
    img=(Image.open(f"weather\icon\{seconddayimage}.png"))
    resized_image=img.resize((50,50))
    photo2=ImageTk.PhotoImage(resized_image)
    secondimage.config(image=photo2)
    secondimage.image=photo2

    #thirdcell

    thirddayimage=json_data['daily'][2]['weather'][0]['icon']
    
    img=(Image.open(f"weather\icon\{thirddayimage}.png"))
    resized_image=img.resize((50,50))
    photo3=ImageTk.PhotoImage(resized_image)
    thirdimage.config(image=photo3)
    thirdimage.image=photo3
    #fourthcell

    fourthdayimage=json_data['daily'][3]['weather'][0]['icon']
    
    img=(Image.open(f"weather\icon\{fourthdayimage}.png"))
    resized_image=img.resize((50,50))
    photo4=ImageTk.PhotoImage(resized_image)
    fourthimage.config(image=photo4)
    fourthimage.image=photo4
    #fifthcell
    fifthdayimage=json_data['daily'][4]['weather'][0]['icon']
    
    img=(Image.open(f"weather\icon\{fifthdayimage}.png"))
    resized_image=img.resize((50,50))
    photo5=ImageTk.PhotoImage(resized_image)
    fifthimage.config(image=photo5)
    fifthimage.image=photo5
    #sixthcell
    sixthdayimage=json_data['daily'][5]['weather'][0]['icon']
    
    img=(Image.open(f"weather\icon\{sixthdayimage}.png"))
    resized_image=img.resize((50,50))
    photo6=ImageTk.PhotoImage(resized_image)
    sixthimage.config(image=photo6)
    sixthimage.image=photo6
    #seventhcell
    seventhdayimage=json_data['daily'][6]['weather'][0]['icon']
    
    img=(Image.open(f"weather\icon\{seventhdayimage}.png"))
    resized_image=img.resize((50,50))
    photo7=ImageTk.PhotoImage(resized_image)
    seventhimage.config(image=photo7)
    seventhimage.image=photo7

    #days
    first=datetime.now()
    day1.config(text=first.strftime("%A"))
    
    second=first+timedelta(days=1)
    day2.config(text=second.strftime("%A"))

    third=first+timedelta(days=2)
    day3.config(text=third.strftime("%A"))

    fourth=first+timedelta(days=3)
    day4.config(text=fourth.strftime("%A"))

    fifth=first+timedelta(days=4)
    day5.config(text=fifth.strftime("%A"))
    

    sixth=first+timedelta(days=5)
    day6.config(text=sixth.strftime("%A"))

    seventh=first+timedelta(days=6)
    day7.config(text=seventh.strftime("%A"))
    
#backgr
bgimg= tk.PhotoImage(file = "weather\image\gr3.png")
limg= Label(root, i=bgimg)
limg.pack()
root.resizable(FALSE,FALSE)

#icon
image_icon = PhotoImage(file="weather\image\logo.png")
root.iconphoto(False, image_icon)

Round_box=PhotoImage(file="weather\image\gr6.png")
Label(root,image=Round_box).place(x=70,y=86)
#label
label1=Label(root,text="Temperature",font=('Helvetica',11),fg="white",bg="#203243")
label1.place(x=90,y=100)

label2=Label(root,text="Humidity",font=('Helvetica',11),fg="white",bg="#203243")
label2.place(x=90,y=138)

label3=Label(root,text="Pressure",font=('Helvetica',11),fg="white",bg="#203243")
label3.place(x=90,y=176)

label4=Label(root,text="Wind Speed",font=('Helvetica',11),fg="white",bg="#203243")
label4.place(x=90,y=214)

label5=Label(root,text="Description",font=('Helvetica',11),fg="white",bg="#203243")
label5.place(x=90,y=252)

# Search
Search_img=PhotoImage(file="weather\image\gr10.png")
Label(root,image=Search_img).place(x=330,y=180)

textfield=tk.Entry(root,justify='center',width=20,font=('poppins',25,'bold'),bg="#131c24",border=0,fg="white")
textfield.place(x=360,y=193)
textfield.focus()

Search_icon=PhotoImage(file="weather\image\srch.png")
myimg_icon=Button(image=Search_icon,borderwidth=0,cursor="hand2",bg="#131c24",command=getWeather)
myimg_icon.place(x=735,y=190)

#bottombox
frame=Frame(root,width=900,height=180,bg="#0d0e0f")
frame.place(x=0,y=320)

#bottom boxers
firstbox=PhotoImage(file="weather\image\c12.png")
secondbox=PhotoImage(file="weather\image\c13.png")

l1=Label(frame,image=firstbox)
l1.place(x=30, y=20)
l2=Label(frame,image=secondbox)
l2.place(x=320,y=9)
l3=Label(frame,image=secondbox)
l3.place(x=416,y=9)
l4=Label(frame,image=secondbox)
l4.place(x=512,y=9)
l5=Label(frame,image=secondbox)
l5.place(x=608,y=9)
l6=Label(frame,image=secondbox)
l6.place(x=704,y=9)
l7=Label(frame,image=secondbox)
l7.place(x=800,y=9)

#clock
clock=Label(root,font=("Helvetica",30,'bold'),fg="white",bg="#406385")
clock.place(x=80,y=20)
#timezone
timezone=Label(root,font=("Helvetica",20,'bold'),fg="white",bg="#406385")
timezone.place(x=710,y=50)

long_lat=Label(root,font=("Helvetica",10,'bold'),fg="white",bg="#406385")
long_lat.place(x=730,y=80)

#thpwd
t=Label(root,width=7,font=("Helvetica",11),fg="white",bg="#203243")
t.place(x=190,y=100)
h=Label(root,width=7,font=("Helvetica",11),fg="white",bg="#203243")
h.place(x=190,y=138)
p=Label(root,width=7,font=("Helvetica",11),fg="white",bg="#203243")
p.place(x=190,y=176)
w=Label(root,width=7,font=("Helvetica",11),fg="white",bg="#203243")
w.place(x=190,y=214)
d=Label(root,width=7,font=("Helvetica",11),fg="white",bg="#203243")
d.place(x=190,y=252)

#first cell
firstframe=Frame(root,width=265,height=110,bg="#282829")
firstframe.place(x=32,y=342)

day1=Label(firstframe,font="arial 20",bg="#282829",fg="#fff")
day1.place(x=100,y=5)

firstimage=Label(firstframe,bg="#282829")
firstimage.place(x=1,y=14)

#second cell
secondframe=Frame(root,width=80,height=132,bg="#282829")
secondframe.place(x=322,y=330)

day2=Label(secondframe,font="arial 8",bg="#282829",fg="#fff")
day2.place(x=15,y=5)

secondimage=Label(secondframe,bg="#282829")
secondimage.place(x=13,y=32)

#third cell
thirdframe=Frame(root,width=80,height=132,bg="#282829")
thirdframe.place(x=418,y=330)

day3=Label(thirdframe,font="arial 8",bg="#282829",fg="#fff")
day3.place(x=15,y=5)

thirdimage=Label(thirdframe,bg="#282829")
thirdimage.place(x=13,y=32)

#fourth cell
fourthframe=Frame(root,width=80,height=132,bg="#282829")
fourthframe.place(x=514,y=330)

day4=Label(fourthframe,font="arial 8",bg="#282829",fg="#fff")
day4.place(x=15,y=5)

fourthimage=Label(fourthframe,bg="#282829")
fourthimage.place(x=13,y=32)

#fifth cell
fifthframe=Frame(root,width=80,height=132,bg="#282829")
fifthframe.place(x=610,y=330)

day5=Label(fifthframe,font="arial 8",bg="#282829",fg="#fff")
day5.place(x=15,y=5)

fifthimage=Label(fifthframe,bg="#282829")
fifthimage.place(x=13,y=32)

#sixth cell
sixthframe=Frame(root,width=80,height=132,bg="#282829")
sixthframe.place(x=706,y=330)

day6=Label(sixthframe,font="arial 8",bg="#282829",fg="#fff")
day6.place(x=15,y=5)

sixthimage=Label(sixthframe,bg="#282829")
sixthimage.place(x=13,y=32)

#seventh cell
seventhframe=Frame(root,width=80,height=132,bg="#282829")
seventhframe.place(x=802,y=330)

day7=Label(seventhframe,font="arial 8",bg="#282829",fg="#fff")
day7.place(x=15,y=5)


seventhimage=Label(seventhframe,bg="#282829")
seventhimage.place(x=13,y=32)
#ptit
Round_box2=PhotoImage(file="weather\image\gr12.png")
Label(root,image=Round_box2).place(x=720,y=10)

button1 = tk.Button(root, text="PTIT",font=('Helvetica',11),fg="red",command=bt_ptit)
button1.place(x=775,y=12)

root.mainloop()