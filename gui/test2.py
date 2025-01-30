import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.textbox = ctk.CTkTextbox(master=self, width=400, height=200, corner_radius=0)
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.insert("end", "Some example text!\n")

app = App()
app.mainloop()