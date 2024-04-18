import subprocess
from config import Config
import signal
import time
from logging import log

"""
subprocess: 새 프로세스를 생성하고 입/출력/에러 파이프라인에 연결하고 반환 코드를 얻는다.
signal: UNIX 신호와 시그널을 처리한다(SIGTERM은 그레이스 풀 종료를 위한 시그널)
time: 작업 지연을 위해 sleep을 사용을 해야함. (프로세스 강제 종료 전 대기 시간과 같은)
config: config 파일에서 정의한 설정을 가져와야 함
logging: 로그 가져와야 함
"""

class Core:
    def __init__(self, config_file):
        self.config = Config(config_file)
        self.processes = {} # 프로세스 이름을 키로 사용하여 프로세스를 저장하는 딕셔너리

    """
    Core 클래스는 Config 클래스를 사용하여 프로그램을 시작, 중지 및 다시 시작하는 메서드를 제공한다.
    인스턴스를 초기화하고 프로세스를 추적하기 위한 딕셔너리 설정
    processes = 프로세스 저장 딕셔너리
    """
    def start_program(self, program_name):
        program_config = self.config.get_program().get(program_name)
        if not program_config:
            log(f"No configuration for program: {program_name}")
            return
        cmd = program_config['cmd']
        numprocs = program_config.get('numprocs', 1)

        for _ in range(numprocs):
            process = subprocess.Popen(
                cmd,
                shell=True,
                preexec_fn=lambda: signal.signal(signal.SIGCHLD, signal.SIG_IGN)
            )
            self.processes[program_name] = self.processes.get(program_name, []) + [process]
            log(f"Started {program_name} with PID {process.pid}")
    """
    start program 메서드는 프로그램 이름을 사용하여 프로그램을 시작한다.
    프로그램 이름을 사용하여 config 파일에서 프로그램 설정을 가져온다.

    for _ in range(numprocs):
    Popen을 사용하여 프로세스를 시작하고, 프로세스에 저장된 수의 프로세스에 사용된다.
    명령은 새로운 쉘에서 실행되며, preexec_fn은 하위 프로세스가 중지되거나 종료될 때 프로세스로 전송되는 SIGCHLD 신호를 무시한다.
    하위 프로세스를 독립적으로 관리하는데에 도움이 된다. 프로세스는 '프로그램 이름' 으로 목록 (processes)에 저장되며, 시작된 각 프로세스마다 로그가 생성된다.
    """

    def stop_program(self, program_name, force=False):
        if program_name not in self.processes:
            log(f"No such program running: {program_name}")
            return

        for process in self.processes[program_name]:
            try:
                if process.poll() is None:  # Only attempt to stop if still running
                    process.send_signal(signal.SIGTERM)
                    log(f"Sent SIGTERM to '{program_name}' with PID {process.pid}")

                    stopwaitsecs = self.config.get_program(program_name).get('stoptime', 10)
                    time.sleep(stopwaitsecs)

                    if process.poll() is None:  # If still running, force kill
                        if force:
                            process.kill()
                            log(f"Forced '{program_name}' with PID {process.pid} to stop")
                        else:
                            log(f"Program '{program_name}' with PID {process.pid} did not terminate after {stopwaitsecs} seconds; consider forcing the stop.")
            finally:
                if process.poll() is not None:
                    self.processes[program_name].remove(process)
                if not self.processes[program_name]:
                    del self.processes[program_name]
        """
        프로그램과 관련된 프로세스를 종료한다. SIGTERM을 프로세스에 전송하여 그레이스풀 종료를 허용한다.
        process.poll은 프로세스가 종료되었는지 확인한다. 종료되지 않은 경우 SIGTERM이 전송되며, 지정된 대기시간 (stop waitsecs) 이후에도 프로세스가 계속 실행중이라면
        force가 true일 때 process.kill()로 강제로 죽인다.
        만약, 프로세스가 중지되면 추적에서 제거되도록 한다.
        """

    def restart_program(self, program_name):
        self.stop_program(program_name, force=True)
        self.start_program(program_name)

    def reload_config(self):
        new_config = Config(self.config.config_file)

        for program_name in new_config.get_program():
            if program_name not in self.config.get_program():
                self.start_program(program_name)
            else:
                if new_config.get_program()[program_name] != self.config.get_program()[program_name]:
                    self.restart_program(program_name)

        for program_name in self.config.get_program():
            if program_name not in new_config.get_program():
                self.stop_program(program_name)

        self.config = new_config
        log("Configuration reloaded.")

    def get_status(self):
        status = {}
        for program_name, processes in self.processes.items():
            status[program_name] = {'running': [p.pid for p in processes if p.poll() is None]}
        return status