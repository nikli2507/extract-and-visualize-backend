import json
from helper_functions import remove_whitespaces

class CategoryExtractor():

    def __init__(self):
        pass

    def extract(self, json_obj: json, n_courses_on_page: int) -> tuple:
        """
        Returns all categories of a given JSON object.

        Parameters:
        json_obj (json): The JSON object where the categories should be extracted.
        n_courses_on_page (int): Defines the amount of categories which can be extracted.

        Returns:
        tuple: A tuple containing a list of strings of all extracted categories and a list of the y position of every category. 
        """

        categories = []
        category_ys = []
        
        # go through every block containing size 12 elements and build together the category names
        for block in json_obj["blocks"]:
            if block["lines"][0]["spans"][0]["size"] == 12:
                category = ""
                for line in block["lines"]:
                    category = category + line["spans"][0]["text"] + " "
                categories.append(category)
                category_ys.append(block["bbox"][1])

        categories = remove_whitespaces(categories)

        # when having two courses on one page check if the order is correct
        if n_courses_on_page == 2:
            if category_ys[0] > category_ys[1]:
                categories = categories[::-1]
                category_ys = category_ys[::-1]

        return categories, category_ys
