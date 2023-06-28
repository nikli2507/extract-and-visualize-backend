class Course():

    def __init__(self, title: str, description: str, target_group: str, content: list,
                  prerequisites: list, dates_location: list, time: str, cost: str,
                  trainer: list, additional_info: str, what_to_bring:str, category: str, 
                  min_age: int, duration: str, duration_as_days: int, dates_locations_list: tuple):
        self.title = title
        self.description = description
        self.target_group = target_group
        self.content = content
        self.prerequisites = prerequisites
        self.dates_location = dates_location
        self.time = time
        self.cost = cost
        self.trainer = trainer
        self.additional_info = additional_info
        self.what_to_bring = what_to_bring
        self.category = category
        self.min_age = min_age
        self.duration = duration
        self.duration_as_days = duration_as_days
        self.dates_locations_list = dates_locations_list
    