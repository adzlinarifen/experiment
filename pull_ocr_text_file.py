import os
import shutil

source_dir = "/home/adzlinarifen/ccsstorageaccount2023/deployed/"
target_dir = "new_directory"

# Create the target directory if it doesn't exist
if not os.path.exists(target_dir):
    os.mkdir(target_dir)

# Iterate through the source directory
for folder in os.listdir(source_dir):
    folder_path = os.path.join(source_dir, folder)
    
    if os.path.isdir(folder_path):
        # Extract the file_UUID from the folder name
        file_UUID = folder
        
        # Check if the ocr_dump.txt file exists in the folder
        ocr_dump_path = os.path.join(folder_path, "ocr", "ocr_dump.txt")
        if os.path.exists(ocr_dump_path):
            # Copy the ocr_dump.txt file to the new directory with the file_UUID name
            target_file_path = os.path.join(target_dir, f"{file_UUID}_ocr_dump.txt")
            shutil.copy(ocr_dump_path, target_file_path)
