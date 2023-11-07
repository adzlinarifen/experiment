import os
from tqdm.auto import tqdm

# Directory path where text files are located
# input_directory_path = '/home/zhah/others/experiment/'

path = '/home/adzlinarifen/ccsstorageaccount2023/deployed/'
folder_names = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]

for file_UUID in tqdm(folder_names):
    input_directory_path = f'/home/adzlinarifen/ccsstorageaccount2023/deployed/{file_UUID}/ocr/'

    for folder, _, files in os.walk(input_directory_path):
        for filename in files:

            if filename == "text.txt":
                # Extract the UUID from the file path
                uuid = folder.split('/')[-2]  # Assuming the UUID is in the second-to-last part of the path

                # Define the output file path for each folder
                output_file_path = os.path.join(folder, 'ocr_rearrange.txt')

                # Variable to store the maximum page number found
                max_page_number = 0

                # Dictionary to store page numbers and corresponding lines
                page_numbers = {}

                with open(os.path.join(input_directory_path, folder, filename), 'r') as input_file:
                    lines = input_file.readlines()
                    page_numbers = {}
                    max_page_number = -1  # Initialize with a non-negative value

                    for line in lines:
                        if 'page_num' in line:
                            # Extract the page number and remove double-quotes
                            page_num = int(line.split('"page_num": ')[1].split(',')[0].strip('"'))

                            doc_texts = []
                            for doc_text in line.split('"doc_text": "')[1:]:
                                doc_texts.append(doc_text.split('"')[0])

                            # Check if the line contains "doc_text"
                            if doc_texts:
                                doc_text = " ".join(doc_texts)
                            else:
                                doc_text = "N/A"  # Handle cases where "doc_text" is not found
                            
                            print(doc_texts)

                            # Add the information to the page_numbers dictionary
                            if page_num in page_numbers:
                                page_numbers[page_num]['extracted_info_params'].append({"par_num": 1, "doc_text": doc_text, "id": uuid})
                            else:
                                page_numbers[page_num] = {
                                    "extracted_info_params": [{"par_num": 1, "doc_text": doc_text, "id": uuid}],
                                    "file_id": uuid,  # Replace with the actual file_id
                                    "classification": "text",
                                    "page_num": page_num
                                }
                            # Update max_page_number if a larger page number is found
                            max_page_number = max(max_page_number, page_num)

                # Ensure that we have lines for all page numbers from 1 to max_page_number
                for page_num in range(1, max_page_number + 1):
                    if page_num not in page_numbers:
                        # If a page number is missing, add an empty line for it
                        page_numbers[page_num] = {
                            "extracted_info_params": [{"par_num": 1, "doc_text": "N/A", "id": uuid}],
                            "file_id": uuid,  # Replace with the actual file_id
                            "classification": "text",
                            "page_num": page_num
                        }

                # Sort the page numbers in ascending order
                sorted_page_numbers = sorted(page_numbers.items())

                # Create a list to store concatenated doc_text values per page
                doc_text_per_page = ["" for _ in range(max_page_number)]

                # Process the lines to extract doc_text values and concatenate them
                for _, line in sorted_page_numbers:
                    if 'extracted_info_params' in line:
                        page_num = line['page_num']
                        doc_texts = [item['doc_text'] for item in line['extracted_info_params']]
                        doc_text_per_page[page_num - 1] = ' '.join(doc_texts)  # Concatenate doc_text values

                # Write the concatenated doc_text values to the output file, separated by page
                with open(output_file_path, 'w') as output_file:
                    for page_num, doc_text in enumerate(doc_text_per_page, start=1):
                        output_file.write(f'{doc_text.strip()}\n\n')
