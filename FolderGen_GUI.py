import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox, ttk

THEME_COLOR = "#22262a" #dark
#THEME_COLOR = "#303841" #azul
opciones = ["fx", "lightning", "comp", "layout","modeling","animation","lookdev","pipeline"]

class PathGenInterface:
	def __init__(self):
		self.window = Tk()
		self.window.title("Project Folder Generator v0.01")
		self.window.config(bg=THEME_COLOR)
		self.window.resizable(False,False)

		#Tema ttk
		style = ttk.Style()
		style.theme_use('alt')

		#Attributes
		self.opened_dir = None
		self.proyecto = "No project selected"
		self.sequences = None
		self.shots = None
		self.seq_path = None
		self.shot_path = None

		#Project Set
		self.label_proyecto = Label(text="Project:", bg=THEME_COLOR, fg="white")
		self.label_proyecto.grid(row=0, column=0,  padx=10, pady=5, sticky="e")

		self.input_proyecto = Label(text=self.proyecto, bg=THEME_COLOR, fg="white", font={"Helvetica",12,"bold"})
		self.input_proyecto.grid(row=0,column=1,padx=30,pady=5)

		self.button_setproject = Button(text="Set Project", command=self.openDirectory)
		self.button_setproject.grid(row=0,column=2,padx="2",sticky="e")

		self.separator1 = Frame(height=2,bd=1,relief=RAISED)
		self.separator1.grid(row=1,column=0, columnspan="4", sticky=W+E)

		#Sequence tab
		self.label_sequence = Label(text="Sequence:",bg=THEME_COLOR, fg="white" )
		self.label_sequence.grid(row=2,column=0,padx=10,pady=5,sticky="e")

		self.dropdown_seq = ttk.Combobox()
		self.dropdown_seq.grid(row=2,column=1)

		self.button_addseq = Button(text="Add", command=self.addFolderSeq)
		self.button_addseq.grid(row=2,column=2,padx=2,sticky="e")

		self.button_removeseq = Button(text="Remove", bg="#775553", command=self.removeConfirmationSeq)
		self.button_removeseq.grid(row=2,column=3)

		#Shot tab
		self.label_shot = Label(text="Shot:", bg=THEME_COLOR, fg="white")
		self.label_shot.grid(row=3,column=0,padx=10,pady=5,sticky="e")

		self.dropdown_shot = ttk.Combobox()
		self.dropdown_shot.grid(row=3,column=1)

		self.button_addshot = Button(text="Add", command=self.addFolderShot)
		self.button_addshot.grid(row=3,column=2,padx=2,sticky="e")

		self.button_removeshot = Button(text="Remove", bg="#775553", command=self.removeConfirmationShot)
		self.button_removeshot.grid(row=3,column=3)

		self.separator2 = Frame(height=2,bd=1,relief=RAISED)
		self.separator2.grid(row=4,column=0, columnspan="4", sticky=W+E)

		#Bind comboboxes
		self.dropdown_seq.bind("<<ComboboxSelected>>",self.updateShot)
		self.dropdown_shot.bind("<<ComboboxSelected>>",self.updateShotSelected)

		#Create Frame
		self.folders_frame = LabelFrame(text="Folders",bg=THEME_COLOR, fg="white")
		self.folders_frame.grid(row=5,column=0, padx=5, sticky="nsew",rowspan=3,columnspan=4)

		#Checkboxes
		self.vars = []
		for _ in opciones:
			var = BooleanVar()
			self.vars.append(var)

		aux = -1
		row = 0

		# Custom style for Checkbutton
		#style.configure("Custom.TCheckbutton", background="black", foreground="white")

		for i, opcion in enumerate(opciones):
			if i%3 == 0:
				aux += 1
				row = 0
			Checkbutton(self.folders_frame,text=opcion, variable=self.vars[i],fg="white", bg=THEME_COLOR,activebackground=THEME_COLOR,activeforeground='white',selectcolor=THEME_COLOR).grid(row=5+row, column=0+aux,sticky="w")
			row += 1


		self.button_gen = Button(text="Generate folders", command=self.generateFolders)
		self.button_gen.grid(row=9,column=0, pady=5,columnspan=4)

		#Execute Loop
		self.window.mainloop()








	#Method to update shots when a sequence is selected
	def updateShot(self,event=None):
		self.seq_path =  os.path.join(self.opened_dir,self.dropdown_seq.get())
		self.dropdown_shot['values'] = self.checkFolders(self.seq_path)

	#Method to update the shot path when selected from the dropdown menu
	def updateShotSelected(self,event=None):
		self.shot_path = os.path.join(self.seq_path,self.dropdown_shot.get())

	#Method to update sequence dropwdown when a sequence is added or deleted
	def updateSeq(self):
		self.seq_path = self.opened_dir
		self.dropdown_seq['values'] = self.checkFolders(self.seq_path)

	#Method to select the Project Folder. First it sets the directory path and then load the sequence folders
	def openDirectory(self):
		self.opened_dir = filedialog.askdirectory()
		self.proyecto = self.opened_dir.split("/")[-1]
		self.input_proyecto.config(text=self.proyecto)
		self.sequences = self.checkFolders(self.opened_dir)
		self.dropdown_seq['values'] = self.sequences

	#Method to check the folders inside a directory and return a list
	def checkFolders(self,directory):
		if os.path.exists(self.opened_dir):
			return [file for file in os.listdir(directory) if os.path.isdir(os.path.join(directory,file))]
		else:
			return None

	#Method to add a new sequence into the project folder
	def addFolderSeq(self):
		if self.opened_dir is None or not os.path.exists(self.opened_dir):
			messagebox.showinfo("No project selected!", "Please, open an existent project.")
			return
		else:
			new_seq = self.dropdown_seq.get()
			if new_seq == "":
				print("No sequence name provided")
			else:
				new_path = os.path.join(self.opened_dir,new_seq)
				if os.path.exists(new_path):
					print("Sequence already exists.")
				else:
					os.makedirs(new_path)
					messagebox.showinfo("Sequence added!", f"New sequence {new_seq} created, SET PROJECT AGAIN")
					self.updateSeq()



	#Method to add a new shot into the project folder
	def addFolderShot(self):
		if self.seq_path is None or not os.path.exists(self.seq_path):
			messagebox.showinfo("No project selected!", "Please, open an existent project.")
			return
		else:
			new_shot = self.dropdown_shot.get()
			if new_shot == "":
				print("No shot name provided")
			else:
				new_path = os.path.join(self.seq_path,new_shot)
				if os.path.exists(new_path):
					print("Shot already exists.")
				else:
					os.makedirs(new_path)
					messagebox.showinfo("Shot added!", f"New shot {new_shot} created.")
					self.updateShot()


	#Method wich shows a confirmation message. Calls removeFolder() if accepted.
	def removeConfirmationSeq(self):
		respuesta = messagebox.askquestion("Are you sure?","You are deleting the folder and everything it contains.")
		if respuesta == 'yes':
			self.removeFolderSeq()

	def removeConfirmationShot(self):
		respuesta = messagebox.askquestion("Are you sure?","You are deleting the folder and everything it contains.")
		if respuesta == 'yes':
			self.removeFolderShot()

	#Method which removes a sequence or a shot. Dangerous to have it here.
	def removeFolderSeq(self):
		try:
			#shutil.rmtree(self.seq_path)
			os.rmdir(self.seq_path)
			self.updateSeq()
			messagebox.showinfo("Sequence deleted!", f"Sequence deleted.")

		except OSError as e:
			print(f"Error, can't delete folder")

	def removeFolderShot(self):
		try:
			#shutil.rmtree(self.seq_path)
			os.rmdir(self.shot_path)
			self.updateShot()
			messagebox.showinfo("Shot deleted!", f"Shot deleted.")

		except OSError as e:
			print(f"Error, can't delete folder")

	#Method to generate the folders selected. If its already created, do nothing
	def generateFolders(self):
		if self.shot_path is None or not os.path.exists(self.shot_path):
			print("No path found.")
			return
		else:
			for i, var in enumerate(self.vars):
				if var.get():
					new_path = os.path.join(self.shot_path,opciones[i])
					if os.path.exists(new_path):
						print(f"Folder {opciones[i]}, already exists in directory.")
					else:
						os.makedirs(new_path)
						print(f"Folder {opciones[i]} created.")
		print("All folders created.")

if __name__ == "__main__":
	ui = PathGenInterface()