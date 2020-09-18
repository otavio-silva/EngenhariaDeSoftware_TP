def h():
    global x
    x = 909

def f():
    print(x)

def main():
    h()
    f()

if __name__ == "__main__":
   main()