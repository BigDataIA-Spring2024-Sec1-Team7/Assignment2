import os
import xml.etree.ElementTree as ET
from grobid_client.grobid_client import GrobidClient


if __name__ == "__main__":
    client = GrobidClient(config_path="config.json")
    client.process("processFulltextDocument", "../../sourcedata", output="Grobid_op", consolidate_citations=True, tei_coordinates=True, force=True)



def copy_xml_to_txt(xml_folder):
    # Iterate over all XML files in the folder
    for filename in os.listdir(xml_folder):
        if filename.endswith(".xml"):
            xml_file = os.path.join(xml_folder, filename)
            fname = os.path.basename(xml_file)  # Corrected line
            
            year = fname[0:4]
            level = fname[5:7]
            
            # Construct the output text file path
            txt_file = os.path.join(xml_folder, f"Grobid_RR_{year}_{level}_combined.txt")

            # Parse the XML file
            tree = ET.parse(xml_file)
            root = tree.getroot()
  

            # Extract text content from XML elements
            text_content = []
            for element in root.iter():
                if element.text:
                    text_content.append(element.text.strip())

            # Write the text content to a text file
            with open(txt_file, 'w') as f:
                for line in text_content:
                    f.write(line + '\n')


xml_folder = 'Grobid_op'
copy_xml_to_txt(xml_folder)
