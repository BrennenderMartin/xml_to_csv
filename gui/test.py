import customtkinter as ctk
from tkinter import filedialog
import shutil

main_folder = "main"
folder_path = f"{main_folder}/input"  # Destination folder for files

class DragDropApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set up the CTk window
        self.title("File Selection Example")
        self.geometry("400x200")

        # Create a frame for file selection
        self.select_frame = ctk.CTkFrame(self, width=300, height=100)
        self.select_frame.pack(pady=50, padx=50)

        # Create a CTkButton for selecting files
        self.select_button = ctk.CTkButton(
            self.select_frame,
            text="Select Files",
            command=self.select_files
        )
        #self.select_button.pack(fill="both", expand=True)
        self.select_button.grid(column=0,row=0, padx=5, pady=5)
        
        self.action_button = ctk.CTkButton(self.select_frame, text="Action", command=self.action)
        self.action_button.grid(column=0,row=1, padx=5, pady=5)
        

    def action():
        print("Action!")
    
    def select_files(self):
        # Open file dialog to select files
        file_paths = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=(("All Files", "*.*"),)
        )
        
        if file_paths:
            for file_path in file_paths:
                print(f"File selected: {file_path}")
                shutil.move(file_path, folder_path)
            print("All files have been moved successfully.")

if __name__ == "__main__":
    app = DragDropApp()
    app.mainloop()
