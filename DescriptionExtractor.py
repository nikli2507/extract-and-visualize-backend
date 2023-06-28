import json
from helper_functions import remove_whitespaces

class DescriptionExtractor():

    MAX_Y_DIFFERENCE = 400
    X_THRESHOLD = 3
    KEYWORDS = ["zielgruppe", "inhalt", "voraussetzung", "zusatzinformation", "dauer", "uhrzeit", "seminarbeitrag", "trainer", "mitzubringen"]

    def __init__(self):
        pass

    def extract(self, json_obj: json, title_coords: list) -> list:
        """
        Returns all descriptions of a given JSON object.

        Parameters:
        json_obj (json): The JSON object where the descriptions should be extracted.
        title_coords (list): List of the coordinate tuples of the titles

        Returns:
        list: A list containing all descriptions. 
        """
        # extract description for every title
        descriptions = []
        for title_x, title_y in title_coords:
            description = ""
            # get all texts in the json objects
            for block in json_obj["blocks"]:
                block_x = block["lines"][0]["spans"][0]["origin"][0]  # there is one case where the bbox x coordinate is wrong -> take span origin
                block_y = block["bbox"][1]
                text = block["lines"][0]["spans"][0]["text"].lower()
                # check if current block is on the same x and below the title, but not further than MAX_Y_DIFFERENCE 
                # (relevant for more courses on one page) and check if text is really a description with the keywords
                if abs(block_x-title_x) < self.X_THRESHOLD and block_y > title_y and \
                   not any(keyword in text for keyword in self.KEYWORDS) and abs(block_y-title_y) < self.MAX_Y_DIFFERENCE:
                    for line in block['lines']:
                        for span in line['spans']:
                            description = description + span['text']
            descriptions.append(description)

        descriptions = remove_whitespaces(descriptions)

        return descriptions
    
