import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES


class DragDropApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        # Set up the CTk window
        self.title("Drag-and-Drop Button Example")
        self.geometry("400x200")

        # Create a frame for drag-and-drop
        self.drop_frame = ctk.CTkFrame(self, width=300, height=100)
        self.drop_frame.pack(pady=50, padx=50)

        # Create a CTkButton inside the frame
        self.drop_button = ctk.CTkButton(
            self.drop_frame,
            text="Drop Files Here",
            command=self.on_button_click
        )
        self.drop_button.pack(fill="both", expand=True)

        # Enable drag-and-drop for the frame
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind("<<Drop>>", self.on_file_drop)

    def on_button_click(self):
        print("Button clicked!")

    def on_file_drop(self, event):
        file_paths = event.data.split()  # File paths separated by spaces
        for file_path in file_paths:
            print(f"File dropped: {file_path}")


if __name__ == "__main__":
    app = DragDropApp()
    app.mainloop()
