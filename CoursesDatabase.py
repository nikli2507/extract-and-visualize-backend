from pymongo import MongoClient

class  CoursesDatabase():
    """
    Serves as interface to the MongoDB database.
    Creates the connection on creation of the object.
    """

    def __init__(self):
        self.__client = MongoClient("mongodb+srv://admin:nrFwOGC8T62BeKfC@cluster0.7esbysh.mongodb.net/?retryWrites=true&w=majority")
        self.__database = self.__client['courses_db']
        self.__courses_collection = self.__database["courses"]

    def write(self, content: dict):
        """
        Writes a given dictionary to the database.

        Parameters:
        dict: The dictionary/JSON which shall be written to the database.
        """
        self.__courses_collection.insert_one(content)

    def query_all_courses(self) -> list:
        """
        Queries all entries from the database.

        Returns:
        list: List of all courses as JSON.
        """
        return list(self.__courses_collection.find())
    
    def clean(self):
        """
        Deletes all entries in the database.
        """
        self.__courses_collection.delete_many({})