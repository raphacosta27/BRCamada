from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror


class MyFrame(Frame):
	def __init__(self):
		self.filename = ""
		Frame.__init__(self)
		self.master.title("Client_Server")
		self.master.rowconfigure(5, weight=1)
		self.master.columnconfigure(5, weight=1)
		self.grid(sticky=W+E+N+S)

		self.label = Label(self, text = "No file")
		self.label.grid(row=0, column=0, sticky=W)

		self.button = Button(self, text="Browse", command=self.load_file, width=10)
		self.button.grid(row=2, column=0, sticky=W)

		self.button_send = Button(self, text="Send", width=10)
		self.button_send.grid(row=2, column=1, sticky=W)

	def load_file(self):
		fname = askopenfilename()
		if fname:
			try:
				self.filename = fname
				print("""here it comes: self.settings["template"].set(fname)""")
				self.label.config(text=str(self.filename))	
				print(self.filename	)
			except:  
				showerror("Open Source File", "Failed to read file\n'%s'" % fname)
			return


if __name__ == "__main__":
	MyFrame().mainloop()