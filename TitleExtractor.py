import json
import sys
from helper_functions import remove_whitespaces

class TitleExtractor():
    
    def __init__(self):
        pass

    def extract(self, json_obj: json) -> tuple:
        """
        Returns all titles of a given JSON object.

        Parameters:
        json_obj (json): The JSON object where the titles should be extracted.

        Returns:
        tuple: A tuple containing a list of strings of all extracted titles and a list of the upper left coordinates of every title. 
        """
        titles = []
        title_coords = []
        
        # go through every block containing size 17 elements and build together the titles
        for block in json_obj["blocks"]:
            if block["lines"][0]["spans"][0]["size"] == 17:
                title = ""
                for line in block["lines"]:
                    if not "termin" in line["spans"][0]["text"].lower():
                        title = title + line["spans"][0]["text"] + " "
                    else:
                        break
                titles.append(title)
                title_coords.append((block["bbox"][0], block["bbox"][1]))

        # on page 10 there is a subheading -> 3 headings
        if len(titles) == 3:
            titles[1] = titles[1] + titles[2]
            del titles[2]
            del title_coords[2]
            
        titles = remove_whitespaces(titles)

        # when having two courses on one page check if the order is correct
        if len(titles) == 2:
            if title_coords[0][1] > title_coords[1][1]:
                titles = titles[::-1]
                title_coords = title_coords[::-1]

        return titles, title_coords