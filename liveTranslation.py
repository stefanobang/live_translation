import subprocess
from tkinter import *

def enButton():
    value = int(inputType.get())
    str_value = str(value)
    subprocess.Popen(['start', 'cmd', '/k', 'python enTranslation.py', str_value], shell=True)
    # subprocess.Popen(['cmd', '/c', 'start', '/B', 'python', 'enTranslation.py', str_value], creationflags=subprocess.CREATE_NO_WINDOW)
    # cmd = ['python', 'enTranslation.py', str_value]
    # subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    
    
def korean_record():
    subprocess.Popen('start cmd /k python koreanTranslation.py', shell=True)


if __name__ == "__main__":
    #gui
    mainWin = Tk()

    mainWin.iconbitmap("icon.ico")

    mainWin.geometry("400x450")
    mainWin.title("liveTranslation")

    label1 = Label(mainWin, text = "아직 한글은 고퀄 번역은 힘들고 빠른 음성인 경우 오류가 매우 큼니다. \n빠른 음성은 영어 번역 사용해주세요")
    label2 = Label(mainWin, text = "\n영어로 버튼시 하나 고른뒤 버튼 클릭해주세요")
    

    inputType = IntVar() #자료형 지정
    radiobtnSmall = Radiobutton(mainWin, text="Base", value = 0, variable=inputType)
    radiobtnSmall.select()
    radiobtnMedium = Radiobutton(mainWin, text="Medium", value = 1, variable=inputType)
    radiobtnLarge = Radiobutton(mainWin, text="Large", value = 2, variable=inputType)

 
    
    btnKR = Button (mainWin, command = korean_record, text ="Translate to Korean(한글로 번역)")
    btnEn = Button (mainWin, command = enButton, text ="Translate to English(영어로 번역)")
    btnKR_improved = Button (text ="고속한글 번역(추가예정)")
    
    #trans_textbox = Text(mainWin, width=60, height=40)


    label1.pack()
    btnKR.pack()
    label2.pack()
    
    radiobtnSmall.pack()
    radiobtnMedium.pack()
    radiobtnLarge.pack()
    btnEn.pack()

    btnKR_improved.pack()
    #trans_textbox.pack(pady=20)
    
 
    mainWin.mainloop()

# pyinstaller --onefile --noconsole --clean --icon='icon.ico' --add-data 'icon.ico;.' liveTranslation.py
# pyinstaller --onefile --add-data "icon.ico;." --icon "icon.ico" liveTranslation.py
#  pyinstaller --onefile --icon=icon.ico liveTranslation.py

