import os

def delete_all_files(folder_path):
    # Convert relative path to absolute path
    folder_path = os.path.abspath(folder_path)

    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return

    # Loop through files in folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Only delete files, skip subfolders
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {filename}")

    print("All files deleted successfully!")

# Example usage

# delete_all_files("downloads")
# delete_all_files("trimmed_audios")
# delete_all_files("output")
