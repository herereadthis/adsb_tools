import csv
import os

class WakeVortexCategories:
    """
    A class that loads wake vortex categories from a CSV file and provides access to them through various methods.

    The CSV file should have the following columns: Category, TC, CA, ICAO, Description.

    Attributes:
        categories (list): A list of dictionaries representing each category.
        category_dict (dict): A dictionary mapping each category name to its corresponding dictionary.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._categories = []
            cls._instance._categories_dict = {}
            cls._instance._category_dict = {}
            cls._instance._parse_csv()
        return cls._instance

    @property
    def categories(self):
        """
        Returns the list of categories as a list of dictionaries.

        Returns:
            list: A list of dictionaries representing each category.
        """
        return self._categories

    @property
    def category_dict(self):
        """
        Returns a dictionary mapping category names to their corresponding dictionaries.

        Returns:
            dict: A dictionary mapping category names to their corresponding dictionaries.
        """
        return self._category_dict

    def get_category_dict(self, category):
        """
        Returns the dictionary corresponding to the given category name.

        Args:
            category (str): The name of the category.

        Returns:
            dict: A dictionary representing the category.
        """
        return self._category_dict.get(category.lower())

    def _parse_csv(self):
        """
        Parses the CSV file and populates the internal category dictionaries.
        """
        # get the directory of the current script (foo.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # construct the path to the csv file
        csv_file_path = os.path.join(current_dir, 'static', 'wake_vortex_categories.csv')
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = row['Category']
                tc = row['TC']
                ca = row['CA']
                icao = row['ICAO']
                description = row['Description']
                category_dict = {
                    'tc': int(tc) if tc != "" else None,
                    'ca': int(ca) if ca != "" else None,
                    'icao': icao,
                    'category': category,
                    'description': description
                }
                self._categories.append(row)
                self._category_dict[category.lower()] = category_dict
