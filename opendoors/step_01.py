import os
import shutil
from configparser import ConfigParser
from logging import Logger

from opendoors.sql import SqlDb
from opendoors.step_base import StepBase
from opendoors.utils import copy_to_dir, make_banner


class Step01(StepBase):
    """
    Load and convert original database file for eFiction or Automated Archive
    """

    def __init__(self, config: ConfigParser, logger: Logger):
        super().__init__(config, logger)
        self.step = "step01"
        self.working_sub_dir = self.create_working_sub_dir()
        self.sql = SqlDb(self.config, self.logger)

    def __check_config_and_continue(self):
        """
        Check archive type and prompt user for db file.
        :return: True if this step needs to be performed, or False if processing should skip to step 02
        """
        archive_type = self.config['Archive']['archive_type']
        # Prompt for original db file for EF or AA
        if archive_type in ["EF", "AA"]:
            if not (self.config.has_option('Archive', 'original_db_file')) or \
                    self.config['Archive']['original_db_file'] == "":
                path_to_original_db = input(">> Full path to the original database file "
                                            "(this will be copied into the working path and loaded into MySQL):\n")
                self.config['Archive']['original_db_file'] = path_to_original_db
            return True
        else:
            return False

    def __check_or_create_original_backup(self, code_name, original_db_file, original_filename, working_dir):
        if self.config.has_option('Processing', 'backup_file') and os.path.exists(
                self.config['Processing']['backup_file']):
            backup_file = self.config['Processing']['backup_file']
            self.logger.info("Using backup file {}".format(backup_file))
        else:
            backup_file = copy_to_dir(original_db_file, os.path.join(working_dir, "backups"),
                                      f"{code_name}_{original_filename}")
            self.config['Processing']['backup_file'] = backup_file
            self.logger.info(f"Created backup of original file at {backup_file}")
        return backup_file

    def __copy_to_working_sub_dir(self):
        code_name = self.config['Processing']['code_name']
        original_db_file = self.config['Archive']['original_db_file']
        original_filename = os.path.basename(original_db_file)
        try:
            self.__check_or_create_original_backup(code_name, original_db_file, original_filename, self.working_sub_dir)
            if self.config.has_option('Processing', 'step01_temp_working_db_file') \
                    and os.path.exists(self.config['Processing']['step01_temp_working_db_file']):
                self.logger.info("Using existing working copy of original file in {}".format(
                    self.config['Processing']['step01_temp_working_db_file']))
            else:
                destination_file = copy_to_dir(original_db_file, self.working_sub_dir,
                                               f"{code_name}_{original_filename}")
                self.config['Processing']['step01_temp_working_db_file'] = destination_file
                self.logger.info("Copied working copy of original file to {}".format(destination_file))
            return True
        except shutil.Error as e:
            self.logger.error(e.strerror)
            return False

    def __edit_db_copy(self):
        archive_type = self.config['Archive']['archive_type']
        if archive_type == 'EF':
            self.logger.info("Processing eFiction archive...")
        elif archive_type == 'AA':
            # TODO: handle Automated Archive and Other
            return True
        else:
            return True

    def run(self):
        """
        Load original database or skip this step
        :return: True if this step was successful and can move on to step 02, False if an error occurred
        """
        banner = make_banner('-', '   Running Step 01   ')
        # Copy the original database file into the working directory and then process
        try:
            if self.__check_config_and_continue():
                self.logger.info(banner)
                if self.__copy_to_working_sub_dir() and self.__edit_db_copy():
                    self.finish()
                    return True
                else:
                    return False
            else:
                self.logger.info(
                    "This step needs to be performed manually for archives that are not eFiction or Automated Archive")
                self.finish()
                return True
        except Exception as e:
            self.logger.error(e)
            return False

    def finish(self):
        self.logger.info("\nStep 01 completed, ready for step 02\n")
        self.config['Processing']['next_step'] = "02"
