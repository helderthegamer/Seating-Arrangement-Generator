import random
import tkinter as tk

entry_listNames = []
entry_frame = None  # Define entry_frame as a global variable
entry_canvas = None
entry_listNames = []
scrollbar = None
listNames = {}
listNamesKeys = []

# --- Functions ---

def generateSeatingArrangement(listNamesKeys):
    arrangement = ""
    for index, key in enumerate(listNamesKeys, start=1):
        name = listNames.get(key, "Unknown")  # Get the name from listNames or use "Unknown" if not found
        arrangement += "Seat {}: {}\n".format(index, name)
    return arrangement

def writeToFile(listNamesKeys):
    if CheckBtnState.get():
        with open("seating_arrangement.txt", "w") as file:
            for index, key in enumerate(listNamesKeys, start=1):
                file.write("Seat {}: {}\n".format(index, listNames[key]))
        output_text.insert(tk.END, "\nSeating arrangement has been saved to seating_arrangement.txt\n\n")
    else:
        output_text.insert(tk.END, "No .txt file was created.")

def generate_and_write():
    global listNames
    for i, entry in enumerate(entry_listNames, start=1):
        name = entry.get().strip()
        if name:
            listNames[i] = name
        else:
            listNames[i] = "Unknown"

    random.shuffle(listNamesKeys)
    arrangement = generateSeatingArrangement(listNamesKeys)
    output_text.delete(1.0, tk.END)  # Clear the output text widget
    output_text.insert(tk.END, arrangement)
    writeToFile(listNamesKeys)

def get_number_of_students():
    global listNames, listNamesKeys, entry_frame, entry_listNames
    
    # Destroy existing frame containing entry fields
    if entry_frame:
        entry_frame.destroy()
    
    if input_field.get().strip().isdigit():
        ns = int(input_field.get())
        create_name_entry_widgets(ns)
        output_text.insert(tk.END, "Please input the names of the students.\n")
        listNames = {}  # Reset the dictionary
        for i in range(1, ns + 1):
            listNames[i] = ''  # Initialize names with empty strings
        listNamesKeys = list(listNames.keys())  # Populate listNamesKeys with indices
    else:
        output_text.insert(tk.END, "Error: Please enter a valid number of students.\n")

def create_name_entry_widgets(num_students):
    global entry_canvas, entry_listNames, scrollbar
    if entry_canvas:  # If canvas already exists, clear its contents
        entry_canvas.destroy()
        scrollbar.destroy()

    entry_listNames = []
    
    # Create a canvas to contain all entry fields
    entry_canvas = tk.Canvas(root)
    entry_canvas.pack(side=tk.LEFT, fill=tk.Y)  # Pack the canvas to the left and allow vertical scrolling
    
    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=entry_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    entry_canvas.config(yscrollcommand=scrollbar.set)
    
    # Create a frame inside the canvas to hold the entry fields
    entry_frame = tk.Frame(entry_canvas)
    entry_canvas.create_window((0, 0), window=entry_frame, anchor=tk.NW)
    
    # Bind canvas scrolling to mousewheel
    entry_canvas.bind_all("<MouseWheel>", lambda event: entry_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    for i in range(num_students):
        entry_label = tk.Label(entry_frame, text=f"{i+1}.", width=3)
        entry_label.grid(row=i, column=0, sticky=tk.E)  # Place labels on the left side
        name_entry = tk.Entry(entry_frame)
        name_entry.grid(row=i, column=1, sticky=tk.W)  # Place entries on the right side
        entry_listNames.append(name_entry)

    # Update the scroll region of the canvas
    entry_frame.update_idletasks()
    entry_canvas.config(scrollregion=entry_canvas.bbox("all"))

def close_window():
    global running
    running = False
    root.destroy()

# --- Main code ---
root = tk.Tk()
root.title("Seating Arrangement")

# Input field for number of students
input_label = tk.Label(root, text="Number of Students:")
input_label.pack()
input_field = tk.Entry(root)
input_field.pack()

# Button to get number of students
get_students_button = tk.Button(root, text="Get Students", command=get_number_of_students)
get_students_button.pack()

# Output text field for seating arrangement
output_label = tk.Label(root, text="Seating Arrangement:")
output_label.pack()
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

# Button to generate seating arrangement and write to file
generate_button = tk.Button(root, text="Generate Seating Arrangement", command=generate_and_write)
generate_button.pack(pady=2.5)  # Add padding between the button and other widgets

#Generate txt checkbox
CheckBtnState = tk.BooleanVar()

checkBtn = tk.Checkbutton(root, text="Generate .txt file", variable=CheckBtnState)
checkBtn.pack()

# Button to close the GUI window
close_button = tk.Button(root, text="Close", command=close_window)
close_button.pack(pady=2.5)

# Bind the close_window function to the window's close event
root.protocol("WM_DELETE_WINDOW", close_window)

running = True
while running:
    try:
        root.update()
    except tk.TclError:
        break
    