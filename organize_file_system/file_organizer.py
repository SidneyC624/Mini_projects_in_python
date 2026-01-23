import os 
import shutil

path = r"C:\Users\Sidney\Downloads"

extensions = {
    "images": [".jpg", ".png", ".jpeg", ".gif"],
    "videos": [".mp4", ".mkv"],
    "musics": [".mp3", ".wav"],
    "zip": [".zip", ".tgz", ".rar", ".tar"],
    "documents": [".pdf", ".docx", ".csv", ".xlsx", ".pptx", ".doc", ".ppt", ".xls"],
    "setup": [".msi", ".exe"],
    "design": [".xd", ".psd"]
}

def allocate_to_folder(file):
    for folder in list(extensions.keys()):
        for ex in extensions[folder]:
            if file.endswith(ex):
                return folder

try:
    os.chdir(path)
    files = os.listdir()
    for i in range(5):
        allocate_to_folder(files[i])
    
except FileNotFoundError:
    print(f"Directory: {path} does not exist")
except NotADirectoryError:
    print(f"{path} is not a directory")
except PermissionError:
    print(f"You do not have permissions to change to {path}")