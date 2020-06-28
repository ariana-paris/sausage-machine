import os
import shutil
from abc import abstractmethod
from configparser import ConfigParser
from logging import Logger


class StepBase:
    def __init__(self, config: ConfigParser, logger: Logger):
        self.logger = logger
        self.config = config
        self.step = "UNKNOWN"

    def create_working_sub_dir(self):
        step_path = os.path.join(self.config['Processing']['working_dir'], self.step)
        if os.path.exists(step_path):
            shutil.rmtree(step_path)
            self.logger.info(f"Deleted existing {self.step} folder to start from scratch")
        os.makedirs(step_path)
        return step_path

    @abstractmethod
    def run(self):
        pass
