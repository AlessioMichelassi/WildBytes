from episodi.wildBytes_1_5.ex5_1_gptW import ChatGptAPIWrapper


class Chat:
    isMemoryMode = False
    isDirectiveMode = False
    isContextMode = False
    isExampleMode = False

    memories = []
    directives = []
    contexts = []
    examples = []

    chatGpt: ChatGptAPIWrapper
    isWannaExit = False

    def __init__(self):
        self.chatGpt = ChatGptAPIWrapper()
        self.startChat()

    def startChat(self):
        while self.isWannaExit is False:
            # Utilizza strip() per rimuovere spazi bianchi all'inizio e alla fine
            question = input("Domanda: ").strip()
            if not question:  # Controlla se la domanda è vuota
                print("Per favore, inserisci una domanda valida.")
                continue
            if question.lower() == "#exit":
                self.isWannaExit = True
                break
            elif question.lower().startswith("#"):
                self.checkCommand(question)
                continue
            if self.chatGpt.budget <= 0.002:
                print("Non hai abbastanza soldi per continuare a chattare.")
                self.isWannaExit = self.chatGpt.askToAddMoreBudget()
            print(self.chatGpt.getAnswer(self.createSimplePrompt(question)))

    def checkCommand(self, command: str):
        if any(keyword in command for keyword in ["memorize", "memory", "memories"]):
            self.addMemories(command)
        elif "directive" in command:
            self.addDirectives(command)
        elif "context" in command:
            self.addContext(command)
        elif "example" in command or "examples" in command:
            self.addExample(command)

    def templateCommandParser(self, lst, command_keyword, activation_variable, command):
        """
        Funzione template per gestire una lista data una specifica keyword di comando.
        Se fornita, la variabile di attivazione verrà attivata o disattivata in base alle condizioni.
        """
        if f"{command_keyword} clear" in command:
            lst = []
            if activation_variable is not None:
                setattr(self, activation_variable, False)
            print(f"{command_keyword.capitalize()} cleared.")
        elif "change" in command:
            itemNumber = int(input(f"Quale {command_keyword} vuoi cambiare? "))
            if itemNumber < len(lst):
                lst[itemNumber] = input(f"Cosa vuoi {command_keyword}? ")
            else:
                print(f"Non esiste un {command_keyword} con questo numero.")
        elif "del" in command:
            itemNumber = int(input(f"Quale {command_keyword} vuoi cancellare? "))
            if itemNumber < len(lst):
                lst.pop(itemNumber)
                if not lst and activation_variable is not None:
                    self.enableAttribute(command_keyword, activation_variable)
            else:
                print(f"Non esiste un {command_keyword} con questo numero.")
        elif "help" in command:
            print(self.createHelpString(command_keyword))
        else:
            answer = input(f"Cosa vuoi {command_keyword}? ")
            if answer:
                lst_was_empty = not lst
                lst.append(answer)
                if lst_was_empty and activation_variable is not None and not activation_variable:
                    self.enableAttribute(command_keyword, activation_variable)
        return lst

    @staticmethod
    def createHelpString(command_keyword):
        return (f"""
                Comandi disponibili:
                - {command_keyword}
                - {command_keyword} del
                - {command_keyword} change
                - {command_keyword} clear
                - {command_keyword} help
                """)

    def enableAttribute(self, command_keyword, activation_variable):
        check = input(f"Vuoi attivare la modalità {command_keyword}? [y/n] ")
        if check.lower() == "y":
            setattr(self, activation_variable, True)
        else:
            setattr(self, activation_variable, False)

    def addMemories(self, command: str):
        """
        Aggiunge un ricordo alla memoria, cancella un ricordo specifico, lo cambia, oppure cancella tutto.
        I comandi possibili sono:
        - memorize
        - memorize del
        - memorize change
        - memorize clear
        - memorize help
        :param command: a string that contains the command
        :return:
        """
        self.templateCommandParser(self.memories, "memories", "isMemoryMode", command)

    def addDirectives(self, command: str):
        """
        Aggiunge una direttiva, cancella una direttiva specifica, la cambia, oppure cancella tutto.
        I comandi possibili sono:
        - directive
        - directive del
        - directive change
        - directive clear
        - directive help
        :param command: a string that contains the command
        :return:
        """
        self.templateCommandParser(self.directives, "directive", "isDirectiveMode", command)

    def addContext(self, command: str):
        """
        Aggiunge un contesto, cancella un contesto specifico, lo cambia, oppure cancella tutto.
        I comandi possibili sono:
        - context
        - context del
        - context change
        - context clear
        - context help
        :param command:
        :return:
        """
        self.templateCommandParser(self.contexts, "context", "isContextMode", command)

    def addExample(self, command: str):
        """
        Aggiunge un esempio, cancella un esempio specifico, lo cambia, oppure cancella tutto.
        I comandi possibili sono:
        - example
        - example del
        - example change
        - example clear
        - example help
        :param command:
        :return:
        """
        self.templateCommandParser(self.examples, "example", "isExampleMode", command)

    def createSimplePrompt(self, question):
        prompt = ""
        if self.isMemoryMode:
            prompt += f"MEMORY: {', '.join(self.memories)}"
        if self.isDirectiveMode:
            prompt += f"DIRECTIVE: {', '.join(self.directives)}"
        if self.isContextMode:
            prompt += f"CONTEXT: {', '.join(self.contexts)}"
        if self.isExampleMode:
            prompt += f"EXAMPLE: {', '.join(self.examples)}"
        return f"""
        {prompt}
    QUESTION: {question}
    ASSISTANT ANSWER:"""


if __name__ == '__main__':
    Chat()
