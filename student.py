

class Student:
  def __init__(self,roll,dept_code,name,address,phone):
    self.roll=int(roll)
    self.dept_code=int(dept_code)
    self.name=name
    self.address=address
    self.phone=phone

  def get_as_str_list(self):
    return [str(self.roll),str(dept_mapping[self.dept_code]),self.name,self.address,self.phone]

  def __str__(self):
    return f"Student(\nroll: {self.roll},\ndept: {dept_mapping[self.dept_code]},\nname: {self.name},\naddress: {self.address},\nphone: {self.phone}\n)"

  def __repr__(self):
    return self.__str__()

dept_mapping={
  0:'cse',
  1:'math',
  2:'phys',
  3:'chem',
  4:'history'
}

rev_dept_mapping=dict(zip(dept_mapping.values(),dept_mapping.keys()))