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

# attempt to rename file , if opened (aka used by another program), there will be an exception
def is_file_in_use(file_path):
    try:
        os.rename(file_path, file_path)
        return False
    except OSError:
        return True

try:
    os.chdir(path)
    files = os.listdir()
    # to save time instead of iterating all the files
    for i in range(50):
        file_name = files[i]
        # file source path
        full_path = os.path.join(path, file_name)

        if os.path.isdir(full_path):
            continue
        
        if is_file_in_use(full_path):
            print(f"Skipping: {file_name} (File is currently in use)")
            continue

        directory = allocate_to_folder(file_name)

        if directory:
            target_dir = os.path.join(sort_root, directory)
            destination_path = os.path.join(target_dir, file_name)
            # to ensure folder exists before moving file to it
            os.makedirs(target_dir, exist_ok=True)
            # only move to destination if file does not exist
            if not os.path.exists(destination_path):
                shutil.move(file_name, destination_path)
                print(f"Moved: {file_name}")
            else:
                print(f"Skipped: {file_name} (Already exists in {directory})")
        
    
except FileNotFoundError:
    print(f"Directory: {path} does not exist")
except NotADirectoryError:
    print(f"{path} is not a directory")
except PermissionError:
    print(f"You do not have permissions to change to {path}")