class CommandHandler:

    def __init__(self, chat_instance):
        self.chat = chat_instance

    def checkCommand(self, command: str):
        if any(keyword in command for keyword in ["memorize", "memory", "memories"]):
            self.chat.addMemories(command)
        elif "directive" in command:
            self.chat.addDirectives(command)
        elif "context" in command:
            self.chat.addContext(command)
        elif "example" in command or "examples" in command:
            self.chat.addExample(command)
        elif "reset" in command:
            self.chat.list_manager.reset()
        elif "mode" in command:
            self.chat.changeMode()
        elif "prompt" in command:
            self.chat.prompt_manager.checkPrompt(command)

    def templateCommandParser(self, lst, command_keyword, activation_variable, command):
        """
        Funzione template per gestire una lista data una specifica keyword di comando.
        Se fornita, la variabile di attivazione verrà attivata o disattivata in base alle condizioni.
        """
        commands = command.split()
        print(f"Commands: {commands}")
        if "clear" in command:
            lst = self.chat.list_manager.clearList(lst, command_keyword, activation_variable)
        elif "change" in command:
            self.chat.list_manager.changeItem(lst, command_keyword)
        elif "del" in command:
            self.chat.list_manager.delItem(lst, command_keyword)
        elif "print" in command:
            self.chat.list_manager.printList(lst)
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
            setattr(self.chat, activation_variable, True)
