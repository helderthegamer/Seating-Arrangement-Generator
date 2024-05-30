import tkinter as tk
import customtkinter as CTk
import random

CTk.set_appearance_mode("System")
CTk.set_default_color_theme("blue")

# --- Variables, States, Lists ---
students = []
shuffled_students = []

# --- Functions ---
def generate():
    clear()
    global shuffled_students
    if students:
        shuffled_students = students.copy()
        random.shuffle(shuffled_students)
        amountOfStudents = len(shuffled_students)
        for i in range(amountOfStudents):
            student = shuffled_students[i]
            inputText(f"Seat {i+1}: {student}\n")
            print(shuffled_students)
        writeToFile()
    else:
        clear()
        inputText("No students in the list.")

def clear():
    textBox.configure(state='normal')
    textBox.delete(1.0, tk.END)
    textBox.configure(state='disabled')
    print("\033c", end='')

def changeAppearanceMode(nextAppearance: str):
    CTk.set_appearance_mode(nextAppearance)

def addStudentToList():
    currentEntry = nameEntry.get()
    if currentEntry:
        students.append(currentEntry)
        nameEntry.delete(0, tk.END)
        clear()
        inputText(f"Student name {currentEntry} added\n")
    else:
        clear()
        inputText("Please enter a student name.\n")

def removeStudent():
    currentName = nameEntry.get()
    if currentName in students:
        students.remove(currentName)
        nameEntry.delete(0, tk.END)
        clear()
        inputText(f"Student name {currentName} removed\n")
    else:
        clear()
        inputText(f"Student name {currentName} not found.\n")

def clearStudentsList():
    students.clear()
    clear()
    inputText("Student List cleared")

def inputText(inpText):
    textBox.configure(state='normal')
    textBox.insert(tk.END, inpText)
    textBox.configure(state='disabled')

def close_window():
    root.destroy()

def writeToFile():
    if switchVar.get():
        if shuffled_students:
            with open("seating_arrangement.txt", "w") as file:
                for i in range(len(shuffled_students)):
                    student = shuffled_students[i]
                    file.write(f"Seat {i+1}: {student}\n")
            inputText("\nSeating arrangement has been saved to seating_arrangement.txt\n\n")
        else:
            inputText("No shuffled students available to save. Generate the list first.\n")
    else:
        inputText("No .txt file was created.\n")

def listStudentsInButtonFrame():
    studentsNameField.configure(state='normal')
    studentsNameField.delete(1.0, tk.END)
    for student in students:
        studentsNameField.insert(tk.END, student + '\n')
    studentsNameField.configure(state='disabled')
 
# --- GUI ---

root = CTk.CTk()
root.title("Modern GUI")
root.geometry("1100x580")

root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=1)

sidebarFrame = CTk.CTkFrame(root, width=140, corner_radius=0)
sidebarFrame.grid(row=0, column=0, rowspan=5, sticky="nsew")
sidebarFrame.grid_rowconfigure(6, weight=1)  # Adjusted row index for weight
sidebarFrame.grid_rowconfigure(7, weight=0)  # Added row index for label
sidebarFrame.grid_rowconfigure(8, weight=0)  # Added row index for option menu

logoLabel = CTk.CTkLabel(sidebarFrame, text="Seat Generator", font=CTk.CTkFont(size=20, weight="bold"))
logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

sidebarButton_1 = CTk.CTkButton(sidebarFrame, text="Generate", command=generate)
sidebarButton_1.grid(row=1, column=0, padx=20, pady=10)
sidebarButton_2 = CTk.CTkButton(sidebarFrame, text="Clear List", command=clearStudentsList)
sidebarButton_2.grid(row=2, column=0, padx=20, pady=10)
sidebarButton_3 = CTk.CTkButton(sidebarFrame, text="Quit", command=close_window)
sidebarButton_3.grid(row=3, column=0, padx=20, pady=10)

switchVar = CTk.BooleanVar()
TXTswitch = CTk.CTkSwitch(sidebarFrame, text="Generate .txt file", variable=switchVar)
TXTswitch.grid(row=4, column=0, padx=20, pady=10)

appearanceModeLabel = CTk.CTkLabel(sidebarFrame, text="Appearance Mode:", anchor="w")
appearanceModeLabel.grid(row=7, column=0, padx=20, pady=(10, 0), sticky="s")
appearanceModeOptionemenu = CTk.CTkOptionMenu(sidebarFrame, values=["System", "Light", "Dark"], command=changeAppearanceMode)
appearanceModeOptionemenu.grid(row=8, column=0, padx=20, pady=(10, 10), sticky="s")

nameEntry = CTk.CTkEntry(root, placeholder_text="Add/Remove Student names here:")
nameEntry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

buttonFrame = CTk.CTkFrame(root, width=140, corner_radius=0)
buttonFrame.grid(row=0, column=3, rowspan=5, padx=(20, 0), sticky="nsew")
buttonFrame.grid_rowconfigure(0, weight=1)

studentsNameField = CTk.CTkTextbox(master=buttonFrame, width=100)
studentsNameField.grid(row=0, column=0, padx=(20, 20), pady=(20, 5), sticky="nsew")

buttonFrame.grid_rowconfigure(1, minsize=5)

addStudentBTN = CTk.CTkButton(master=buttonFrame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Add Student", command=lambda: (addStudentToList(), listStudentsInButtonFrame()))
addStudentBTN.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")

removeStudentBTN = CTk.CTkButton(master=buttonFrame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Remove Student", command=lambda: (removeStudent(), listStudentsInButtonFrame()))
removeStudentBTN.grid(row=3, column=0, padx=(20, 20), pady=(5, 20), sticky="ew")

buttonFrame.grid_rowconfigure(2, weight=0)
buttonFrame.grid_rowconfigure(3, weight=0)

textBox = CTk.CTkTextbox(root, width=250, state="disabled")
textBox.grid(row=0, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")

root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()