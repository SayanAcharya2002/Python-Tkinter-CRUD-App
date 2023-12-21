from tkinter import *


class tk_table:
  def __init__(self,n,m,headers,root,table_name='Table',padx_each=10,pady_each=5):
    self.holder_frame=LabelFrame(root,padx=(n+2)*pady_each,pady=(m+2)*padx_each)
    self.tab_name=Label(self.holder_frame,text=table_name,font=20)
    self.tab_name.grid(row=0,columnspan=5,pady=10)
    self.entries=[]
    for i in range(n+1):# one extra for headers
      self.entries.append([])
      for j in range(m):
        self.entries[i].append(Entry(self.holder_frame,font=5,borderwidth=2))
        self.entries[i][j].grid(row=i+1,column=j)
    
    for j in range(m):#putting the headers
      self.entries[0][j].delete(0,END)
      self.entries[0][j].insert(0,headers[j])

  def set_entry(self,i,j,val):
    i+=1
    self.entries[i][j].delete(0,END)
    self.entries[i][j].insert(0,val)

  def get_entry(self,i,j):
    i+=1
    return self.entries[i][j].get()

  def pack(self,*args,**kwargs):
    self.holder_frame.pack(args,kwargs)