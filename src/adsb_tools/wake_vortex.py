import csv
import os


class WakeVortexCategories:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._categories = {}
            cls._instance._category_dict = {}
            cls._instance._parse_csv()
        return cls._instance

    @property
    def categories(self):
        return self._categories

    def get_category_dict(self, category):
        return self._category_dict.get(category.lower())

    def _parse_csv(self):
        # get the directory of the current script (foo.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # construct the path to the csv file
        csv_file_path = os.path.join(current_dir, 'static', 'wake_vortex_categories.csv')
        print(csv_file_path)
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                category = row['Category']
                tc = row['TC']
                ca = row['CA']
                icao = row['ICAO']
                description = row['Description']
                category_dict = {
                    'TC': tc,
                    'CA': ca,
                    'ICAO': icao,
                    'Description': description
                }
                self._categories[category] = category_dict
                self._category_dict[category.lower()] = category_dict