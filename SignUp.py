from tkinter import*
from tkinter import messagebox
import ast

window=Tk()
window.title("SignUp")
window.title('925x500+200+200')
window.configure(bg='#fff')
window.resizable(False,False)


img =PhotoImage(file='')
Label(window, image=img,border=0,bg='white').place(x=50)

Frame=Frame(window,width=350,height=390,bg='red')
Frame.place(x=480, y=50)

heading=Label(Frame,text='Registro', fg="#57a1f",bg='white',font=('Microsoft YaHei UI Light',23,'bold'))

##------

user = Entry(Frame,width=25,fg='black', border=2,bg='white',font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)

window.mainloop()
