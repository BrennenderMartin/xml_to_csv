# Mapping with key:value1:value2 structure
mapping = {
    "Python Programming": ("John Doe", 2020),
    "Machine Learning Basics": ("Jane Smith", 2021),
    "Data Science with Python": ("Mike Johnson", 2019),
}

# Accessing values for a specific key
book = "Python Programming"
author, year = mapping[book]
print(f"Book: '{book}', Author: '{author}', Year: '{year}'")
