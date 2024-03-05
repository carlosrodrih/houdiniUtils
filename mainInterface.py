from tkinter import *
from tkinter import filedialog
import zipfile
import os
import sys
import glob
import pandas as pd 
from unzipUtils import UnzipUtils

THEME_COLOR = "#444666"

class FolderInterface:
	def __init__(self):
		self.window = Tk()
		self.window.title("holaaaa")
		self.window.config(padx=20,pady=20,bg=THEME_COLOR)

		self.opened_dir = None
		self.zip_files = None

		self.folder_name_label = Label(text="Select Folder: ",bg=THEME_COLOR, fg="white")
		self.folder_name_label.grid(row=0,column=1)

		#Open button
		self.open_button_image = PhotoImage(file="images/open_button.png")
		self.openDir_button = Button(bg=THEME_COLOR, image=self.open_button_image, bd=0, highlightbackground=THEME_COLOR, highlightthickness=0, command=self.openDirectory)
		self.openDir_button.grid(row=1,column=1)

		#Central Canvas
		self.central_canvas = Canvas(width=200,height=200,highlightthickness=0,bg="white")
		self.central_text = self.central_canvas.create_text(150,75,width=200,text="",fill="#000000",font=("Arial",20,"italic"))
		self.central_canvas.grid(row = 2, column = 0, columnspan=3, pady=50)

		#Unzip button
		self.unzip_button_image = PhotoImage(file="images/unzip_button.png")
		self.unzip_button = Button(image=self.unzip_button_image, bd=0, highlightbackground=THEME_COLOR, highlightthickness=0, command=self.unzipAllButton)
		self.unzip_button.grid(row = 5, column = 1)


		#CSV button
		self.csv_button_image = PhotoImage(file="images/csv_button.png")
		self.csv_button = Button(image=self.csv_button_image, bd=0, highlightbackground=THEME_COLOR, highlightthickness=0, command=self.exportCSVButton)
		self.csv_button.grid(row = 6, column = 1)

		#Delete button
		self.del_button_image = PhotoImage(file="images/del_button.png")
		self.del_button = Button(image=self.del_button_image, bd=0, highlightbackground=THEME_COLOR, highlightthickness=0, command=self.deleteZipsButton)
		self.del_button.grid(row = 7, column = 1)

		self.window.mainloop()


	#Open directory function
	def openDirectory(self):
		self.opened_dir = filedialog.askdirectory()
		self.zip_files = [file for file in os.listdir(self.opened_dir) if file.endswith(".zip")]
		self.central_canvas.itemconfig(self.central_text,text=f"{len(self.zip_files)} zip files found in: {self.opened_dir}")

	#Creates an instance of the UnzipUtils and call the unzipAll method. Unzips all the .zip in the folder.
	def unzipAllButton(self):
		zip1 = UnzipUtils(self.opened_dir)
		zip1.unzipAll()


	#Delete Zip files in the open directory
	def deleteZipsButton(self):
		#zip2 = UnzipUtils(self.opened_dir)
		#zip1.deleteZipFiles()
		#or
		for zfile in self.zip_files:
			#os.remove(self.opened_dir + "/" + zfile)
			print("Done removing files")

	def exportCSVButton(self):
		dirpath = self.opened_dir
		fbx_files = []

		for x in os.walk(dirpath):
			for y in glob.glob(os.path.join(x[0],"*.fbx")):
				fbx_files.append(y)

		h = {"fbx_files": fbx_files}

		df = pd.DataFrame(h)
		df.to_csv("file_list.csv")
		data = pd.read_csv("file_list.csv")
		print(data)

if __name__ == "__main__":
	ui = FolderInterface()