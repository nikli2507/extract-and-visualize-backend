from Extractor import Extractor
from CoursesDatabase import *
from helper_functions import *

extractor = Extractor("courses.pdf")
courses = extractor.extract()

# connection to mongodb
database = CoursesDatabase()
database.clean()

for course in courses:
    database.write({
        'title': course.title,
        'description': course.description,
        'target_group': course.target_group,
        'content': course.content,
        'prerequisites': course.prerequisites,
        'dates_location': course.dates_location,
        'time': course.time,
        'cost': course.cost,
        'trainer': course.trainer,
        'additional_info': course.additional_info,
        'what_to_bring': course.what_to_bring,
        'category': course.category,
        'min_age': course.min_age,
        'duration': course.duration
    })

