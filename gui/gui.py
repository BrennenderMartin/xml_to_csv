import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("gui")
        self.geometry("400x400")

if __name__ == "__main__":
    app = App()
    app.mainloop()
