from tkinter import *
import tkmacosx as tkm

from os.path import abspath, basename



class App:
    def __init__(self) -> None:
        self.tk = Tk()
        self.Password = StringVar()
        self.Username = StringVar()
        self.FullPath = abspath(__file__)
        self.FilePath = f"{self.FullPath[:-len(basename(self.FullPath))]}"
        self.tk.title("Login")
        Label(self.tk, text="Username",).grid(row=0, column=0,)
        self.et1 = Entry(self.tk, textvariable=self.Username).grid(row=1, column=0,)
        Label(self.tk, text="Password",).grid(row=2, column=0,)
        self.et2 = Entry(self.tk, textvariable=self.Password).grid(row=3, column=0,)
        self.bt1 = Button(self.tk, text="Submit", command=self.Submit).grid(row=4, column=0,)
        self.tk.mainloop()
    
    def Submit(self) -> None:
        #st = "{'Fireflare5': {'Email': '829005@kirkwoodschools.org', 'Password': 'YouShallNotPass'}}"
        #text = " ".join(format(ord(x), 'b') for x in st)
        #with open(f"{self.FilePath}UserList.txt", "w") as f:
            #f.write(text.encode("ascii").hex())
        with open(f"{self.FilePath}UserList.txt", "rb") as f:
            self.UserList = eval(f.read())
        try:
            self.User = self.UserList[self.Username.get()]
            if self.User["Password"] == self.Password.get():
                self.clear()
                self.rainbow()
        except:
            pass

    def clear(self):
        for widget in self.tk.winfo_children():
            widget.destroy()
        
    
    def rainbow(self):
        Frame(self.tk, width=200, height=150, bg="red", takefocus=1).grid(row=1, column=0,)
        Frame(self.tk, width=200, height=150, bg="blue", takefocus=1).grid(row=0, column=0,)
        Frame(self.tk, width=100, height=150, bg="yellow", takefocus=1).grid(row=1, column=1,)
        Frame(self.tk, width=100, height=150, bg="green", takefocus=1).grid(row=0, column=1,)
        
if __name__ == "__main__":
    app = App()