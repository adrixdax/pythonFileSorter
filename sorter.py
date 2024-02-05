import os
import shutil
import sys

def create_dir(base_path, folder_name):
    directory = os.path.join(base_path, folder_name)
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError:
        print(f"Error creating directory: {directory}")
        return 1
    return 0

def move_file(filename, extension, base_path):
    source_path = os.path.join(base_path, filename)
    destination_dir = os.path.join(base_path, "Ordinati", extension)

    # Create the "Ordinati" folder if it doesn't exist
    create_dir(base_path, "Ordinati")

    try:
        os.makedirs(destination_dir, exist_ok=True)
    except OSError:
        print(f"Error creating directory: {destination_dir}")
        return 1

    if os.path.exists(os.path.join(destination_dir, filename)):
        base_name, file_ext = os.path.splitext(filename)
        count = 1
        new_filename = f"{base_name} ({count}){file_ext}"
        destination_path = os.path.join(destination_dir, new_filename)
        while os.path.exists(destination_path):
            # Append a numeric suffix to the filename
            count += 1
            new_filename = f"{base_name} ({count}){file_ext}"
            destination_path = os.path.join(destination_dir, new_filename)
    else:
        destination_path = os.path.join(destination_dir, filename)

    # Only move the file if it exists in the source path
    if os.path.exists(source_path):
        try:
            shutil.move(source_path, destination_path)
        except OSError:
            print(f"Error moving file: {source_path}")
            return 1
    return 0

def move_folder(folder_name, base_path):
    source_path = os.path.join(base_path, folder_name)
    destination_dir = os.path.join(base_path, "Cartelle")

    # Create the "Directories" folder if it doesn't exist
    create_dir(base_path, "Cartelle")

    try:
        os.makedirs(destination_dir, exist_ok=True)
    except OSError:
        print(f"Error creating directory: {destination_dir}")
        return 1

    if os.path.exists(os.path.join(destination_dir, folder_name)):
        count = 1
        new_folder_name = f"{folder_name} ({count})"
        destination_path = os.path.join(destination_dir, new_folder_name)
        while os.path.exists(destination_path):
            # Append a numeric suffix to the folder name
            count += 1
            new_folder_name = f"{folder_name} ({count})"
            destination_path = os.path.join(destination_dir, new_folder_name)
    else:
        destination_path = os.path.join(destination_dir, folder_name)

    # Only move the folder if it exists in the source path
    if os.path.exists(source_path):
        try:
            shutil.move(source_path, destination_path)
        except OSError:
            print(f"Error moving folder: {source_path}")
            return 1
    return 0

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <working_directory>")
        sys.exit(1)

    base_path = sys.argv[1]

    try:
        extensions = set()
        for filename in os.listdir(base_path):
            if os.path.isfile(os.path.join(base_path, filename)):
                _, ext = os.path.splitext(filename)
                if ext:
                    extensions.add(ext[1:])

        # Create the "Ordinati" folder if it doesn't exist
        create_dir(base_path, "Ordinati")

        for ext in extensions:
            create_dir(os.path.join(base_path, "Ordinati"), ext)  # Create a folder for each extension

            for filename in os.listdir(base_path):
                if os.path.isfile(os.path.join(base_path, filename)):
                    _, file_ext = os.path.splitext(filename)
                    if file_ext == f".{ext}":
                        move_file(filename, ext, base_path)

        # Create the "Directories" folder if it doesn't exist
        create_dir(base_path, "Cartelle")

        for folder_name in os.listdir(base_path):
            if os.path.isdir(os.path.join(base_path, folder_name)) and folder_name != "Ordinati":
                move_folder(folder_name, base_path)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
