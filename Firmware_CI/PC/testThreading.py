import threading 
import time 
import tkinter
def test() :
    while True :
        print("a")
        time.sleep(1)
        print("b")
        time.sleep(1)
thr = threading.Thread(target=test,daemon=True)
main = tkinter.Tk()
button = tkinter.Button(main,text="Test",command=thr.start)
button.pack(
)
tkinter.mainloop()