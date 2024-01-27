import os, shutil, sys

def get_folders(path: str) -> list[str]:
    """
    Returns directories in a folder

        Parameters:
            path (str): Absolout path of the folder

        Returns:
            list_filtered_directories (list[str]): name of all folder in the folder
    """
    all_paths = os.listdir(path)
    function = lambda p: os.path.isdir(os.path.join(path, p))

    filtered_directories = filter(function, all_paths)
    list_filtered_directories = list(filtered_directories)

    return list_filtered_directories

def get_folder_size(path: str) -> int: 
    """
    Return folder's size
    
    Parameters:
        path (str): Path of the folder

    Returns:
        size (int): Size of the folder
    """

    size = 0
    for path, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    
    return size
    

def checkFolder(folderpath: str) -> None:
    """
    Checks folder is an output of the compiler (obj, or bin)
    Prints size of each folder and the location

    Parameters:
        folderpath (str): Start path of the operation
    """
    global total_size

    # get all sub folders
    all_directories = get_folders(folderpath)

    for folder in all_directories:
        new_path = os.path.join(folderpath, folder)

        # check is folder in the specified directories
        if folder.lower() in ["obj", "bin"]:
            parent = os.path.join(os.path.basename(os.path.dirname(new_path)), folder)
            size = get_folder_size(new_path)/1024/1024
            algin = (35-len(parent))*" " # align for 35 characters
            
            total_size += size

            # do not print if there isn't anything to remove
            if size != 0:
                print(f"{parent} {algin}: {size:.6f}MB")

            # deleting path
            shutil.rmtree(new_path)
            continue
        
        # move to the next folder
        checkFolder(new_path)

    return total_size

def get_cwd():
    """
    Get current working directory (from provided positional argument)
    Returns:
        cwd (str): current working directory
    """
    try:
        cwd: str = sys.argv[1]
        # check does cwd is a 
        if not os.path.isdir(cwd):
            raise FileNotFoundError("Unvalid folder name")

        return cwd
    except:
        print("First argument must be existing folder")
        quit()

def main():
    cwd: str = get_cwd()

    checkFolder(cwd)

    print(f"\nTotal Save: {total_size:.2f}MB\n")

total_size: int = 0

if __name__ == "__main__":
    main()