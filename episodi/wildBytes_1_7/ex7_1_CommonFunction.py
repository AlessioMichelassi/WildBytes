import os


class CommonFunctions:

    @staticmethod
    def read(file_path):
        """Legge il contenuto di un file."""
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def write(file_path, content):
        """Scrive (o sovrascrive) il contenuto su un file."""
        with open(file_path, 'w') as file:
            file.write(content)

    @staticmethod
    def append(file_path, content):
        """Aggiunge contenuto alla fine di un file esistente."""
        with open(file_path, 'a') as file:
            file.write(content)

    @staticmethod
    def exists(file_path):
        """Verifica se un file esiste."""
        try:
            with open(file_path, 'r'):
                return True
        except FileNotFoundError:
            return False

    @staticmethod
    def findFile(target_file, search_path):
        """
        Cerca un file in una directory e nelle sue sottodirectory.

        :param target_file: nome del file da cercare.
        :param search_path: percorso della directory in cui iniziare la ricerca.
        :return: percorso completo del file se trovato, altrimenti None.
        """
        for folderName, subFolders, fileNames in os.walk(search_path):
            if target_file in fileNames:
                return os.path.join(folderName, target_file)
        return None

    @staticmethod
    def delete(file_path):
        """Elimina un file, se esiste."""
        import os
        try:
            os.remove(file_path)
            return f"File {file_path} eliminato."
        except FileNotFoundError:
            return f"File {file_path} non trovato."



