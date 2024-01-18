
import threading


def func(i):
    while 1:
        
        print(threading.current_thread())
        print(i)


if __name__ =="__main__":

    print("main")
    x1= threading.Thread(target=func, args=[1])
    print ("srarting1")
    x1.start()

    x2= threading.Thread(target=func, args=[2])
    print ("srarting1")
    x2.start()
    x2.join()
    x1.join()