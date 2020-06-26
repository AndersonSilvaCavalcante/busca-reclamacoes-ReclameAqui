import csv


class CSVGenerator:
    def __init__(self, document, directory, file_name, index):
        self.document = document
        self.directory = directory
        self.file_name = file_name
        self.index = index

    def generate_csv(self):
        document = self.document
        directory = self.directory
        file_name = self.file_name
        index = self.index
        document.to_csv(
            f"{directory}/{file_name}.csv", index=index)
