class OpenAIApiFunctionManager:
    def __init__(self):
        # Lista delle funzioni per l'API
        self.functions = []

    @staticmethod
    def createParameter(properties, required):
        """
        Crea un parametro.
        :param properties: Proprietà del parametro.
        :param required: Lista dei campi obbligatori.
        :return: Un dizionario rappresentante il parametro.
        """
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

    @staticmethod
    def createContentParameter(_type, description):
        """
        Crea un parametro specifico per il contenuto.
        :param _type: Tipo del contenuto.
        :param description: Descrizione del contenuto.
        :return: Un dizionario rappresentante il parametro di contenuto.
        """
        return {
            "content": {
                "type": _type,
                "description": description
            }
        }

    @staticmethod
    def createFunction(name, description, parameters):
        """
        Crea una funzione.
        :param name: Nome della funzione.
        :param description: Descrizione della funzione.
        :param parameters: Parametri della funzione.
        :return: Un dizionario rappresentante la funzione.
        """
        return {
            "name": name,
            "description": description,
            "parameters": parameters
        }

    def addFunction(self, name, description, parameters):
        """
        Aggiunge una funzione per l'api di openAI.
        :param name: Nome della funzione.
        :param description: Descrizione della funzione.
        :param parameters: Parametri della funzione.
        :return: La funzione creata.
        """
        func = self.createFunction(name, description, parameters)
        self.functions.append(func)
        return func
