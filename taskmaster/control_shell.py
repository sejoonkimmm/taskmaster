import cmd
from core import Core

class ControlShell(cmd.Cmd):
    intro = 'Taskmaster control shell start.'
    prompt = '(taskmaster) '

    def __init__(self, core):
        super().__init__()
        self.core = core

    def do_start(self, arg):
        program_name = arg
        if program_name:
            self.core.start_program(program_name)
        else:
            print("Please specify a program name to start.")

    def do_stop(self, arg):
        program_name = arg.strip()
        if program_name:
            self.core.stop_program(program_name)
        else:
            print("Pleas specify a program name to stop.")

    def do_restart(self, arg):
        program_name = arg.strip()
        if program_name:
            self.core.stop_program(program_name)
            self.core.start_program(program_name)
        else:
            print("Please specify a program name to restart.")

    def do_reload(self, arg):
        self.core.reload_config()
        print("Reloaded configuration.")

    def do_status(self, line):
        """ Get the status of all the programs. """
        status = self.core.get_status()
        for program_name, process_info in status.items():
            if process_info['running']:
                print(f"{program_name}: Running processes - {process_info['running']}")
            else:
                print(f"{program_name}: No running processes")

    def do_exit(self, line):
        """ Exit the control shell. """
        print("Exiting Taskmaster control shell.")
        return True  # This will exit the cmd loop

if __name__ == '__main__':
    core_instance = Core('../configs/default.yaml')
    ControlShell(core_instance).cmdloop()