import json
import os


class PromptManager:
    commonDirective = ("Rispondi alla domanda tenendo conto delle informazioni e delle direttive fornite. Se sono "
                       "presenti informazioni in MEMORY, basa la tua risposta su di esse. Se sono state fornite "
                       "direttive specifiche, rispetta quelle direttive. Se è stato fornito un contesto, assicurati "
                       "che la tua risposta sia pertinente a quel contesto. E, infine, se sono stati forniti esempi, "
                       "usa quegli esempi come guida per formulare la tua risposta.")

    def __init__(self, chat_instance):
        self.chat = chat_instance

    def checkPrompt(self, command):
        """
        Gestisce i comandi relativi al prompt.
        :param command:
        :return:
        """
        if "print" in command:
            self.printPrompt()
        elif "load" in command:
            self.loadPrompt()
        elif "save" in command:
            self.savePrompt()
        else:
            print("""
            - prompt print
            - prompt load
            - prompt save
            """)

    def printPrompt(self):
        """
        Stampa il prompt.
        :return:
        """
        if self.chat.isStandardMode:
            print(self.createSimplePrompt(""))
        else:
            print(self.createOpenAiPrompt(""))

    def loadPrompt(self):
        """
        Carica il prompt da un file.
        :return:
        """
        fileName = input("Inserisci il nome del file o il percorso assoluto: ")

        # Controlla se il percorso fornito esiste come percorso assoluto
        if os.path.exists(fileName):
            self.deserializePrompt(fileName)
        else:
            # Altrimenti, cerca il file nella directory e nelle sottodirectory
            findFile = self.chat.commonFunctions.findFile(fileName, os.getcwd())
            if findFile:
                self.deserializePrompt(findFile)
            else:
                print("Il file non esiste.")

    def deserializePrompt(self, findFile):
        """
        Deserializza il prompt da un file.
        :param findFile:
        :return:
        """
        jSonDictionary = self.chat.commonFunctions.read(f"{findFile}")
        dictionary = json.loads(jSonDictionary)
        self.chat.memories = dictionary["MEMORY"]
        self.chat.directives = dictionary["DIRECTIVE"]
        self.chat.contexts = dictionary["CONTEXT"]
        self.chat.examples = dictionary["EXAMPLE"]
        self.chat.isMemoryMode = True
        self.chat.isDirectiveMode = True
        self.chat.isContextMode = True
        self.chat.isExampleMode = True
        print("Prompt caricato correttamente.")

    def savePrompt(self):
        """
        Salva il prompt in un file.
        :return:
        """
        dictionary = {
            "MEMORY": self.chat.memories,
            "DIRECTIVE": self.chat.directives,
            "CONTEXT": self.chat.contexts,
            "EXAMPLE": self.chat.examples
        }
        jSonDictionary = json.dumps(dictionary)
        fileName = input("Inserisci il nome del file: ")
        self.chat.commonFunctions.write(f"data/prompt/{fileName}_PROMPT.json", jSonDictionary)
        print("Prompt salvato correttamente.")

    def clearPrompt(self):
        """
        Pulisce il prompt.
        :return:
        """
        self.chat.directives.clear()
        self.chat.contexts.clear()
        self.chat.examples.clear()
        self.chat.isDirectiveMode = False
        self.chat.isContextMode = False
        self.chat.isExampleMode = False
        print("Prompt pulito.")

    def createSimplePrompt(self, question):
        """
        Crea il prompt per il modello standard.
        :param question:
        :return:
        """
        prompt = ""
        if self.chat.isMemoryMode:
            prompt += f"MEMORY: {', '.join(self.chat.memories)}"
        if self.chat.isDirectiveMode:
            prompt += f"DIRECTIVE: {', '.join(self.chat.directives)}"
        if self.chat.isContextMode:
            prompt += f"CONTEXT: {', '.join(self.chat.contexts)}"
        if self.chat.isExampleMode:
            prompt += f"EXAMPLE: {', '.join(self.chat.examples)}"
        return f"""
        {prompt}
    QUESTION: {question}
    ASSISTANT ANSWER:"""

    def createOpenAiPrompt(self, question):
        """
        Crea il prompt per il modello OpenAI.
        :param question:
        :return:
        """
        messages = [
            {
                "role": "system",
                "content": f"{self.commonDirective}",
            }
        ]
        if self.chat.isMemoryMode:
            messages.append({"role": "system", "content": f"MEMORY: {', '.join(self.chat.memories)}"})
        if self.chat.isDirectiveMode:
            messages.append({"role": "system", "content": f"DIRECTIVE: {', '.join(self.chat.directives)}"})
        if self.chat.isContextMode:
            messages.append({"role": "system", "content": f"CONTEXT: {', '.join(self.chat.contexts)}"})
        if self.chat.isExampleMode:
            messages.append({"role": "system", "content": f"EXAMPLE: {', '.join(self.chat.examples)}"})
        messages.append({"role": "user", "content": f"{question}"})
        return messages
