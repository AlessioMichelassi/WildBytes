class ListManager:
    def __init__(self, chat_instance):
        self.chat = chat_instance

    def clearList(self, lst, command_keyword, activation_variable):
        setattr(self.chat, activation_variable, False)
        print(f"{command_keyword.capitalize()} cleared.")
        lst.clear()
        return lst

    def changeItem(self, lst, command_keyword):
        itemNumber = int(input(f"Quale {command_keyword} vuoi cambiare? "))
        if itemNumber < len(lst):
            lst[itemNumber] = input(f"Cosa vuoi {command_keyword}? ")
        else:
            self.printError(command_keyword, "indexError")

    def delItem(self, lst, command_keyword):
        itemNumber = int(input(f"Quale {command_keyword} vuoi cancellare? "))
        if itemNumber < len(lst):
            lst.pop(itemNumber)
        else:
            self.printError(command_keyword, "indexError")

    def reset(self):
        self.chat.isMemoryMode = False
        self.chat.isDirectiveMode = False
        self.chat.isContextMode = False
        self.chat.isExampleMode = False
        self.chat.isStandardMode = True
        self.chat.memories.clear()
        self.chat.directives.clear()
        self.chat.contexts.clear()
        self.chat.examples.clear()
        print("All variables and lists have been reset.")

    @staticmethod
    def printError(command_keyword, error_Type):
        if error_Type == "indexError":
            print(f"Non esiste un {command_keyword} con questo numero.")

    @staticmethod
    def printList(lst):
        if len(lst) == 0:
            print("La lista è vuota.")
        for i, item in enumerate(lst):
            print(f"{i}: {item}")
