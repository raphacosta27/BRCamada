from tkinter import *
import server

class MyFrame(Frame):
	def __init__(self):
		self.root = Tk()
		Frame.__init__(self)
		self.master.title("Server")
		self.master.rowconfigure(5, weight=1)
		self.master.columnconfigure(5, weight=1)
		self.grid(sticky=W+E+N+S)

		status_label = Label(self, text ="Recebendo dados ....")
		status_label.grid(row = 1, column =0, sticky = W)

		self.button = Button(self, text="Start", command=self.receive, width=50)
		self.button.grid(row=0, column=0, sticky=W)

	def receive(self):
		print("passei por aq")
		server.main()

if __name__ == "__main__":
	MyFrame().mainloop()