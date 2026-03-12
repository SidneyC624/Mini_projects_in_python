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

base_dir = os.path.dirname(os.path.realpath(__file__))
sort_root = os.path.join(base_dir, "sorted_downloads")

def allocate_to_folder(file):
    for folder in list(extensions.keys()):
        for ex in extensions[folder]:
            if file.endswith(ex):
                return folder
    return "others"

try:
    os.chdir(path)
    files = os.listdir()
    # to save time instead of iterating all the files
    for i in range(10):
        directory = allocate_to_folder(files[i])

        if directory:
            target_dir = os.path.join(sort_root, directory)
            destination_path = os.path.join(target_dir, files[i])
            # to ensure folder exists before moving file to it
            os.makedirs(target_dir, exist_ok=True)
            # only move to destination if file does not exist
            if not os.path.exists(destination_path):
                shutil.move(files[i], destination_path)
                print(f"Moved: {files[i]}")
            else:
                print(f"Skipped: {files[i]} (Already exists in {directory})")

        # what if file is opened in another program -> need to handle errors
        
    
except FileNotFoundError:
    print(f"Directory: {path} does not exist")
except NotADirectoryError:
    print(f"{path} is not a directory")
except PermissionError:
    print(f"You do not have permissions to change to {path}")