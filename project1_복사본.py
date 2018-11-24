
from tkinter import * 
from tkinter.filedialog import *  # 파일 경로를 GUI를 사용할 수 있게해줌
from tkinter.simpledialog import * 
from wand.image import *


def displayImage(img,width,height):#이미지 출력
    global window, canvas,paper,photo,newPhoto,oriX,oriY

    window.geometry(str(width) + "x" + str(height)) # 이미지의 크기만큼 window창 조절
    if canvas != None: # 이미 사진이 출력된적 있으면 지움
        canvas.destroy()

    canvas = Canvas(window,width = width,height = height)
    # 이미지를 그리기위해 캔버스를 사진의 크기만큼 설정
    paper = PhotoImage(width=width,height=height) # 사진의 가로 세로만큼 설정
    canvas.create_image((width/2, height/2),image = paper,state="normal")
    # width/2 , height/2 위치에 이미지 생성(기본 생성위치가 중앙에서 시작하기 때문에 2로 나누어 좌표를 수정함) 

    blob=img.make_blob(format='RGB')
     # 이미지 포맷을 RGB로 설정
    for i in range(0, width):
        for k in range(0, height):
            r = blob[(i*3*width) + (k*3) + 0]# 3차원 이기때문에 가로 + 세로 + 차원
            g = blob[(i*3*width) + (k*3) + 1]
            b = blob[(i*3*width) + (k*3) + 2]
            paper.put("#%02x%02x%02x" %(r, g, b),(k, i))
            # 현실에서 표현하는 x ,y좌표와 이미지상에서 표현하는 x ,y좌표가 다르기때문에 x와 y를 바꾸어 준다.
            # 빈자리는 0으로 채우고 2자리면 출력
            # 좌표에 점을 찍어 표현

    canvas.pack()
    # 이미지 출력
                     
def funcOpen():#파일 열기 
    global window,canvas,paper,photo,newPhoto,oriX,oriY

    if canvas != None:
        canvas.destroy()

    readFp = askopenfilename(parent= window,filetypes=
                            (("모든 그림 파일","*.jpg;*.jpex;*.bmp;*.png;*.tif;*.gif"),("모든 파일","*.*")))

    if rreadFp == None:
        return
   
    photo = Image(filename=readFp)
    oriX=photo.width
    oriY=photo.height
    newPhoto= photo.clone()
    newX=newPhoto.width
    newY= newPhoto.height
    displayImage(newPhoto,newX,newY)

def funcSave(): #파일 저장
    
    global window,canvas,paper,photo,newPhoto,oriX,oriY

    if newPhoto == None:
         return
    if canvas != None:
        canvas.destroy()
    saveFp = asksaveasfile(parent = window,mode="w",defaultextension =".jpg",filetypes=(("JPG 파일","*.jpg;*.jpeg"),("모든 파일","*.*"))) #filedialog모듈 :파일 저장 상자
    savePhoto = newPhoto.convert("jpg")
    savePhoto.save(filename =saveFp.name)

def funcExit():#종료 
    global window
    window.destroy() 


def funcZoomInout():# 확대 축소 기능
    global window,canvas,paper,photo,newPhoto,oriX,oriY    
   
   
    scale = askfloat("확대/축소","확대/축소 배율(0.1~4.0)을 입력하세요",minvalue=0.1,maxvalue=4.0)
    # 실수 입력이 가능한 창을 띄워 배율입력 하도록 함. 최소 0.1 최대 4.0
    if scale == None:
        return

    newPhoto = photo.clone()
    # 원본 이미지를 복사함
    label2 = Label(window,text = '확대 축소: '+ str(scale)) 
    # 확대 축소기능을 실행했다는 글자와 어느정도 수치인지
    label2.pack(side = BOTTOM) # 위치는 아래쪽
    newPhoto.resize(int(oriX * scale),int(oriY * scale)) # 복사한 이미지를 배율만큼 재조정함
    newX= newPhoto.width # 변환된 이미지의 width
    newY=newPhoto.height # 변환된 이미지의 height 
    displayImage(newPhoto,newX,newY)

def funcFlip(): #상하 반전
    global window,canvas,paper,photo,newPhoto,oriX,oriY
    
    label2 = Label(window,text = '상하 반전')
    label2.pack()
    
    newPhoto = photo.clone() # 원본 이미지를 복사
    newPhoto.flip() # 복사한 이미지의 상하 반전 실행
    newX = newPhoto.width # 변환된 사진의 width 
    newY = newPhoto.height # 변환된 사진의 height
    displayImage(newPhoto,newX,newY)

def funcFlop(): # 좌우 반전 기능
    global window,canvas,paper,photo,newPhoto,oriX,oriY
    
    label2 = Label(window,text = '좌우 반전')
    label2.pack()
    
    newPhoto=photo.clone() # 원본 이미지를 복사
    newPhoto.flop() # 복사한 이미지의 좌우 반전 실행
    newX = newPhoto.width # 변환된 이미지의 width
    newY = newPhoto.height # 변환된 이미지의 height
    displayImage(newPhoto,newX,newY)

def funcRotate():#사진 회전
    global window,canvas,paper,photo,newPhoto,oriX,oriY        
    degree = askinteger("회전","회전할 각도(0~360)를 입력하세요",minvalue=0,maxvalue=360)
    # 정수 입력이 가능한 창을 띄워 회전할 각도를 입력받음 (최소 0도 ~ 최대 360도)
   
    if degree == None:
        return 
    newPhoto = photo.clone()
    # 원본 이미지를 복사
    label2 = Label(window,text = '회전: '+ str(degree))
    label2.pack(side = BOTTOM)
    newPhoto.rotate(degree)
    # 입력한 각도만큼 회전 실행
    newX = newPhoto.width
    # 변환된 이미지의 width
    newY = newPhoto.height
    # 변환된 이미지의 height
    displayImage(newPhoto,newX,newY)

def funcBrightness():#사진 명도
    global window,canvas,paper,photo,newPhoto,oriX,oriY
    
   
    value = askinteger("명도","값을 입력하세요(0~200)",minvalue=0,maxvalue=200)
    if value == None:
        return 
    
    newPhoto = photo.clone()
    label2 = Label(window,text = '명도: '+ str(value))
    label2.pack(side = BOTTOM)
    newPhoto.modulate(value,100,100)
    newX = newPhoto.width
    newY = newPhoto.height
    displayImage(newPhoto,newX,newY)

def funcSaturation():# 사진 채도
    global window,canvas,paper,photo,newPhoto,oriX,oriY    
    
    value = askinteger("채도","값을 입력하세요(0~200)",minvalue=0,maxvalue=200 )
    if value == None:
        return 
    photo2 = photo.clone()
    label2 = Label(window,text = '채도: '+ str(value))
    label2.pack(side = BOTTOM)
    photo2.modulate(100,value,100)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2,newX,newY)

def funcHue():#사진 색조
    global window,canvas,paper,photo,newPhoto,oriX,oriY
    
    
   
    value = askinteger("색조","값을 입력하세요(0~200)",minvalue=0,maxvalue=200 )
    if value == None:
        return 
    newPhoto = photo.clone()
    newPhoto.modulate(100,100,value) 
    label2 = Label(window,text = '색조: '+ str(value))
    label2.pack(side = BOTTOM)
    newX = newPhoto.width
    newY = newPhoto.height
    displayImage(newPhoto,newX,newY)

def funcBW():#사진 흑백 변환
    global window,canvas,paper,photo,newPhoto,oriX,oriY
    
    label2 = Label(window,text = '흑백')
    label2.pack()
    newPhoto = photo.clone()
    newPhoto.type = "grayscale"
    newX = newPhoto.width
    newY = newPhoto.height
    displayImage(newPhoto,newX,newY)



window,canvas,paper = None,None,None
photo, newPhoto = None,None
oriX, oriY =0,0


window= Tk() #윈도우와 메뉴 구성
window.geometry("400x400")
# 창의 너비와 높이 설정
window.title("파이썬 포토샵")
# 윈도우창의 제목 설정

button1 = Button(window,text = "안녕하세요.3조입니다.",command=quit)
# 윈도우창 맨위에 버튼을 만들고 버튼을 누르면 종료
button1.pack() # 할당

mainMenu = Menu(window) # 윈도우창에 메뉴 사용
window.config(menu = mainMenu) # 윈도우창에 메뉴등록
photo = PhotoImage() # 빈 사진을 저장
pLabel=Label(window,image = photo) # 윈도우 창에 라벨에 포함할 image를 설정
pLabel.pack(expand = 1,anchor = CENTER) # pack을 통해 라벨을 위젯배치 

# 파일 메뉴
fileMenu = Menu(mainMenu)  # 다른 메뉴 등록
mainMenu.add_cascade(label="파일",menu = fileMenu) # mainMenu와 fileMenu 연결
fileMenu.add_command(label="열기",command = funcOpen) # fileMenu에 열기 생성
fileMenu.add_command(label="저장",command = funcSave) # fileMenu에 저장 생성
fileMenu.add_separator()# 구분선 생성
fileMenu.add_command(label = "종료",command= funcExit)# fileMenu에 종료 생성

# 영상 처리 메뉴
imageMenu = Menu(mainMenu)# 다른 메뉴 등록
mainMenu.add_cascade(label="이미지",menu=imageMenu) # mainMenu와 imageMenu 연결
imageMenu.add_command(label="확대/축소",command=funcZoomInout) # imageMenu 확대/축소 생성
imageMenu.add_separator() # 구분선 생성
imageMenu.add_command(label="상하 반전",command=funcFlip) # imageMenu 상하 반전 생성
imageMenu.add_command(label="좌우 반전",command=funcFlop) # imageMenu 좌우 반전 생성
imageMenu.add_command(label="회전",command=funcRotate) # imageMenu 회전 생성
imageMenu.add_separator() # 구분선 생성
imageMenu.add_command(label="명도",command=funcBrightness) # imageMenu 명도 생성
imageMenu.add_command(label="채도",command=funcSaturation) # imageMenu 채도 생성
imageMenu.add_command(label="색조",command=funcHue) # imageMenu 색조 생성
imageMenu.add_separator() # 구분선 생성
imageMenu.add_command(label="흑백",command=funcBW) # imageMenu 흑백 생성
window.mainloop() # 윈도우 창을 윈도우가 종료될 때 까지 실행
