from tkinterdnd2 import TkinterDnD, DND_FILES

root = TkinterDnD.Tk()
root.title("TkinterDnD Test")

def on_drop(event):
    print("File dropped:", event.data)

root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", on_drop)

root.mainloop()
