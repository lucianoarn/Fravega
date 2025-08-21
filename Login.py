from tkinter import*
from tkinter import messagebox

root=Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False,False)

img=PhotoImage(file='Fravega.png')
Label(root, image=img ,bg='white').place(x=50,y=50)

frame=Frame(root, width=350, height=350, bg="white")
frame.place(x=480,y=70)

heading=Label(frame,text='Ingresar', fg='#57a1f8',bg='white', font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)

#-----------------------------aca abajo esta el usuario

user = Entry(frame,width=25,fg='black',border=0,bg="white", font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Usuario')

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

#------------------------------aca abajo la contra

user = Entry(frame,width=25,fg='black',border=0,bg="white", font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Contraseña')

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

#####

Button(frame,width=39,pady=7,text="Ingrese",bg='#57a1f8',fg='white',border=0).place(x=35 , y=204)
label=Label(frame,text="No tenes cuenta?",fg='black',bg='white', font=('Microsoft YaHei UI Light',9))
label.place(x=75,y=270)

ingresar = Button(frame,width=6,text='Ingresar',border=0,bg='white',cursor='hand',fg='#57a1f8')

root.mainloop()
