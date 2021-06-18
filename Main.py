from tkinter import *
import tkinter as tk
from datetime import date 
from PIL import ImageTk
from tkinter import ttk
from tkcalendar import Calendar
import sqlite3 
import time

conn = sqlite3.connect("database1.sqlite")
cur = conn.cursor()

#SELECT show.Table_NO,show.Items,show.Quantity,price.Reupee,quantity*price.Reupee as Total_rupee FROM show JOIN price WHERE show.Items=price.Items AND show.Table_NO=1

cur.execute('''CREATE TABLE IF NOT EXISTS show
  (Table_NO INTEGER,Items varchar(1000),Quantity varchar(1000))''')
cur.execute('''CREATE TABLE IF NOT EXISTS price
  (Items varchar(1000),Rs_Per_Plate varchar(1000))''')
cur.execute('''CREATE TABLE IF NOT EXISTS total
  (Table_NO varchar(1000),Today_Date text,Amount varchar(1000))''')
cur.execute('''CREATE TABLE IF NOT EXISTS collection
  (Username varchar(20) PRIMARY KEY,Password varchar(20),Email varchar(20),Waiter varchar(20))''')

def delete2():
  screen3.destroy()

def delete3():
  sucessscreen.destroy()

def delete4():
  invalidscreen.destroy()
def delete5():
	validscreen.destroy()

def remove_allAdmin():
	x = tv.get_children()
	y = tv1.get_children()
	if x != '()':
		for child in x:
			tv.delete(child)
	
	if y != '()':
		for child in y:
			tv1.delete(child)

def remove_all():
	x = tv.get_children()
	if x != '()':
		for child in x:
			tv.delete(child)

def closeAdmin():
	screen3.destroy()

def close():
	screen4.destroy()
	screen.destroy()

def clean():
	remove_allAdmin()

def submit_sucess():
  global screen4
  screen4 = Toplevel(screen)
  screen4.title("Success")
  screen4.geometry("300x100")
  screen4.configure(bg="#ffffcc")
  screen4.resizable(False,False)
  screen4.iconbitmap('Icon/succes.ico') 
  Label(screen4, text = "Submit Success", fg = "#00cc00" ,bg="#ffffcc",font = ("calibri", 15,"bold")).pack()
  Button(screen4, text = "OK", width=10, height=1, command =close).pack()
  remove_all()
  table_entry.delete(0, END)
  stater_no.delete(0, END)
  maincourse_no.delete(0, END)
  roti_no.delete(0, END)
  rice_no.delete(0, END)

def submit_sucessAdmin():
  global screen3
  screen3 = Toplevel(screen2)
  screen3.title("Success")
  screen3.geometry("300x100")
  screen3.configure(bg="#ffffcc")
  screen3.resizable(False,False)
  screen3.iconbitmap('Icon/succes.ico') 
  Label(screen3, text = "Submit Success", fg = "#00cc00" ,bg="#ffffcc",font = ("calibri", 15,"bold")).pack()
  Button(screen3, text = "OK", width=10, height=1, command =closeAdmin).pack()
  remove_allAdmin()
  table_entry.delete(0, END)
  
def pay_succes():
	x=table_value.get()
	cur.execute('SELECT Table_NO,DATE(),SUM(show.Quantity*price.Rs_Per_Plate) FROM show JOIN price WHERE show.Items=price.Items AND show.Table_NO=(?)',(x,))
	row=cur.fetchall()
	conn.commit()

	y=' '
	d=date.today()
	cur.execute('INSERT OR IGNORE INTO total (Table_NO,Today_Date,Amount) VALUES (?,?,?)',(y,d,row[0][2]))
	cur.execute('DELETE FROM show WHERE Table_NO=(?)',(x,))
	conn.commit()
	submit_sucessAdmin()

def all_amount():
	def print_sel():
		d=cal.selection_get()
		top.destroy()
		cur.execute('SELECT Table_NO,Today_Date as Date,SUM(Amount) FROM total WHERE Today_Date=(?)',(d,))
		row=cur.fetchall()
		conn.commit()
		
		for i in row:
			tv1.insert('','end',values=i)

	global top
	top = tk.Toplevel(screen2)
	cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',cursor="hand1",date_pattern='y-mm-dd')
	cal.pack(fill="both", expand=True)
	ttk.Button(top, text="ok",command=print_sel).pack()

def pay():
	remove_all()
	x = table_value.get()

	cur.execute('SELECT show.Table_NO,show.Items,show.Quantity,price.Rs_Per_Plate,show.Quantity*price.Rs_Per_Plate as Total_rupee FROM show JOIN price WHERE show.Items=price.Items AND show.Table_NO=(?)',(x,))
	rows=cur.fetchall()
	conn.commit()

	for i in rows:
		tv.insert('','end',values=i)


	cur.execute('SELECT Table_NO,DATE(),SUM(show.Quantity*price.Rs_Per_Plate) FROM show JOIN price WHERE show.Items=price.Items AND show.Table_NO=(?)',(x,))
	row=cur.fetchall()
	conn.commit()

	for i in row:
		tv1.insert('','end',values=i)

def update_items():
	remove_all()
	a = stater.get()
	b = stat.get()
	c = maincourse.get()
	d = maico.get()
	e = roti.get()
	f = rono.get()
	g = rice.get()
	h =	rino.get()
	x = table_value.get()
	table_entry.delete(0, END)
	stater_no.delete(0, END)
	maincourse_no.delete(0, END)
	roti_no.delete(0, END)
	rice_no.delete(0, END)

	if(b != '0'):
		cur.execute('UPDATE show SET Quantity = Quantity + (?) WHERE Items = (?)',(b,a))

	if(d != '0'):
		cur.execute('UPDATE show SET Quantity = Quantity + (?) WHERE Items = (?)',(d,c))
		
	if(f != '0'):
		cur.execute('UPDATE show SET Quantity = Quantity + (?) WHERE Items = (?)',(f,e))
		
	if(h != '0'):
		cur.execute('UPDATE show SET Quantity = Quantity + (?) WHERE Items = (?)',(h,g))
		
	cur.execute('SELECT * FROM show WHERE Table_NO=(?) AND Quantity IS NOT NULL',(x,))
	rows=cur.fetchall()
	conn.commit()

	for i in rows:
		tv.insert('','end',values=i)


def remove():
	remove_all()
	a = stater.get()
	b = stat.get()
	c = maincourse.get()
	d = maico.get()
	e = roti.get()
	f = rono.get()
	g = rice.get()
	h =	rino.get()
	x = table_value.get()

	table_entry.delete(0, END)
	stater_no.delete(0, END)
	maincourse_no.delete(0, END)
	roti_no.delete(0, END)
	rice_no.delete(0, END)

	cur.execute('DELETE FROM show WHERE Table_NO=(?) AND Items=(?) AND Quantity=(?)',(x,a,b))
	cur.execute('DELETE FROM show WHERE Table_NO=(?) AND Items=(?) AND Quantity=(?)',(x,c,d))
	cur.execute('DELETE FROM show WHERE Table_NO=(?) AND Items=(?) AND Quantity=(?)',(x,e,f))
	cur.execute('DELETE FROM show WHERE Table_NO=(?) AND Items=(?) AND Quantity=(?)',(x,g,h))

	cur.execute('SELECT * FROM show WHERE Table_NO=(?)',(x,))
	rows=cur.fetchall()
	conn.commit()

	for i in rows:
		tv.insert('','end',values=i)

def showitems():
	remove_all()
	x = table_value.get()
	cur.execute('SELECT * FROM show WHERE Table_NO=(?)',(x,))
	rows=cur.fetchall()
	conn.commit()

	table_entry.delete(0, END)
	stater_no.delete(0, END)
	maincourse_no.delete(0, END)
	roti_no.delete(0, END)
	rice_no.delete(0, END)

	for i in rows:
		tv.insert('','end',values=i)

def showitemsAdmin():
	remove_all()
	x = table_value.get()
	cur.execute('SELECT * FROM show WHERE Table_NO=(?)',(x,))
	rows=cur.fetchall()
	conn.commit()

	for i in rows:
		tv.insert('','end',values=i)


def add():
	remove_all()
	a = stater.get()
	b = stat.get()
	c = maincourse.get()
	d = maico.get()
	e = roti.get()
	f = rono.get()
	g = rice.get()
	h =	rino.get()
	x = table_value.get()
	table_entry.delete(0, END)
	stater_no.delete(0, END)
	maincourse_no.delete(0, END)
	roti_no.delete(0, END)
	rice_no.delete(0, END)

	if(b != '0'):
		cur.execute('INSERT OR IGNORE INTO show (Table_NO,Items,Quantity) VALUES (?,?,?)',(x,a,b))

	if(d != '0'):
		cur.execute('INSERT OR IGNORE INTO show (Table_NO,Items,Quantity) VALUES (?,?,?)',(x,c,d))
		
	if(f != '0'):
		cur.execute('INSERT OR IGNORE INTO show (Table_NO,Items,Quantity) VALUES (?,?,?)',(x,e,f))
		
	if(h != '0'):
		cur.execute('INSERT OR IGNORE INTO show (Table_NO,Items,Quantity) VALUES (?,?,?)',(x,g,h))
		

	cur.execute('SELECT * FROM show WHERE Table_NO=(?) AND Quantity IS NOT NULL',(x,))
	rows=cur.fetchall()
	conn.commit()

	for i in rows:
		tv.insert('','end',values=i)

def managerscreen():
	global screen2
	global total_amount
	global table_value
	global table_entry
	global tv
	global tv1
	screen2 = Toplevel(login)
	screen2.geometry("1300x700+80+50")
	screen2.title("Bill Payment")
	screen2.iconbitmap('Icon/menupage.ico')
	screen2.resizable(False,False)

	table_value = StringVar()

	admin_data = Frame(screen2,bg="#ff80ff")
	admin_data.place(x=30,y=10,width=400,height=400)

	table=Label(admin_data,text="Enter Table No :",font=("Arial",15),fg="black",bg="#ff80ff").place(x=5,y=20)
	table_entry=Entry(admin_data,font=("times new roman",15),fg="black",bg="white",textvariable=table_value)
	table_entry.place(x=170,y=22)

	Button(admin_data,text="Show Items",font=("Arial",15),fg="black",bg="red",width=15,height=1,command=showitemsAdmin).place(x=100,y=100)
	Button(admin_data,text="Clear All",font=("Arial",15),fg="black",bg="lightgreen",width=15,height=1,command=clean).place(x=100,y=150)
	Button(admin_data,text="Take Bill Payment",font=("Arial",15),fg="black",bg="lightgreen",width=15,height=1,command=pay).place(x=100,y=200)
	Button(admin_data,text="Submit",font=("Arial",15),fg="black",bg="Green",width=15,height=1,command=pay_succes).place(x=100,y=250)
	Button(admin_data,text="Show All Amount",font=("Arial",15),fg="black",bg="blue",width=15,height=1,command=all_amount).place(x=100,y=350)
	
	Pay_data = Frame(screen2,bg="white")
	Pay_data.place(x=550,y=10,width=700,height=350)

	style = ttk.Style()
	style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 13)) # Modify the font of the body
	style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
	style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
	tv = ttk.Treeview(Pay_data,height=10,style="mystyle.Treeview")
	tv.pack()

	tv["columns"]=("1","2","3","4","5")
	tv.column("#0",width=0)
	tv.column("1",width=80)
	tv.column("2",width=170)
	tv.column("3",width=80)
	tv.column("4",width=120)
	tv.column("5",width=120)
	tv.heading("1", text="Table No")
	tv.heading("2", text="Items")
	tv.heading("3", text="Quantity")
	tv.heading("4", text="Rs Per Plate")
	tv.heading("5", text="Total Rupee")

	total_amount=Frame(screen2,bg="white")
	total_amount.place(x=550,y=400,width=700,height=200)

	style = ttk.Style()
	style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 13)) # Modify the font of the body
	style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
	style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
	tv1 = ttk.Treeview(total_amount,height=10,style="mystyle.Treeview")
	tv1.pack()

	tv1["columns"]=("1","2","3")
	tv1.column("#0",width=0)
	tv1.column("1",width=80)
	tv1.column("2",width=110)
	tv1.column("3",width=170)
	
	tv1.heading("1", text="Table No")
	tv1.heading("2",text="Date")
	tv1.heading("3", text="Total Amount")


def waiterscreen():
	global screen
	screen = Toplevel(login)
	screen.geometry("1300x700+80+50")
	screen.title("Order Receipt")
	screen.iconbitmap('Icon/menupage.ico')
	screen.resizable(False,False)

	global show_data
	global table_value
	global stater
	global maincourse
	global roti
	global rice
	global stat
	global maico
	global rono
	global rino
	global tv
	global table_entry
	global stater_no
	global maincourse_no
	global roti_no
	global rice_no

	table_value = StringVar()
	stat = StringVar()
	maico = StringVar()
	rono = StringVar()
	rino = StringVar()
	

	create_data = Frame(screen,bg="#ff80ff")
	create_data.place(x=30,y=10,width=600,height=650)

	table=Label(create_data,text="Enter Table NO :",font=("Arial",15),fg="black",bg="#ff80ff").place(x=20,y=20)
	table_entry=Entry(create_data,font=("times new roman",15),fg="black",bg="white",textvariable=table_value)
	table_entry.place(x=270,y=22)

	Label(create_data, text = "Select Stater :", font = ("Arial", 15),bg="#ff80ff").place(x=20,y=70) 
	stater = ttk.Combobox(create_data, width = 18,background="#ff80ff",font=("times new roman",15)) 
	stater['values']=('Masala Papad','Papad','Tomato Soup','Manchow Soup','Manchurian','chai','Coffee','Chinease Noddles')
	stater.place(x=270,y=70)
	stater.current(1)

	stater_no=Entry(create_data,font=("times new roman",15),fg="black",bg="white",width=5,textvariable=stat)
	stater_no.place(x=500,y=70)

	Label(create_data, text = "Select Main Course :", font = ("Arial", 15),bg="#ff80ff").place(x=20,y=120) 
	maincourse = ttk.Combobox(create_data, width = 18,background="#ff80ff",font=("times new roman",15)) 
	maincourse['values']=('Paneer Masala','Mutter Paneer Masala','Paneer Tikka Masala','Paneer Malvani','Aakha Masoor','Mix Vegetarian',
		'Paneer Kadai','Tava Paneer','Dal Fry','Dal Tadaka','kaju Kary','Chicken Masala','Chicken Fry','Chicken Malavani','Butter Chicken','Chicken Kadai','Chicken Handi','Mutton Masala',
		'Mutton Fry','Mutton Malavani','Mutton Handi')
	maincourse.place(x=270,y=120)
	maincourse.current(1)

	maincourse_no=Entry(create_data,font=("times new roman",15),fg="black",bg="white",width=5,textvariable=maico)
	maincourse_no.place(x=500,y=120)

	Label(create_data, text = "Select Roti :", font = ("Arial", 15),bg="#ff80ff").place(x=20,y=170)
	roti = ttk.Combobox(create_data, width = 18,background="#ff80ff",font=("times new roman",15)) 
	roti['values']=('Chapati','Simple Roti','Butter Roti','Nan Roti','Paratha Roti','Bhakari')
	roti.place(x=270,y=170)
	roti.current(1)

	roti_no=Entry(create_data,font=("times new roman",15),fg="black",bg="white",width=5,textvariable=rono)
	roti_no.place(x=500,y=170)

	Label(create_data, text = "Select Rice :", font = ("Arial", 15),bg="#ff80ff").place(x=20,y=220)
	rice = ttk.Combobox(create_data, width = 18,background="#ff80ff",font=("times new roman",15)) 
	rice['values']=('Simple Rice','Jerra Rice','Veg Birayani','Chicken Birayani','Mutton Birayani')
	rice.place(x=270,y=220)
	rice.current(1)

	rice_no=Entry(create_data,font=("times new roman",15),fg="black",bg="white",width=5,textvariable=rino)
	rice_no.place(x=500,y=220)

	Button(create_data,text="Add Items",font=("Arial",15),fg="black",bg="red",width=10,height=1,command=add).place(x=50,y=300)
	Button(create_data,text="Remove Items",font=("Arial",15),fg="black",bg="red",width=15,height=1,command=remove).place(x=200,y=300)
	Button(create_data,text="Show Items",font=("Arial",15),fg="black",bg="red",width=15,height=1,command=showitems).place(x=400,y=300)
	Button(create_data,text="Update Items",font=("Arial",15),fg="black",bg="lightgreen",width=15,height=1,command=update_items).place(x=100,y=400)
	Button(create_data,text="Submit Bill",font=("Arial",15),fg="black",bg="lightgreen",width=15,height=1,command=submit_sucess).place(x=300,y=400)

	show_data = Frame(screen,bg="white")
	show_data.place(x=650,y=10,width=600,height=650)

	style = ttk.Style()
	style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 15)) # Modify the font of the body
	style.configure("mystyle.Treeview.Heading", font=('Calibri', 17,'bold')) # Modify the font of the headings
	style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
	tv = ttk.Treeview(show_data,height=10,style="mystyle.Treeview")
	tv.pack()

	tv["columns"]=("1","2","3")
	tv.column("#0",width=0)
	tv.column("1",width=130)
	tv.column("2",width=250)
	tv.column("3",width=150)
	tv.heading("1", text="Table No")
	tv.heading("2", text="Items")
	tv.heading("3", text="Quantity")

def invalid():
  global invalidscreen
  invalidscreen = Toplevel(login)
  invalidscreen.title("Incomplete")
  invalidscreen.geometry("300x100")
  invalidscreen.resizable(False,False)
  invalidscreen.configure(bg="#ffffcc")
  invalidscreen.iconbitmap('Icon/wrong.ico')
  Label(invalidscreen, text = "Invalid Username Or Password", fg="Red", bg="#ffffcc", font = ("calibri", 13,"bold")).pack()
  Button(invalidscreen, text = "OK", width=10, height=1, command =delete4).pack()

def login_verify():
  
  username1 = username_verify.get()
  password1 = password_verify.get()
  username_entry1.delete(0, END)
  password_entry1.delete(0, END)

  cur.execute('SELECT COUNT(*) FROM collection WHERE Username=(?) AND Password=(?) AND Waiter=(1)',(username1,password1))
  rows=cur.fetchall() 
  if(rows[0][0] == 1):
    waiterscreen()
  else:
    invalid()

def login_verify_admin():
  
  username1 = username_verify.get()
  password1 = password_verify.get()
  username_entry1.delete(0, END)
  password_entry1.delete(0, END)

  cur.execute('SELECT COUNT(*) FROM collection WHERE Username=(?) AND Password=(?)',(username1,password1))
  rows=cur.fetchall() 
  if(rows[0][0] == 1):
    managerscreen()
  else:
    invalid()

def validation():
	global validscreen
	validscreen = Toplevel(regiscreen)
	validscreen.title("Incomplete")
	validscreen.geometry("300x100")
	validscreen.configure(bg="#ffffcc")
	validscreen.resizable(False,False)
	validscreen.iconbitmap('Icon/wrong.ico')
	Label(validscreen, text = "Please Fill Up Below Given Information",fg="Red",bg="#ffffcc", font = ("calibri", 13,"bold")).pack()
	Button(validscreen, text = "OK", width=10, height=1, command =delete5).place(x=100,y=30)

def register_sucess():
	global sucessscreen
	sucessscreen = Toplevel(login)
	sucessscreen.title("Success")
	sucessscreen.geometry("300x100")
	sucessscreen.configure(bg="#ffffcc")
	sucessscreen.resizable(False,False)
	sucessscreen.iconbitmap('Icon/succes.ico') 
	Label(sucessscreen, text = "Registration successful", fg = "#00cc00" ,bg="#ffffcc",font = ("calibri", 15,"bold")).pack()
	Button(sucessscreen, text = "OK", width=10, height=1, command =delete3).place(x=100,y=60)
 

def register_user():
  username_info = username.get()
  password_info = password.get()
  email_info = email.get()
  waiter_info = var1.get()
  match2 = re.search('([\w.-]+)@([\w.-]+)', email_info)
  match1 = re.search(r'[a-zA-z0-9]',username_info)
  match3 = re.search(r'[a-zA-z0-9]',password_info)
  if(match1 and match2 and match3):
  	cur.execute('INSERT OR IGNORE INTO collection (Username,Password,Email,Waiter) VALUES (?,?,?,?)',(username_info,password_info,email_info,waiter_info))
  	conn.commit()
  	username_entry.delete(0, END)
  	password_entry.delete(0, END)
  	email_entry.delete(0,END)
  	var1.set(0)
  	time.sleep(2)
  	regiscreen.destroy()
  	register_sucess()
  else:
  	validation()

def update_data():
  database = r"database1.sqlite"
  conn = sqlite3.connect(database)
  Uusername = username2.get()
  Upassword = password2.get()
  Uemail = email2.get()
  task=(Upassword,Uusername,Uemail)
  Uusername_entry.delete(0, END)
  Upassword_entry.delete(0, END)
  Uemail_entry.delete(0,END)

  sql ='''UPDATE collection SET Password=? WHERE Username=? AND Email=?'''
  cur = conn.cursor()
  cur.execute(sql, task)
  conn.commit()
  updatescreen.destroy()

def update():
  global updatescreen
  global bg2

  updatescreen = Toplevel(login)
  updatescreen.title("Update Data")
  updatescreen.geometry("800x533")
  updatescreen.resizable(False,False)
  updatescreen.iconbitmap('Icon/succes1.ico')

  global username2
  global password2
  global email2
  global Uusername_entry
  global Upassword_entry
  global Uemail_entry

   

  username2 = StringVar()
  password2= StringVar()
  email2 = StringVar()

  bg2=ImageTk.PhotoImage(file="Images/image2.jpg")
  bg2_image=Label(updatescreen,image=bg2).place(x=0,y=0,relwidth=1,relheight=1)
  
  register_frame=Frame(updatescreen,bg="white")
  register_frame.place(x=150,y=100,height=400,width=500)

  Uusername=Label(register_frame, text = "Username * ",font=("Domine",15,"bold"),fg="#001a66",bg="white").place(x=50,y=80)
  Uusername_entry=Entry(register_frame,font=("times new roman",15),bg="#d9d9d9", width=25, textvariable = username2)
  Uusername_entry.place(x=50,y=120)

  Uemail_entry=Label(register_frame,text="Email *",font=("Domine",15,"bold"),fg="#001a66",bg="white").place(x=50,y=150)
  Uemail_entry = Entry(register_frame, font=("times new roman",15),bg="#d9d9d9", width=27, textvariable = email2)
  Uemail_entry.place(x=50,y=190)

  Upassword_entry=Label(register_frame, text = "New Password * ",font=("Domine",15,"bold"),fg="#001a66",bg="white").place(x=50,y=220)
  Upassword_entry =  Entry(register_frame,font=("times new roman",15),bg="#d9d9d9",width=25, show="*",textvariable = password2)
  Upassword_entry.place(x=50,y=260)

  Label(register_frame, text = "")
  Button(updatescreen, text = "Update", font=(15), fg="#000000", bg="#ff0000", width = 10, height = 1, command = update_data).place(x=300,y=400)


def register():
  global regiscreen
  global bg2

  regiscreen = Toplevel(login)
  regiscreen.title("Register Form")
  regiscreen.geometry("800x533")
  regiscreen.resizable(False,False)
  regiscreen.iconbitmap('Icon/succes1.ico')

  global username
  global password
  global email
  global username_entry
  global password_entry
  global email_entry
  global var1

  username = StringVar()
  password = StringVar()
  email = StringVar()
  var1 = IntVar()

  bg2=ImageTk.PhotoImage(file="Images/image2.jpg")
  bg2_image=Label(regiscreen,image=bg2).place(x=0,y=0,relwidth=1,relheight=1)
  
  register_frame=Frame(regiscreen,bg="white")
  register_frame.place(x=150,y=100,height=400,width=500)

  title=Label(register_frame, text = "Please Enter Details Below",font=("Domine",25,"bold"),fg="#ff8000",bg="white").place(x=50,y=20)

  username_entry=Label(register_frame, text = "Username * ",font=("Domine",15,"bold"),fg="#001a66",bg="white").place(x=50,y=80)
  username_entry=Entry(register_frame,font=("times new roman",15),bg="#d9d9d9", width=25, textvariable = username)
  username_entry.place(x=50,y=120)

  email_entry=Label(register_frame,text="Email *",font=("Domine",15,"bold"),fg="#001a66",bg="white").place(x=50,y=150)
  email_entry = Entry(register_frame, font=("times new roman",15),bg="#d9d9d9", width=27, textvariable = email)
  email_entry.place(x=50,y=190)

  password_entry=Label(register_frame, text = "Password * ",font=("Domine",15,"bold"),fg="#001a66",bg="white").place(x=50,y=220)
  password_entry =  Entry(register_frame,font=("times new roman",15),bg="#d9d9d9",width=25, show="*",textvariable = password)
  password_entry.place(x=50,y=260)

  Checkbutton(register_frame, text="Waiter",font=("Domine",15,"bold"),fg="#001a66",bg="white",activebackground="red",variable=var1).place(x=50,y=300)

  Label(register_frame, text = "")
  Button(regiscreen, text = "Register", font=(15), fg="#000000", bg="#ff0000", width = 10, height = 1, command = register_user).place(x=300,y=450)


def login_screen1():
  global username_entry1
  global password_entry1
  global username_verify
  global password_verify
  global bg

  login.geometry("1199x600+100+50")
  login.title("Login Screen")
  login.resizable(False,False)
  login.iconbitmap('Icon/login.ico') 

  username_verify = StringVar()
  password_verify = StringVar()

  #====BG Frame=====
  bg=ImageTk.PhotoImage(file="Images/image.png")
  bg_image=Label(login,image=bg).place(x=0,y=0,relwidth=1,relheight=1)

  #====Login Frame=====
  Frame_login=Frame(login,bg="white")
  Frame_login.place(x=150,y=150,height=420,width=500)

  #====Title Frame===
  title_frame=Frame(login,bg="#00ccff").place(x=0,y=10,width=1199,height=80)
  title_name=Label(title_frame,text="Waiter Login",font=("Domine",35,"bold"),fg="#ff3300",bg="#00ccff").place(x=300,y=20)


  title=Label(Frame_login,text="Login Here",font=("Domine",35,"bold"),fg="#ff3300",bg="white").place(x=90,y=30)
  user=Label(Frame_login,text="Username *",font=("Arial",15,"bold"),fg="#cc0066",bg="white").place(x=90,y=140)
  username_entry1=Entry(Frame_login,font=("times new roman",15),bg="#d9d9d9", textvariable=username_verify)
  username_entry1.place(x=90,y=180)

  passw=Label(Frame_login,text="Password *",font=("Arial",15,"bold"),fg="#cc0066",bg="white").place(x=90,y=220)
  password_entry1=Entry(Frame_login,font=("times new roman",15),bg="#d9d9d9", show="*", textvariable=password_verify)
  password_entry1.place(x=90,y=260)

  login_btn=Label(Frame_login, text = "").pack()
  Button(Frame_login, text = "Login",font=(15), width = 10, height = 1,fg="#000000",bg="#ff0000",command=login_verify).place(x=90,y=320)

def login_screen():
  global username_entry1
  global password_entry1
  global username_verify
  global password_verify
  global bg

  login.geometry("1199x600+100+50")
  login.title("Login Screen")
  login.resizable(False,False)
  login.iconbitmap('Icon/login.ico') 

  username_verify = StringVar()
  password_verify = StringVar()

  #====BG Frame=====
  bg=ImageTk.PhotoImage(file="Images/image.png")
  bg_image=Label(login,image=bg).place(x=0,y=0,relwidth=1,relheight=1)

  #====Login Frame=====
  Frame_login=Frame(login,bg="white")
  Frame_login.place(x=150,y=150,height=420,width=500)

  #====Title Frame===
  title_frame=Frame(login,bg="#00ccff").place(x=0,y=10,width=1199,height=80)
  title_name=Label(title_frame,text="Manager Login",font=("Domine",35,"bold"),fg="#ff3300",bg="#00ccff").place(x=300,y=20)


  title=Label(Frame_login,text="Login Here",font=("Domine",35,"bold"),fg="#ff3300",bg="white").place(x=90,y=30)
  user=Label(Frame_login,text="Username *",font=("Arial",15,"bold"),fg="#cc0066",bg="white").place(x=90,y=140)
  username_entry1=Entry(Frame_login,font=("times new roman",15),bg="#d9d9d9", textvariable=username_verify)
  username_entry1.place(x=90,y=180)

  passw=Label(Frame_login,text="Password *",font=("Arial",15,"bold"),fg="#cc0066",bg="white").place(x=90,y=220)
  password_entry1=Entry(Frame_login,font=("times new roman",15),bg="#d9d9d9", show="*", textvariable=password_verify)
  password_entry1.place(x=90,y=260)

  Button(Frame_login,text="Forgot password?",bg="white",fg="blue",bd=0,font=("times new roman",10),command=update).place(x=90,y=290)

  login_btn=Label(Frame_login, text = "").pack()
  Button(Frame_login, text = "Login",font=(15), width = 10, height = 1,fg="#000000",bg="#ff0000",command=login_verify_admin).place(x=90,y=320)

  register_btn=Button(Frame_login,text="Create Account?",bg="white",fg="#d77337",bd=0,font=("times new roman",15),command=register).place(x=90,y=380)


def main_screen():
	global login

	login = Tk()
	login.geometry("1200x700+80+50")
	login.title("Restaurant Managment System")
	login.resizable(False,False)
	login.iconbitmap('Icon/Restaurant.ico')
	login.configure(bg="#99ccff")

	#===Title===
	title_frame = Frame(login,bg="white").place(x=0,y=5,height=70,width=1200)
	Label(text="Restaurant Managment System",font=("Arial",30,"bold"),fg="black",bg="white").place(x=350,y=15)

	#===Image===
	backg=ImageTk.PhotoImage(file="Images/restra.jpg")
	bg_image=Label(login,image=backg).place(x=200,y=80,width=800,height=400)
	#===Frame==
	login_frame = Frame(login,bg="white").place(x=0,y=500,height=150,width=1200)
	adimage=ImageTk.PhotoImage(file="Images/admin1.jpg")
	empimage=ImageTk.PhotoImage(file="Images/employee1.jpg")

	admin_image=Label(login_frame,image=adimage).place(x=480,y=500,width=100,height=100)
	emplo_image=Label(login_frame,image=empimage).place(x=680,y=500,width=100,height=100)

	Button(login_frame,text="Manager Login",font=("Arial",15),fg="black",bg="red",width=13,height=1,command=login_screen).place(x=440,y=600)
	Button(login_frame,text="Waiter Login",font=("Arial",15),fg="black",bg="red",width=13,height=1,command=login_screen1).place(x=660,y=600)

	login.mainloop()

main_screen()
