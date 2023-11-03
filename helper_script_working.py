import os
from tqdm.auto import tqdm

# Directory path where text files are located
input_directory_path = '/home/adzlinarifen/ccsstorageaccount2023/deployed/58f93aa2-fe2f-4657-9030-eef067a70ee4/ocr/'

for folder, _, files in os.walk(input_directory_path):
    for filename in files:
        print(folder)
        if filename.endswith("text.txt"):
            # Extract the UUID from the file path
            uuid = folder.split('/')[-2]  # Assuming the UUID is in the second-to-last part of the path

            # Define the output file path for each folder
            output_file_path = os.path.join(folder, 'ocr_rearrange.txt')

            # Variable to store the maximum page number found
            max_page_number = 0

            # Dictionary to store page numbers and corresponding lines
            page_numbers = {}

            #define doc_text
            doc_text_list={}

            with open(os.path.join(input_directory_path, folder, filename), 'r') as input_file:
                lines = input_file.readlines()
                page_numbers = {}
                max_page_number = -1  # Initialize with a non-negative value

                for line in lines:
                    print(line)

                    if 'page_num' in line:
                        # Extract the page number and remove double-quotes
                        page_num = int(line.split('"page_num": ')[1].split(',')[0].strip('"'))
                        # Check if the line contains "doc_text"
                        if '"doc_text": " in line:
                            doc_text = line.split('"doc_text": "')[1].split('"')[0]
                        else:
                            doc_text = "N/A"  # Handle cases where "doc_text" is not found
                        # Check if the line contains "id"
                        if '"id": "' in line:
                            uuid = line.split('"id": "')[1].split('"')[0]
                        else:
                            uuid = "N/A"  # Handle cases where "id" is not found
                        # Add the information to the page_numbers dictionary
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
                    page_numbers[page_num] = f'{{"extracted_info_params": "{doc_text}", "file_id": "{uuid}", "classification": "text", "page_num": {page_num}}}\n'

            # Sort the page numbers in ascending order
            sorted_page_numbers = sorted(page_numbers.items())

            # Write the sorted lines to the output file

            with open(output_file_path, 'w') as output_file:
                for _, line in sorted_page_numbers:
                    output_file.write(line)

            print(f"Output file with {max_page_number} lines has been written to '{output_file_path}'")