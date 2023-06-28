import json
import sys

class DatesLocationExtractor():

    KEYWORDS = ["dauer", "uhrzeit", "seminarbeitrag", "trainer", "mitzubringen", "zusatzinformation", "hinweis", "mindestalter"]

    def __init__(self):
        pass

    def extract(self, json_obj: json, n_courses_on_page: int, category_ys: list) -> list:
        """
        Returns all date/location strings of a given JSON object.

        Parameters:
        json_obj (json): The JSON object where the dates and locations should be extracted.
        n_courses_on_page (int): Defines the amount of date/location strings which can be extracted.
        category_ys (list): Defines where the categories are located on the y axis.

        Returns:
        list: A list containing all date/location strings. 
        """

        category1_y = category_ys[0]
        # if only one category exists on one page the y of the second category is set to plus infinite
        category2_y = category_ys[1] if n_courses_on_page == 2 else sys.float_info.max  

        # split all blocks into two sections for every single course, the categories y coordinate is a good point to split
        # TODO: check if this is also possible with the titles y coordinate
        cat1_blocks = [block for block in json_obj["blocks"] if block["bbox"][1] > category1_y and block["bbox"][1] < category2_y]
        cat2_blocks = [block for block in json_obj["blocks"] if block["bbox"][1] > category2_y]

        dates_locations = []

        for blocks in [cat1_blocks, cat2_blocks]:
            
            # determine where the section of all dates and locations begins
            dates_x = 0
            dates_y = 0
            for block in blocks:
                if "termin" in block["lines"][0]["spans"][0]["text"].lower():
                    dates_x = block["bbox"][0]
                    dates_y = block["bbox"][1]
                    break
            
            # get date/location strings
            subresult = []
            for block in blocks:
                text = block["lines"][0]["spans"][0]["text"].lower()
                # check if the found text is at the same x and below the "Termine" heading or is part of another text section (e.g. "Uhrzeit")
                if (block["bbox"][0] == dates_x) and (block["bbox"][1] >= dates_y) and not any(keyword in text for keyword in self.KEYWORDS):
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if "termin" not in span["text"].lower():
                                subresult.append(span["text"])
            if subresult != []:
                subresult = "<br>".join(subresult)
                dates_locations.append(subresult)
                    
        # fill result list with empty entries if some date/location string was not found            
        if len(dates_locations) < n_courses_on_page:
            if cat1_blocks == []:
                dates_locations.insert(0, "")
            elif cat2_blocks == []:
                dates_locations.append("")

        return dates_locations