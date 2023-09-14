from episodi.wildBytes_1_6.ex6_4_gptW import ChatGptAPIWrapper


class Chat:
    isMemoryMode = False
    isDirectiveMode = False
    isContextMode = False
    isExampleMode = False
    isStandardMode = True

    memories = []
    directives = []
    contexts = []
    examples = []

    chatGpt: ChatGptAPIWrapper
    isWannaExit = False

    def __init__(self):
        self.chatGpt = ChatGptAPIWrapper(self)
        try:
            self.startChat()
        except KeyboardInterrupt:
            self.chatGpt.serialize()
            print("\nExiting...")

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
            if self.isStandardMode:
                print(self.chatGpt.getAnswer(self.createSimplePrompt(question)))
            else:
                print(self.chatGpt.getAnswer(self.createOpenAiPrompt(question)))

    def checkCommand(self, command: str):
        if any(keyword in command for keyword in ["memorize", "memory", "memories"]):
            self.addMemories(command)
        elif "directive" in command:
            self.addDirectives(command)
        elif "context" in command:
            self.addContext(command)
        elif "example" in command or "examples" in command:
            self.addExample(command)
        elif "reset" in command:
            self.reset()
        elif "mode" in command:
            self.changeMode()
        elif "prompt" in command:
            self.printPrompt()

    def templateCommandParser(self, lst, command_keyword, activation_variable, command):
        """
        Funzione template per gestire una lista data una specifica keyword di comando.
        Se fornita, la variabile di attivazione verrà attivata o disattivata in base alle condizioni.
        """
        commands = command.split()
        print(f"Commands: {commands}")
        if "clear" in command:
            lst = self.clearList(lst, command_keyword, activation_variable)
        elif "change" in command:
            self.changeItem(lst, command_keyword)
        elif "del" in command:
            self.delItem(lst, command_keyword)
        elif "print" in command:
            self.printList(lst)
        elif "help" in command:
            print(self.createHelpString(command_keyword))

        else:
            answer = input(f"Cosa vuoi {command_keyword}? ")
            if answer:
                lst_was_empty = not lst
                lst.append(answer)
                if lst_was_empty:
                    self.enableAttribute(command_keyword, activation_variable)
                else:
                    print(f"lst_was_empty: {lst_was_empty}")
        return lst

    @staticmethod
    def createHelpString(command_keyword):
        if command_keyword:
            return (f"""
                Comandi disponibili:
                - {command_keyword}
                - {command_keyword} del
                - {command_keyword} change
                - {command_keyword} clear
                - {command_keyword} help
                """)
        else:
            return ("""
                    Comandi disponibili:
                    - #memorize
                    - #directive
                    - #context
                    - #example
                    - #reset
                    - #exit
                    """)

    def enableAttribute(self, command_keyword, activation_variable):
        check = input(f"Vuoi attivare la modalità {command_keyword}? [y/n] ")
        if check.lower() == "y":
            setattr(self, activation_variable, True)

    def clearList(self, lst, command_keyword, activation_variable):
        setattr(self, activation_variable, False)
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
        self.isMemoryMode = False
        self.isDirectiveMode = False
        self.isContextMode = False
        self.isExampleMode = False
        self.isStandardMode = True
        self.memories.clear()
        self.directives.clear()
        self.contexts.clear()
        self.examples.clear()
        print("All variables and lists have been reset.")

    def changeMode(self):
        answer = input("Vuoi attivare la modalità standard - 0 o la modalià openAI - 1? [0/1] ")
        if answer == "0":
            self.isStandardMode = True
        elif answer == "1":
            self.isStandardMode = False

    def printPrompt(self):
        if self.isStandardMode:
            print(self.createSimplePrompt(""))
        else:
            print(self.createOpenAiPrompt(""))

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

    def addMemoriesFromGpt(self, content):
        self.memories.append(content)
        self.isMemoryMode = True

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

    def createOpenAiPrompt(self, question):
        messages = [
            {
                "role": "system",
                "content": "Rispondi alla domanda tenendo conto delle informazioni e delle direttive fornite. Se sono "
                           "presenti informazioni in MEMORY, basa la tua risposta su di esse. Se sono state fornite "
                           "direttive specifiche, rispetta quelle direttive. Se è stato fornito un contesto, "
                           "assicurati che la tua risposta sia pertinente a quel contesto. E, infine, se sono stati "
                           "forniti esempi, usa quegli esempi come guida per formulare la tua risposta.",
            }
        ]
        if self.isMemoryMode:
            messages.append({"role": "system", "content": f"MEMORY: {', '.join(self.memories)}"})
        if self.isDirectiveMode:
            messages.append({"role": "system", "content": f"DIRECTIVE: {', '.join(self.directives)}"})
        if self.isContextMode:
            messages.append({"role": "system", "content": f"CONTEXT: {', '.join(self.contexts)}"})
        if self.isExampleMode:
            messages.append({"role": "system", "content": f"EXAMPLE: {', '.join(self.examples)}"})
        messages.append({"role": "user", "content": f"{question}"})
        return messages


if __name__ == '__main__':
    Chat()
