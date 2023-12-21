from tkinter import *
from tkinter import messagebox
from tkinter import font as tk_font
import student,table
import sys

db_file="load_db.txt"
if len(sys.argv)>=2:
  db_file=sys.argv[1]

student_dict=dict()

#filling the student array
with open(db_file,'r') as f:
  for i in f.readlines():
    i=i.strip('\r\n').strip('\n').split()
    st=student.Student(i[0],i[1],i[2],' '.join(i[3:-1]),i[-1])
    student_dict[st.roll]=st

root=Tk()
root.geometry('640x640+800+100')
root.title('Database App')


#database_handler_function
def add_student_to_record(roll,dept_code,name,address,phone):
  
  st=student.Student(roll,student.rev_dept_mapping[dept_code],name,address,phone)
  if st.roll in student_dict:
    return False
  else:
    student_dict[st.roll]=st
    return True

def delete_roll_from_db(roll:int):
  if roll in student_dict:
    del student_dict[roll]
    return True
  return False

#controller_buttons

def handle_add_student_message(*args):
  for i in args:
    if len(i)==0:
      messagebox.showerror(title='Error',message='Cant keep fields empty')
      return 
  
  res=messagebox.askokcancel(title='response',message='Sure to add student?(Yes/No)')
  if res:
    ret_val=add_student_to_record(*args)
    if ret_val:
      messagebox.showinfo(title='Success',message='Data Added Successfully')
    else:
      messagebox.showerror(title='Error',message='Student already Exists')


def add_window_func():
  top=Toplevel(root)
  top.geometry('640x640')
  top.title('Add Students')
  labels=[]
  entries=[]
  fields=['roll','name','address','phone']
  opt_menu_var=StringVar(top)
  for i in range(len(fields)):
    cur_label=Label(top,text=fields[i]+':',font=20,padx=20,pady=20)
    cur_label.grid(row=i,column=0,pady=10)
    labels.append(cur_label)
    cur_entry=Entry(top,font=5)
    cur_entry.grid(row=i,column=1,pady=10)
    entries.append(cur_entry)

  opt_label=Label(top,text='dept_names(Select from menu)',font=20,padx=20,pady=20)
  opt_label.grid(row=len(fields),column=0,pady=10)
  opt_menu=OptionMenu(top,opt_menu_var,*list(student.dept_mapping.values()))
  opt_menu_var.set('')
  opt_menu.grid(row=len(fields),column=1,pady=10)
  entries.insert(1,opt_menu_var)

  submit_button=Button(top,text='Submit',command=lambda :handle_add_student_message(*[i.get() for i in entries]),padx=100,pady=20).grid(row=len(fields)+1,columnspan=2,pady=10)

  # exit_button=Button(top,text='Exit',command=top.destroy,padx=100,pady=20).grid(row=len(fields)+2,columnspan=2,pady=10)

def render_table(st_list,table,index:IntVar,forward_button,backward_button):
  for i in range(index.get(),index.get()+5):
    if(i<len(st_list)):
      list_content=st_list[i].get_as_str_list()
    else:
      list_content=['']*5
    for j in range(len(list_content)):
      table.set_entry(i-index.get(),j,list_content[j])
  
  if backward_button is not None:
    if(index.get()==0):
      backward_button.configure(state=DISABLED)
    else:
      backward_button.configure(state=ACTIVE)

  if forward_button is not None:
    if(index.get()+5>=len(st_list)):
      forward_button.configure(state=DISABLED)
    else:
      forward_button.configure(state=ACTIVE)

def display_window_func():
  top=Toplevel(root)
  top.geometry('640x640')
  top.title('Display all Students')

  st_list=list(student_dict.values())
  table_obj=table.tk_table(5,5,['roll','dept_code','name','address','phone'],top,"Students' Table")
  table_obj.holder_frame.pack()
  
  head_index=IntVar()
  head_index.set(0)

  
  forward_button=Button(top,text='Next>>',font=tk_font.Font(size=15))

  forward_button.configure(command=lambda : head_index.set(head_index.get()+5) or render_table(st_list,table_obj,head_index,forward_button,backward_button))
  
  backward_button=Button(top,text='<<Prev',font=tk_font.Font(size=15))
  
  backward_button.configure(command=lambda : head_index.set(head_index.get()-5) or render_table(st_list,table_obj,head_index,forward_button,backward_button))

  render_table(st_list,table_obj,head_index,forward_button,backward_button)

  forward_button.pack()
  backward_button.pack()


def show_roll(roll):
  try:
    roll=int(roll)
    if roll in student_dict:
      messagebox.showinfo(title='Found Student',message=str(student_dict[roll]))
    else:
      messagebox.showerror(title='No Student',message="No such student found")
  except:
    messagebox.showerror(title='Error',message='invalid roll!')
  


def search_window_func():
  top=Toplevel(root)
  top.geometry('640x640')
  top.title('Search Students')

  lab=Label(top,text='Roll no.',font=5)
  ent=Entry(top,font=5)
  
  lab.pack()
  ent.pack()

  but=Button(top,text='Search',font=tk_font.Font(size=20),command=lambda :show_roll(ent.get()))
  but.pack()


def delete_roll_gui(roll):
  try:
    roll=int(roll)
    if delete_roll_from_db(roll):
      messagebox.showinfo(title='Delete successful',message=f'Deleted Roll->{roll}')
    else:
      messagebox.showerror(title='Delete Failed',message='Roll not found')
  except:
    messagebox.showerror(title='Error',message='Invalid Roll')


def delete_window_func():
  top=Toplevel(root)
  top.geometry('640x640')
  top.title('Delete Students')

  lab=Label(top,text='Roll no.',font=5)
  ent=Entry(top,font=5)
  
  lab.pack()
  ent.pack()

  but=Button(top,text='Delete',font=tk_font.Font(size=20),command=lambda :delete_roll_gui(ent.get()))
  but.pack()


def update_as_required(roll,dept,name,address,phone):
  print(roll,dept,name,address,phone)
  try:
    roll=int(roll)
    if roll not in student_dict:
      messagebox.showerror(title='Error',message='No such student exists')
      return 
    st=student_dict[roll]
    
    if dept in student.rev_dept_mapping:
      st.dept_code=student.rev_dept_mapping[dept]
    if len(name)>0:
      st.name=name
    if len(address)>0:
      st.address=address
    if len(phone)>0:
      st.phone=phone

  except Exception as e:
    messagebox.showerror(title='Error',message='Invalid Roll')

def handle_update_student_message(roll,dept,name,address,phone):
  res=messagebox.askokcancel(title='confirmation box',message='sure to proceed?')
  if res:# proceed
    update_as_required(roll,dept,name,address,phone)
  

def update_window_func():
  top=Toplevel(root)
  top.geometry('640x640')
  top.title('Add Students')
  labels=[]
  entries=[]
  fields=['roll','name','address','phone']
  opt_menu_var=StringVar(top)
  for i in range(len(fields)):
    cur_label=Label(top,text=fields[i]+':',font=20,padx=20,pady=20)
    cur_label.grid(row=i,column=0,pady=10)
    labels.append(cur_label)
    cur_entry=Entry(top,font=5)
    cur_entry.grid(row=i,column=1,pady=10)
    entries.append(cur_entry)

  opt_label=Label(top,text='dept_code',font=20,padx=20,pady=20)
  opt_label.grid(row=len(fields),column=0,pady=10)
  opt_menu=OptionMenu(top,opt_menu_var,*list(student.dept_mapping.values()))
  opt_menu_var.set('Select an option')
  opt_menu.grid(row=len(fields),column=1,pady=10)
  entries.insert(1,opt_menu_var)

  submit_button=Button(top,text='Submit',command=lambda :handle_update_student_message(*[i.get() for i in entries]),padx=100,pady=20).grid(row=len(fields)+1,columnspan=2,pady=10)





# main app stuff
add_window_button=Button(root,text='Add Students',font=tk_font.Font(size=20),command=add_window_func,padx=100,pady=10,borderwidth=5)

add_window_button.pack(padx=100,pady=20)

display_window_button=Button(root,text='Display Students',font=tk_font.Font(size=20),command=display_window_func,padx=100,pady=10,borderwidth=5)

display_window_button.pack(padx=100,pady=20)

search_window_button=Button(root,text='Search Students',font=tk_font.Font(size=20),command=search_window_func,padx=100,pady=10,borderwidth=5)

search_window_button.pack(padx=100,pady=20)

delete_window_button=Button(root,text='Delete Students',font=tk_font.Font(size=20),command=delete_window_func,padx=100,pady=10,borderwidth=5)

delete_window_button.pack(padx=100,pady=20)


update_window_button=Button(root,text='Update Students',font=tk_font.Font(size=20),command=update_window_func,padx=100,pady=10,borderwidth=5)

update_window_button.pack(padx=100,pady=20)

root.mainloop()