from tkinter import *
import server
from PIL import Image, ImageTk
import time

class MyFrame(Frame):
	def __init__(self):
		self.root = Tk()
		Frame.__init__(self)
		self.master.title("Server")
		self.master.rowconfigure(7, weight=1)
		self.master.columnconfigure(5, weight=1)
		self.grid(sticky=W+E+N+S)

		status_label = Label(self, text ="Recebendo dados ....")
		status_label.grid(row = 1, column =0, sticky = W)

		self.button = Button(self, text="Start", command=self.receive, width=50)
		self.button.grid(row=0, column=0, sticky=W)


	def receive(self):
		server.main(self)

	def plot_img(self, imagem):
		img = Image.open(imagem)
		photo = ImageTk.PhotoImage(img)
		#PhotoImage(file=r)
		#ImageTk.PhotoImage(img)
		label = Label(self, image = photo)
		label.image = photo
		label.grid(row = 6, column =0, sticky = W)

if __name__ == "__main__":
	MyFrame().mainloop()
