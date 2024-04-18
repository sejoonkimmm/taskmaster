import cmd
from .core import Core
import os

class ControlShell(cmd.Cmd):
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    BLUE = '\033[1;34m'
    RESET = '\033[0m'

    intro = f'{BLUE}Taskmaster control shell start.{RESET}'
    prompt = f'{GREEN}(taskmaster){RESET} '

    def __init__(self, core):
        super().__init__()
        self.core = core

    def cmdloop(self, intro=None):
        if intro is not None:
            print(intro)
        else:
            print(self.intro)

        while True:
            try:
                super().cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print(f"\n{self.RED}Keyboard interrupt. Exiting control shell.{self.RESET}")
            except EOFError:
                print(f"\n{self.RED}EOF. Exiting control shell.{self.RESET}")

    def emptyline(self):
        pass

    def do_start(self, arg):
        program_name = arg
        if program_name:
            self.core.start_program(program_name)
        else:
            print("Please specify a program name to start.")

    def do_stop(self, arg):
        program_name = arg.strip()
        if not arg:
            print("Please specify a program name or PID to stop.")
            return

        try:
            pid = int(arg)
            self.core.stop_program_pid(pid)
        except ValueError:
            self.core.stop_program(program_name)

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
        print(f"${self.BLUE}\nExiting Taskmaster control shell.{self.RESET}")
        return True  # This will exit the cmd loop
    
    def do_EOF(self, line):
        self.do_exit(line)
        print(f"{self.BLUE}Thank you for using Taskmaster.{self.RESET}")
        return True

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(dir_path, '..', 'configs', 'default.yaml')
    core_instance = Core(config_path)
    ControlShell(core_instance).cmdloop()