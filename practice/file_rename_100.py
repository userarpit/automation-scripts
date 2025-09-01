import os


def rename_files_with_suffix(folder_path):
    # Get list of all files in the folder
    files = os.listdir(folder_path)

    count = 1
    for file in files:
        # Skip directories
        if os.path.isfile(os.path.join(folder_path, file)):
            file_name, file_ext = os.path.splitext(file)  # split name and extension
            print(file_name)
            new_name = f"{file_name}_{count}{file_ext}"  # add suffix
            old_path = os.path.join(folder_path, file)
            new_path = os.path.join(folder_path, new_name)

            os.rename(old_path, new_path)
            print(f"Renamed: {file} → {new_name}")
            count += 1


# 👉 Replace with your folder path
rename_files_with_suffix(r"C:\Users\maste\Documents\Arpit\automation-scripts\renamed")
