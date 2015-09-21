import webbrowser
import threading
import os
newtab = 2 # open in a new tab, if possible

# open a public URL, in this case, the webbrowser docs

url = "http://127.0.0.1:8000"

class bottleThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        os.system("python runkeeper_demo.py")

class browserThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        webbrowser.open(url,new=newtab)



if __name__ == "__main__":
    thread1 = bottleThread()
    thread2 = browserThread()

    thread1.start() 
    thread2.start()
    print"Pulling data"
