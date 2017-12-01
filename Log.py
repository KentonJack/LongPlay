from tkinter import *
from tkinter.messagebox import *


class Login(object):
	def __init__(self):
		self.root = Tk()
		self.root.title(u'reg')
		self.root.resizable(False, False)
		self.root.geometry('+450+250')
		self.lb_user = Label(self.root, text=u'Username：', padx=5)
		self.lb_passwd = Label(self.root, text=u'Password：', padx=5)
		self.lb_user.grid(row=0, column=0, sticky=W)
		self.lb_passwd.grid(row=1, column=0, sticky=W)
		self.en_user = Entry(self.root, width=18)
		self.en_passwd = Entry(self.root, width=18)
		self.en_user.grid(row=0, column=1, columnspan=2)
		self.en_passwd.grid(row=1, column=1, columnspan=2)
		self.en_user.insert(0, u'Input username')
		self.en_passwd.insert(0, u'Input password')
		self.en_user.config(validate='focusin', validatecommand=lambda: self.validate_func('self.en_user'), invalidcommand=lambda: self.invalid_func('self.en_user'))
		self.en_passwd.config(validate='focusin', validatecommand=lambda: self.validate_func('self.en_passwd'), invalidcommand=lambda: self.invalid_func('self.en_passwd'))
		self.var = IntVar()
		self.bt_print = Button(self.root, text=u'Submit')
		self.bt_print.grid(row=2, column=2, sticky=E, pady=5)
		self.bt_print.config(command=self.print_info)
		self.root.bind('<Return>', self.enter_print)
		self.root.mainloop()

	@staticmethod
	def validate_func(self, en):
		return False if eval(en).get().strip() != '' else True

	@staticmethod
	def invalid_func(self, en):
		value = eval(en).get().strip()
		if value == u'Input username' or value == u'Input password':
			eval(en).delete(0, END)
		if en == 'self.en_passwd':
			eval(en).config(show='*')

	def print_info(self):
		en1_value = self.en_user.get().strip()
		en2_value = self.en_passwd.get().strip()
		if en1_value == '' or en1_value == u'Input username':
			showwarning(u'No username', u'Please input username')
		elif en2_value == '' or en2_value == u'Input password':
			showwarning(u'No password', u'Please input password')
		else:
			showinfo('Successful')

	def enter_print(self, event):
		self.print_info()


if __name__ == "__main__":
	Login()
