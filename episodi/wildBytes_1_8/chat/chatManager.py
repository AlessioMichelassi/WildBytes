from episodi.wildBytes_1_8.chat.chatGptWrapper import ChatGptAPIWrapper
from episodi.wildBytes_1_8.chat.commandHandler import CommandHandler
from episodi.wildBytes_1_8.chat.commonFunction import CommonFunctions
from episodi.wildBytes_1_8.chat.listManager import ListManager
from episodi.wildBytes_1_8.chat.promptManager import PromptManager


class ChatManager:

    def __init__(self):
        self.command_handler = CommandHandler(self)
        self.list_manager = ListManager(self)
        self.prompt_manager = PromptManager(self)

        self.isMemoryMode = False
        self.isDirectiveMode = False
        self.isContextMode = False
        self.isExampleMode = False
        self.isStandardMode = True

        self.memories = []
        self.directives = []
        self.contexts = []
        self.examples = []

        self.chatGpt = ChatGptAPIWrapper(self)
        self.commonFunctions = CommonFunctions()
        self.isWannaExit = False

        try:
            self.startChat()
        except KeyboardInterrupt:
            self.chatGpt.serialize()
            print("\nExiting...")

    def startChat(self):
        while not self.isWannaExit:
            if self.chatGpt.budget <= 0.002:
                print("Non hai abbastanza soldi per continuare a chattare.")
                self.isWannaExit = self.chatGpt.askToAddMoreBudget()
            else:
                question = input("Domanda: ").strip()
                if not question:
                    print("Per favore, inserisci una domanda valida.")
                    continue
                elif question.lower() == "#exit":
                    self.isWannaExit = True
                    break
                elif question.lower().startswith("#"):
                    self.command_handler.checkCommand(question)
                    continue
                if self.isStandardMode:
                    print(self.chatGpt.getAnswer(self.prompt_manager.createSimplePrompt(question)))
                else:
                    print(self.chatGpt.getAnswer(self.prompt_manager.createOpenAiPrompt(question)))

    def addMemories(self, command: str):
        self.command_handler.templateCommandParser(self.memories, "memories", "isMemoryMode", command)

    def addMemoriesFromGpt(self, content):
        self.memories.append(content)
        self.isMemoryMode = True

    def addDirectives(self, command: str):
        self.command_handler.templateCommandParser(self.directives, "directive", "isDirectiveMode", command)

    def addContext(self, command: str):
        self.command_handler.templateCommandParser(self.contexts, "context", "isContextMode", command)

    def addExample(self, command: str):
        self.command_handler.templateCommandParser(self.examples, "example", "isExampleMode", command)

    def setParameters(self, command: str):
        if "temperature" in command:
            temp = input("Inserisci la temperatura da 0.0 a 1.0: ")
            try:
                self.chatGpt.setTemperature(float(temp))
            except ValueError:
                print("La temperatura deve essere un numero.")
        elif "max_tokens" in command:
            try:
                maxTokens = input("Inserisci il numero massimo di token: ")
                self.chatGpt.setMaxTokens(int(maxTokens))
            except ValueError:
                print("Il numero massimo di token deve essere un numero intero.")
        elif "model" in command:
            print(f"I modelli disponibili sono: {self.chatGpt.geModelList()}")
            model = input("Inserisci il nome del modello: ")
            if model:
                self.chatGpt.setModel(model)
        elif "standard" in command:
            self.changeMode()
        else:
            print("Comando non riconosciuto.")

    def printParameters(self, command: str):
        if "temperature" in command:
            print(f"Temperature: {self.chatGpt.getTemperature()}")
        elif "max_tokens" in command:
            print(f"Max tokens: {self.chatGpt.getMaxTokens()}")
        elif "model" in command:
            print(f"Model: {self.chatGpt.getModel()}")
        elif "standard" in command:
            print(f"Standard mode: {self.isStandardMode}")
        else:
            print("Comando non riconosciuto.")

    def changeMode(self):
        answer = input("Vuoi attivare la modalità standard - 0 o la modalià openAI - 1? [0/1] ")
        if answer == "0":
            self.isStandardMode = True
        elif answer == "1":
            self.isStandardMode = False


if __name__ == '__main__':
    ChatManager()
