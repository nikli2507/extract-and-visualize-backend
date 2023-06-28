import fitz
import re

def remove_whitespaces(str_list: list) -> list:
    
    edited_str_list = []

    # remove leading/following whitespaces and double whitespaces 
    for str in str_list:
        edited_str_list.append(" ".join(str.split()).strip().lstrip("<br>"))

    return edited_str_list

def save_dict_as_file(dictionary: dict, page_n: int):
    with open(f'page{page_n}.json', 'w') as file:
        file.write(str(dictionary))

def save_page_as_file(page_n: int):
    doc = fitz.open("courses.pdf")
    dict = doc[page_n].get_text("dict")
    save_dict_as_file(dict, page_n)

def durations_as_days(durations: list) -> list:
    durations_days = []
    days_conversion = {
        'Tag': 8,
        'Tage': 8,
        'Stunden': 1,
        'Minuten': 1/60
    }
    for duration in durations:
        if duration != "":
            duration = re.sub(r'\(.*?\)|oder.*', '', duration)
            periods = re.findall(r'(\d+(?:,\d+)?)\s*(\w+)', duration)
            
            for period in periods:
                duration = float(period[0].replace(',', '.'))
                unit = period[1]
                
                if unit in days_conversion:
                    hours = duration * days_conversion[unit]
                    days = hours / 8
                    durations_days.append(days)
        else:
            durations_days.append(0.0)

        if len(durations_days) == 0:
            durations_days = [0.0 for _ in range(len(durations))]

    return durations_days        

def remove_text_after_keywords(string, keywords):
    pattern = r'(' + '|'.join(re.escape(keyword) for keyword in keywords) + r')\b(.*)'
    result = re.sub(pattern, r'\1', string, flags=re.IGNORECASE)
    return result.strip()

def contains_date(string):
    date_pattern = r"\d{2}\.\d{2}\.\d{4}" 
    return bool(re.search(date_pattern, string))

def remove_unnecessary_info(string):
    pattern = r'(Modul|Block) \d+:'
    result = re.sub(pattern, "", string)
    return result

def delete_chars_before_number(string):
    match = re.search(r'\d', string)
    if match:
        index = match.start()
        string = string[index:]
    return string

def get_date_location_list(dates_locations):

    result = []

    for dates_location in dates_locations:
        string = remove_unnecessary_info(dates_location)
        string = delete_chars_before_number(string)
        string = remove_text_after_keywords(string, ["dauer", "uhrzeit", "seminarbeitrag", "trainer", "mitzubringen", "zusatzinformation", "hinweis", "mindestalter"])
        
        dates_list = []
        locations_list = []
        
        date_list = []
        for substring in string.split("<br>"):
            if not any(char.isalnum() for char in substring):
                continue
            if contains_date(substring):
                date_list.append(substring.strip())
            elif len(date_list) > 0 and not substring.strip().startswith("von") and not substring.strip()[0].isdigit():
                locations_list.append(substring.strip())
                dates_list.append(date_list)
                date_list = []

        result.append((dates_list, locations_list))

    return result