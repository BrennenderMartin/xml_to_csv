import customtkinter as ctk

class CTkConsole(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("CTk Console")
        self.geometry("600x400")

        # Create a text widget for console output
        self.console_output = ctk.CTkTextbox(self, width=580, height=300)
        self.console_output.pack(pady=10, padx=10)

        # Create an entry widget for user input
        self.input_entry = ctk.CTkEntry(self, placeholder_text="Type your command here...")
        self.input_entry.pack(fill="x", padx=10, pady=(0, 10))
        self.input_entry.bind("<Return>", self.handle_command)  # Bind Enter key

        # Create a button to submit commands
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.handle_command)
        self.submit_button.pack(pady=5)

    def handle_command(self, event=None):
        # Get the input text
        command = self.input_entry.get()

        if command.strip():  # If input is not empty
            # Display the command in the console
            self.console_output.insert("end", f"User: {command}\n")
            self.console_output.see("end")  # Scroll to the bottom
            self.input_entry.delete(0, "end")  # Clear the input entry

            # Example: Handle some commands
            if command.lower() == "hello":
                self.console_output.insert("end", "Console: Hi there!\n")
            elif command.lower() == "exit":
                self.console_output.insert("end", "Console: Goodbye!\n")
                self.quit()  # Exit the application
            else:
                self.console_output.insert("end", f"Console: Unknown command '{command}'\n")
            self.console_output.see("end")  # Scroll to the bottom


if __name__ == "__main__":
    app = CTkConsole()
    app.mainloop()
