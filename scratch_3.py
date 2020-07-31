while True:
    userinput = input("talk some with me")
    if userinput == "How are you":
        print("I am fine ,thank you.")

    if userinput == "baidu":
        baidu = input("what do you want to search")
        print("https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&ch=&tn=baiduerr&bar=&wd=" + baidu)

    if userinput == "Hello":
        print("Hi")

    if userinput == "google":
        google = input("what do you want to search")
        print("https://www.google.com/search?q=" + google)

    if userinput == ("help"):
        print("What's metter with you,You can sand e-mail to owen6666662019@outlook.com")
