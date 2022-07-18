from tkinter import *
from tkinter.font import BOLD
import tkinter.messagebox as tmsg
from typing import Sized
from PIL import ImageTk, Image
import json
import os
from cryptography.fernet import Fernet
key=Fernet.generate_key()
fernet=Fernet(key)

# ---------------------------------- Creating ROOT ELEMENT window --------------------------------------#
root=Tk()
root.minsize(800,600)
root.maxsize(800,600)
imgTitle=PhotoImage(file="imgLock.png")
root.iconphoto(True,imgTitle)
image=Image.open("imgLock.png").resize((300,300), Image.ANTIALIAS)
root.title("Password Manager")

# ---------------------------- Canvas for picture of Lock ---------------------------#
canvas=Canvas(height=300,width=300)
canvas.place(x=250,y=20)
canvas.config(bg="#00ADE7",highlightthickness=0)
imgMainLock=ImageTk.PhotoImage(image)
canvas.create_image(150,150,image=imgMainLock)

root.config(bg="#00ADE7")


##################################################################################################
frame=Frame(root,width=600,height=200,bg="#00ADE7")
frame.place(x=100,y=400)

#----------------------------- Row 1-----------------------------------#

l_Website=Label(frame,text="Website  ",font=("Courier",20,BOLD),bg="#00ADE7")
l_Website.grid(row=1,column=1)

e_Website=Entry(frame,width=25,font=("Courier",18,BOLD),bg="#50C7C8")
e_Website.grid(row=1,column=2)



#----------------------------- Row 2-----------------------------------#

l_Email=Label(frame,text="Email  ",font=("Courier",20,BOLD),bg="#00ADE7")
l_Email.grid(row=2,column=1)

e_Email=Entry(frame,width=25,font=("Courier",18,BOLD),bg="#50C7C8")
e_Email.grid(row=2,column=2)



#----------------------------- Row 3-----------------------------------#

l_Password=Label(frame,text="Password ",font=("Courier",20,BOLD),bg="#00ADE7")
l_Password.grid(row=3,column=1)

e_Password=Entry(frame,width=25,font=("Courier",18,BOLD),bg="#50C7C8")
e_Password.grid(row=3,column=2)


# ----------------- DEFINING ALL FUNCTIONS -------------------------#

def saveContent():
    emailLis=e_Email.get()
    pswdLis=e_Password.get()
    websiteLis=e_Website.get().upper()
    encodeEmail=fernet.encrypt(emailLis.encode())
    encodePswd=fernet.encrypt(pswdLis.encode())
    encodeWebsite=fernet.encrypt(websiteLis.encode())

    if(emailLis=="" or pswdLis=="" or websiteLis==""):
        tmsg.showinfo("Error","Some Data Missing")
        
    else:
        emailLis=e_Email.get()
        pswdLis=e_Password.get()
        websiteLis=e_Website.get().upper()

        encodeEmail=fernet.encrypt(emailLis.encode())
        encodePswd=fernet.encrypt(pswdLis.encode())
        encodeWebsite=fernet.encrypt(websiteLis.encode())
        print(encodePswd,type(encodePswd))
        new_data={websiteLis:{"email":str(emailLis),"password":str(pswdLis)}}        
        data={}

        try:
            with open("SavePassword.json","r") as dataFile:
                data=json.load(dataFile)
                data.update(new_data)
            with open("SavePassword.json","w") as dataFile:
                json.dump(data,dataFile,indent=4)
                tmsg.showinfo("Success","Data Saved Successfully")
                e_Email.delete(0,END)
                e_Password.delete(0,END)
                e_Website.delete(0,END)
        except:
            with open("SavePassword.json","w") as dataFile:
                json.dump(new_data,dataFile,indent=4)
                tmsg.showinfo("Success","Data Saved Successfully")
                e_Email.delete(0,END)
                e_Password.delete(0,END)
                e_Website.delete(0,END)

def searchContent():
    websiteLis=e_Website.get().upper()
    # try:
    with open("SavePassword.json","r") as dataFile:
        data=json.load(dataFile)
        
        if data[f"{websiteLis}"]:
            print("1")########################
            tempEmail=data[f"{websiteLis}"]["email"]
            print("2")#######################
            
            # print(res,type(res))
            print("3")####################
            # res1=fernet.decrypt(res).decode()
            print("4")########################
            
            temppswd=data[f"{websiteLis}"]["password"]
            print("4 working")
        tmsg.showinfo("Details",f"EMAIL    : {tempEmail}\nPassword : {temppswd}")
    # except:
        # tmsg.showinfo("Error",f"No Credential found for website {websiteLis.capitalize()}")

    
def DeleteContent():
    websiteLis=e_Website.get().upper()
    try:
        with open("SavePassword.json","r") as dataFile:
            data=json.load(dataFile)
        
        del data[websiteLis]

        with open("SavePassword.json","w") as dataFile:
            data=json.dump(data,dataFile,indent=4)
        tmsg.showinfo("Success","Data Deleted Successfully")

    except:
        tmsg.showinfo("Error",f"No Credential found for website {websiteLis.capitalize()}")

def clearAll():
    try:
        os.remove("SavePassword.json")
        tmsg.showinfo("Success","All Data Cleared")
    except:
        tmsg.showinfo("Status","No Data Available to delete")


#----------------------------- Row 4-----------------------------------#
buttonSave=Button(frame,text="Save",width=20,bg="#0096FF",font=("Courier",14,BOLD),command=saveContent)
buttonSave.grid(row=4,column=2)

buttonSearch=Button(frame,text="Search",width=15,bg="#0096FF",font=("Courier",12,BOLD),command=searchContent)
buttonSearch.grid(row=1,column=3)

buttonSearch=Button(frame,text="Delete",width=15,bg="#0096FF",font=("Courier",12,BOLD),command=DeleteContent)
buttonSearch.grid(row=4,column=3)

buttonSearch=Button(frame,text="ClearAll Data",width=15,bg="#0096FF",font=("Courier",12,BOLD),command=clearAll)
buttonSearch.grid(row=4,column=1)
#######################################################################################################
root.mainloop() # End of mainloop