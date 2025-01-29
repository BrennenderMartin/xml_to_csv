from cx_Freeze import setup, Executable

# Define the base and the executable
executables = [Executable("complete.py")]

# Modify setup to only focus on the executable and not the MSI
setup(
    name="MyApp",
    version="1.0",
    description="My Application",
    executables=executables,
    options={
        "build_exe": {
            "packages": ["os", "sys"],  # Add any necessary packages
            "include_files": ["data.txt", "image.png"],  # Include additional files if needed
        }
    },
)