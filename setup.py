import os
import shutil
import main
import gui


os.makedirs("main", exist_ok=True)
os.makedirs(f"main/{main.folder_path}")
os.makedirs(f"main/{main.output_folder}")
os.makedirs(f"main/{main.processed_folder}")

shutil.copy("gui.py", "main")
shutil.copy("main.py", "main")
shutil.copy("setup.py", "main")

app = gui.DragDropApp()
app.mainloop()