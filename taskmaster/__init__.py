from .control_shell import ControlShell
from .core import Core
from .config import Config, ConfigError
from .logging import setup_logging

def main():
    setup_logging()
    core = Core('configs/default.yaml')
    shell = ControlShell(core)
    shell.cmdloop()

if __name__ == '__main__':
    main()


"""
config.py : configuration 파일을 파싱하고 액세스할 때 사용한다.
core.py : 프로세스 시작 / 정지 / 모니터링 프로세스 / '원하는 상태'(desire state)로 프로세스를 유지하기 위한 로직을 포함한다.
logging.py : 프로세스 관리와 관련한 모든 이벤트에 파일로 기록하는 것을 관리한다.
control_shell.py : 사용자가 프로세스 관리를 위해 대화형 명령줄 인터페이스를 제공할 것이다.
"""