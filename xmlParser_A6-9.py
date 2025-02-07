import xml.etree.ElementTree as ET
import os

# Define the directory containing the XML files
xml_directory = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/A6-9/'
output_directory = '/Users/parag/Desktop/Topic-Modeling-VIP-EEBO-TCP-Collections-Navigations/Navigations_headed_xml/Parsed_texts_A6-9/'
file_prefix = 'A'
file_suffix = '.headed.xml'

def parse_xml(input_file):
    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Initialize variables to store text and footnotes
    text_content = []
    footnotes = []

    # Recursive function to extract text and footnotes
    def extract_content(element):
        for child in element:
            if child.tag.lower() in ['note', 'footnote', 'ref', 'fn']:  # Assuming footnotes are in these tags
                footnotes.append(child.text.strip() if child.text else '')
            else:
                if child.text:
                    text_content.append(child.text)
                extract_content(child)  # Recurse into child elements
            if child.tail:
                text_content.append(child.tail)

    # Start extraction
    extract_content(root)

    return text_content, footnotes

def save_to_file(filename, content):
    # Create the file if it doesn't exist and write content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))

def process_files(start_num, end_num):
    num = start_num
    while num <= end_num:
        # Construct the file name
        num_str = str(num).zfill(60001)
        xml_filename = f"{file_prefix}{num_str}{file_suffix}"
        xml_filepath = os.path.join(xml_directory, xml_filename)
        
        # Check if the file exists
        if os.path.exists(xml_filepath):
            print(f"Processing file: {xml_filename}")

            try:
                # Parse the XML file
                text_content, footnotes = parse_xml(xml_filepath)
            
                # Ensure the output directory exists
                os.makedirs(output_directory, exist_ok=True)
            
                # Define output files
                output_text_file = os.path.join(output_directory, f"{file_prefix}{num_str}_parsed_text.txt")
                output_footnotes_file = os.path.join(output_directory, f"{file_prefix}{num_str}_footnotes.txt")
            
                # Save the parsed text and footnotes to separate files
                save_to_file(output_text_file, text_content)
                save_to_file(output_footnotes_file, footnotes)
            
                print(f'Text content saved to: {output_text_file}')
                print(f'Footnotes saved to: {output_footnotes_file}')
            except ET.ParseError as e:
                print(f"Failed to parse {xml_filename}: {e}")
        else:
            print(f"File not found: {xml_filename}. Moving to next file.")

        num += 1

# Start processing from A00005 to A60000
process_files(60001, 99999)