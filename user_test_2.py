import tkinter as tk

def on_option_selected(option):
    # This function is called when an option is selected
    print(f"Selected option: {option}")

root = tk.Tk()
root.title("Dropdown Menu Example")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# List of possible inputs
possible_inputs = ["Option 1", "Option 2", "Option 3", "Option 4"]

# Create a variable to store the selected option
selected_option = tk.StringVar(root)
selected_option.set("Select an option")  # Default value

# Create an OptionMenu
dropdown = tk.OptionMenu(frame, selected_option, *possible_inputs, command=on_option_selected)
dropdown.pack()

root.mainloop()

