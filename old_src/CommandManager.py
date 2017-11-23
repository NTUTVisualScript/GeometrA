###http://derdon.github.io/blog/implementing-an-undo-redo-manager-in-python.html

class CommandManager(object):
    def __init__(self):
        self.undo_commands = []
        self.redo_commands = []

    def push_undo_command(self, command):
        """Push the given command to the undo command stack."""
        self.undo_commands.append(command)

    def pop_undo_command(self):
        """Remove the last command from the undo command stack and return it.
        If the command stack is empty, EmptyCommandStackError is raised.
        """
        try:
            last_undo_command = self.undo_commands.pop()
        except IndexError:
            raise NotImplementedError
        return last_undo_command

    def push_redo_command(self, command):
        """Push the given command to the redo command stack."""
        self.redo_commands.append(command)

    def pop_redo_command(self):
        """Remove the last command from the redo command stack and return it.
        If the command stack is empty, EmptyCommandStackError is raised.
        """
        try:
            last_redo_command = self.redo_commands.pop()
        except IndexError:
            raise NotImplementedError
        return last_redo_command

    def do(self, command):
        """Execute the given command. Exceptions raised from the command are
        not catched.
        """
        command()
        self.push_undo_command(command)
        # clear the redo stack when a new command was executed
        self.redo_commands[:] = []

    def undo(self):
        """Undo the last n commands. The default is to undo only the last
        command. If there is no command that can be undone because n is too big
        or because no command has been emitted yet, EmptyCommandStackError is
        raised.
        """
        command = self.pop_undo_command()
        command.undo()
        self.push_redo_command(command)

    def redo(self):
        """Redo the last n commands which have been undone using the undo
        method. The default is to redo only the last command which has been
        undone using the undo method. If there is no command that can be redone
        because n is too big or because no command has been undone yet,
        EmptyCommandStackError is raised.
        """
        command = self.pop_redo_command()
        command()
        self.push_undo_command(command)