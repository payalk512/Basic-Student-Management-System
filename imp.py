from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import sys
import cx_Oracle
from PIL import ImageTk,Image
import socket
import requests
import bs4
import datetime
import matplotlib.pyplot as plt
import numpy as np

dt = datetime.datetime.now()
top=""
#-----------------------SPLASH SCREEN--------------------
app = Tk()
app.title("Welcome!")

try:
	socket.create_connection(("www.google.com", 80))
	res1 = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
	soup = bs4.BeautifulSoup(res1.text, 'lxml')
	data1 = soup.find('img', {"class":"p-qotd"})
	q = data1['alt']
	i_url = data1['data-img-url']
	r = requests.get("https://www.brainyquote.com"+i_url)
	with open("im1.jpg", 'wb') as f:
		f.write(r.content)	
	res2 = requests.get("https://ipinfo.io/")
	data2 = res2.json()
	city = data2['city']
	website = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	loc = "&q=" + city
	api_key = "&appid=c6e315d09197cec231495138183954bd"
	t1 = requests.get(website + loc + api_key).json()['main']['temp']
except OSError:
	print("Check network")

lblCity = Label(app, text=city,font=("Times New Roman", 22, 'bold'))
lblCity.place(x=20, y=610)
temp = str(t1) + "\u00b0" + "C"
lblTemp = Label(app, text=temp, font=("Times New Roman", 22, 'bold'))
lblTemp.place(x=20, y=650)
lblDay = Label(app, text=str(dt.strftime("%A")), font=("Times New Roman", 22, 'bold'))
lblDay.place(x=850, y=610)
lblDate = Label(app, text=str(dt.date()), font=("Times New Roman", 22, 'bold'))
lblDate.place(x=830, y=650)

imgSp1 =Image.open('im1.jpg')
imgSp2 = ImageTk.PhotoImage(imgSp1)
w = imgSp2.width()
h = imgSp2.height()

app.geometry("1000x690+180+0")
label1 = Label(app, image=imgSp2,font=("Times New Roman", 24),justify=CENTER, width=1000,height=600)
label1.pack()
app.after(7000, app.destroy)
app.mainloop()

#-------------------------FRAMES-------------------------
root = Tk()
root.title("Student Management System")
root.geometry("700x600+330+50")
root.resizable(False, False)

img1 =Image.open('main.png')
img2 = ImageTk.PhotoImage(img1)
lbl1 = Label(root, image=img2,justify=CENTER,width=700, height=600)
lbl1.pack()

adst = Toplevel(root)
adst.title("Add details")
adst.geometry("700x600+330+50")
adst.resizable(False, False)
adst.withdraw()

img3 =Image.open('add.png')
img4 = ImageTk.PhotoImage(img3)
lbl2 = Label(adst, image=img4,justify=CENTER,width=700, height=600)
lbl2.pack()

vist = Toplevel(root)
vist.title("View details")
vist.geometry("750x600+330+50")
vist.resizable(False, False)
vist.withdraw()

img5 =Image.open('view.png')
img6 = ImageTk.PhotoImage(img5)
lbl3 = Label(vist, image=img6,justify=CENTER,width=750, height=600)
lbl3.pack()

upst = Toplevel(root)
upst.title("Update details")
upst.geometry("600x600+330+50")
upst.resizable(False, False)
upst.withdraw()

img7 =Image.open('update.png')
img8 = ImageTk.PhotoImage(img7)
lbl4 = Label(upst, image=img8,justify=CENTER,width=600, height=600)
lbl4.pack()

dest = Toplevel(root)
dest.title("Delete details")
dest.geometry("600x500+330+100")
dest.resizable(False, False)
dest.withdraw()

img9 =Image.open('del.png')
img10 = ImageTk.PhotoImage(img9)
lbl5 = Label(dest, image=img10,justify=CENTER,width=600, height=500)
lbl5.pack()

#-------------------------ROOT PAGE-------------------------
def f1():
	root.withdraw()
	adst.deiconify()
def f2():
	global top
	lstNam, lstSum = [], []
	root.withdraw()
	vist.deiconify()
	stData.configure(state='normal')
	entTop.configure(state='normal')
	con = None
	cursor = None
	try:
		stData.delete("1.0",END)
		entTop.delete(0,END)
		con = cx_Oracle.connect('system/abc123')
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		stData.insert(INSERT, "ROLL NO.\t\tNAME\t\tPHYSICS\t\tCHEMISTRY\t\tMATHS\t\tSUM\n\n")
		disp = ""
		for i in data:
			disp = disp + str(i[0]) + "\t\t" + str(i[1]) + "\t\t"  + str(i[2]) + "\t\t" + str(i[3]) + "\t\t"  + str(i[4]) + "\t\t" + str(i[5]) + "\n" 
			lstNam.append(i[1])
			lstSum.append(i[5])
		stData.insert(INSERT, disp)
		stData.configure(state='disabled')
		max, pk = lstSum[0], lstNam[0]
		for j in range(len(lstSum)):
			if lstSum[j] > max:
				max = lstSum[j]
				pk = lstNam[j]
		top = "TOPPER: " + str(pk) + " (" + str(max) + "/200)"
		entTop.insert(INSERT, top)
		entTop.configure(state='disabled')
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
def f3():
	root.withdraw()
	upst.deiconify()
def f4():
	root.withdraw()
	dest.deiconify()
def f12():
	sys.exit(0)
def f13():
	lstName, lstPhy, lstChe, lstMat = [], [], [], [] 
	con = None
	cursor = None
	try:
		con = cx_Oracle.connect('system/abc123')
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		res = cursor.fetchall()
		for i in res:
			lstName.append(i[1])
			lstPhy.append(i[2])
			lstChe.append(i[3])
			lstMat.append(i[4])
		x = np.arange(len(lstName))
		plt.bar(x, lstPhy, width=0.25, label='Physics', color='r', alpha=0.5)
		plt.bar(x+0.25, lstChe, width=0.25, label='Chemistry', color='b', alpha=0.3)
		plt.bar(x+0.5, lstMat, width=0.25, label='Maths', color='m', alpha=0.8)
		plt.xticks(x, lstName, fontsize=10)
		plt.title('CET Score')
		plt.xlabel('Names', fontsize=10)
		plt.ylabel('Marks', fontsize=10)
		plt.legend()
		plt.grid()
		plt.show()
	except IndexError:
		messagebox.showerror("Failure","No records found")
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
	
lblHead = Label(root, text="STUDENT'S DESK", font=('Algerian',36,'bold'))
lblHead.place(x=20, y=40)

btnAdd = Button(root, text="ADD", width=20, font=('Times New Roman',16,'bold'), command=f1)
btnView = Button(root, text="VIEW", width=20, font=('Times New Roman',16,'bold'), command=f2)
btnUpdate = Button(root, text="UPDATE", width=20, font=('Times New Roman',16,'bold'), command=f3)
btnDelete = Button(root, text="DELETE", width=20, font=('Times New Roman',16,'bold'), command=f4)
btnPerform = Button(root, text="PERFORMANCE", width=20, font=('Times New Roman',16,'bold'), command=f13)
btnLogout = Button(root, text="Exit", width=10, font=('Times New Roman',16,'bold'), command=f12)

btnAdd.place(x=20, y=150)
btnView.place(x=20, y=220)
btnUpdate.place(x=20, y=290)
btnDelete.place(x=20, y=360)
btnPerform.place(x=20, y=430)
btnLogout.place(x=350, y=500)

#----------------------ADD PAGE-----------------------
lblNo1 = Label(adst, text="Roll no.: ", font=('Times New Roman',24))
lblNo1.place(x=20, y=50)
entNo1 = Entry(adst, width=10, bd=5, font=('MS Comic Sans',20))
entNo1.place(x=150, y=50)

lblName = Label(adst, text="Name: ", font=('Times New Roman',24))
lblName.place(x=20, y=150)
entName = Entry(adst, width=25, bd=5, font=('MS Comic Sans',20))
entName.place(x=150, y=150)

lblMarks = Label(adst, text="Enter marks: ", font=('Times New Roman',24))
lblMarks.place(x=20, y=250)

lblPmks = Label(adst, text="Phy(of 50)", font=('Times New Roman',18))
lblPmks.place(x=20, y=310)
entPmks = Entry(adst, width=10, bd=5, font=('MS Comic Sans',16))
entPmks.place(x=20, y=350)

lblCmks = Label(adst, text="Chem(of 50)", font=('Times New Roman',18))
lblCmks.place(x=220, y=310)
entCmks = Entry(adst, width=10, bd=5, font=('MS Comic Sans',16))
entCmks.place(x=220, y=350)

lblMmks = Label(adst, text="Maths(of 100)", font=('Times New Roman',18))
lblMmks.place(x=420, y=310)
entMmks = Entry(adst, width=10, bd=5, font=('MS Comic Sans',16))
entMmks.place(x=420, y=350)


class A(Exception):
	def __init__(self, msga):
		self.msga = msga
class B(Exception):
	def __init__(self, msgb):
		self.msgb = msgb
class M(Exception):
	def __init__(self, msgm):
		self.msgm = msgm
def f5():
	con = None
	cursor = None
	try:
		l = []
		con = cx_Oracle.connect('system/abc123')
		cursor = con.cursor()
		no = int(entNo1.get())
		if no <= 0:
			raise A("Invalid ROLL NO.")
		name = entName.get()
		l = name.split(' ')
		for d in l:
			if d.isalpha() == False:
				raise B("Invalid literals for NAME") 
		phy = int(entPmks.get())
		che = int(entCmks.get())
		mat = int(entMmks.get())
		if phy<0 or phy>50 or che<0 or che>50 or mat<0 or mat>100:
			raise M("Invalid MARKS")	
		sum = phy+che+mat
		sql = "insert into student values('%d', '%s', '%d', '%d', '%d', '%d')"
		args = (no, name, phy, che, mat, sum)
		cursor.execute(sql%args)
		con.commit()
		messagebox.showinfo("Success", str(cursor.rowcount) + " record inserted")
	except A as a:
		messagebox.showerror("Error",a.msga)
	except B as b:
		messagebox.showerror("Error",b.msgb)
	except M as m:
		messagebox.showerror("Error",m.msgm)
	except ValueError:
		messagebox.showerror("Error", "Invalid ROLL NO. or MARKS")
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
		entName.delete(0,END)
		entNo1.delete(0,END)
		entPmks.delete(0,END)
		entCmks.delete(0,END)
		entMmks.delete(0,END)
		entNo1.focus()

def f6():
	adst.withdraw()
	root.deiconify()

btnSave5 = Button(adst, text="SAVE", width=15, font=('Times New Roman',16,'bold'), command=f5)
btnBack6 = Button(adst, text="BACK", width=15, font=('Times New Roman',16,'bold'), command=f6)

btnSave5.place(x=100, y=470)
btnBack6.place(x=350, y=470)

#-----------------------------VIEW PAGE-----------------------------
stData = scrolledtext.ScrolledText(vist, width=85, height=25)
stData.place(x=20, y=50)
def f7():
	vist.withdraw()
	root.deiconify()

entTop = Entry(vist, bd=2, width=25, font=('Times New Roman',18))
entTop.place(x=50, y=500)
btnBack7 = Button(vist, text="BACK", width=10, font=('Times New Roman',16,'bold'), command=f7)
btnBack7.place(x=550, y=500)

#-----------------------------UPDATE PAGE-----------------------------
lblNo2 = Label(upst, text="Roll no.: ", font=('Times New Roman',24))
lblNo2.place(x=20, y=100)
entNo2 = Entry(upst, width=10, bd=5, font=('MS Comic Sans',20))
entNo2.place(x=150, y=100)

lblMks2 = Label(upst, text="Marks: ", font=('Times New Roman',24))
lblMks2.place(x=20, y=200)
entMks2 = Entry(upst, width=25, bd=5, font=('MS Comic Sans',20))
entMks2.place(x=150, y=200)

lblFor = Label(upst, text="For subject:", font=('Times New Roman',24))
lblFor.place(x=20, y=300)

sub = IntVar()
sub.set(1)
rbPhy = Radiobutton(upst, text="Physics", variable=sub, value=1, font=('Times New Roman',20))
rbChe = Radiobutton(upst, text="Chemistry", variable=sub, value=2, font=('Times New Roman',20))
rbMat = Radiobutton(upst, text="Maths", variable=sub, value=3, font=('Times New Roman',20))
rbPhy.place(x=20, y=350)
rbChe.place(x=170, y=350)
rbMat.place(x=340, y=350)

def f8():
	con = None
	cursor = None
	try:
		con = cx_Oracle.connect('system/abc123')
		cursor = con.cursor()
		no = int(entNo2.get())
		if no <= 0:
			raise A("Invalid ROLL NO.")
		s = sub.get()
		if s==1:
			phy = int(entMks2.get())
			if phy<0 or phy>50:
				raise M("Invalid MARKS")
			sql = "update student set phy='%d' where no='%d'"
			args = (phy, no)
		elif s==2:
			che = int(entMks2.get())
			if che<0 or che>50:
				raise M("Invalid MARKS")
			sql = "update student set che='%d' where no='%d'"
			args = (che, no)
		else:
			mat = int(entMks2.get())
			if mat<0 or mat>100:
				raise M("Invalid MARKS")
			sql = "update student set mat='%d' where no='%d'"
			args = (mat, no)
		cursor.execute(sql%args)
		messagebox.showinfo("Success", str(cursor.rowcount) + " record updated")
		sql = "select no, phy, che, mat from student"
		cursor.execute(sql)
		sel = cursor.fetchall()
		for i in sel:
			if i[0] == no:
				sum = i[1]+i[2]+i[3]
				sql = "update student set sum='%d' where no='%d'"
				args = (sum, no)
				cursor.execute(sql%args)
				break
		con.commit()
	except A as a:
		messagebox.showerror("Error",a.msga)
	except M as m:
		messagebox.showerror("Error",m.msgm)
	except ValueError:
		messagebox.showerror("Error", "Invalid ROLL NO. or MARKS")
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
		entMks2.delete(0,END)
		entNo2.delete(0,END)
		entNo2.focus()
	
def f9():
	upst.withdraw()
	root.deiconify()

btnSave5 = Button(upst, text="UPDATE", width=10, font=('Times New Roman',16,'bold'), command=f8)
btnBack6 = Button(upst, text="BACK", width=10, font=('Times New Roman',16,'bold'), command=f9)

btnSave5.place(x=100, y=450)
btnBack6.place(x=350, y=450)

#-----------------------------DELETE PAGE-----------------------------
lblNo3 = Label(dest, text="Roll no.: ", font=('Times New Roman',24))
lblNo3.place(x=120, y=180)
entNo3 = Entry(dest, width=10, bd=5, font=('MS Comic Sans',20))
entNo3.place(x=250, y=180)

def f10():
	con = None
	cursor = None
	try:
		con = cx_Oracle.connect('system/abc123')
		cursor = con.cursor()
		no = int(entNo3.get())
		if no <= 0:
			raise A("Invalid roll no.")
		sql = "delete from student where no='%d'"
		args = (no)
		cursor.execute(sql%args)
		con.commit()
		messagebox.showinfo("Success", str(cursor.rowcount) + " record deleted")
	except A as a:
		messagebox.showerror("Error",a.msg)
	except ValueError:
		messagebox.showerror("Error", "Invalid roll no.")
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
		entNo3.delete(0,END)
		entNo3.focus()	
def f11():
	dest.withdraw()
	root.deiconify()

btnSave10 = Button(dest, text="DELETE", width=10, font=('Times New Roman',16,'bold'), command=f10)
btnBack11 = Button(dest, text="BACK", width=10, font=('Times New Roman',18,'bold'), command=f11)

btnSave10.place(x=100, y=350)
btnBack11.place(x=350, y=350)

root.mainloop()