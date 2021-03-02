import os

class FolderIterator:

    def __init__(self, folder_add, extensions=['.jpg', '.png']):
        self.folder_address = folder_add
        self.extensions = extensions

    def save_paths_in_csv(self, csv_name):
        for _, _, files in os.walk(self.folder_address):
            for f in files:
                for extension in self.extensions:
                    if f.endswith(extension):
                        print(f)
                        break


fi = FolderIterator('E:\\Personal')
fi.save_paths_in_csv('hello')
