import json
from helper_functions import remove_whitespaces

class GenericExtractor():

    def __init__(self):
        pass

    def extract(self, json_obj: json, n_courses_on_page: int, keywords: str) -> list:
        """
        Returns all texts below a given keyword (in the PDF representative) of the given JSON object.

        Parameters:
        json_obj (json): The JSON object where the texts should be extracted.
        n_courses_on_page (int): Defines the number of courses in the JSON object.
        keyword (str): Defines the keyword for which should be searched.

        Returns:
        list: A list containing all texts below the given keyword. 
        """
        # get all text of blocks containing the keyword
        result = []
        y_list = []
        for block in json_obj["blocks"]:
            # check if first span of block contains the keyword
            if any(keyword.lower() in block["lines"][0]["spans"][0]["text"].lower() for keyword in keywords):
                subresult = []
                # add all text within the block to the result, excluding the keyword
                for line in block["lines"]:
                    for span in line["spans"]:
                        if not any(keyword.lower() in span["text"].lower() for keyword in keywords) or ":" not in span["text"].lower():
                            subresult.append(span["text"])
                result.append("<br>".join(subresult))
                y_list.append(block["bbox"][1])

        result = remove_whitespaces(result)

        # sort result list and eventually fill with dummy values
        if n_courses_on_page == 2 and len(result) == 1:
            if y_list[0] < 450:
                result.append("")
            else:
                result.insert(0, "")
        elif n_courses_on_page == 2 and len(result) == 2:
            if y_list[0] > y_list[1]:
                result = result[::-1]
        elif len(result) == 0:
            while len(result) != n_courses_on_page:
                result.append("")

        return result