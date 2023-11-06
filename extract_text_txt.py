import os
from tqdm.auto import tqdm

# Function to check if a doc_text should be omitted
def should_omit_doc_text(doc_text):
    # Omit if the doc_text is a single word
    if len(doc_text.split()) == 1:
        return True
    # Omit specific phrases
    phrases_to_omit = ["table of contents"]
    for phrase in phrases_to_omit:
        if phrase in doc_text.lower():
            return True
    # Omit image, table, and plot captions
    if any(keyword in doc_text.lower() for keyword in ["image", "table", "plot"]):
        return True
    return False

# Directory path where text files are located

# Get a list of folder names in the specified path

path = '/home/adzlinarifen/ccsstorageaccount2023/deployed/'
folder_names = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]


for file_UUID in tqdm(folder_names):
    input_directory_path = f'/home/adzlinarifen/ccsstorageaccount2023/deployed/{file_UUID}/ocr/'

    for folder, _, files in os.walk(input_directory_path):
        for filename in files:

            if filename == "ocr_dump.txt":
               
                # Extract the UUID from the file path
                uuid = folder.split('/')[-2]  # Assuming the UUID is in the second-to-last part of the path

                # Define the output file path for each folder
                output_file_path = os.path.join()

                



