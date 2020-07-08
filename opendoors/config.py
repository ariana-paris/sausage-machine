import configparser
import os
from logging import Logger

from opendoors.utils import get_full_path


class ArchiveConfig:

    def __init__(self, logger: Logger, code_name, working_dir):
        self.logger = logger
        self.working_dir = working_dir
        self.code_name = code_name
        self.config_path = os.path.join(self.working_dir, self.code_name + ".ini")
        self.config = self._create_or_get_archive_config()

    def _new_config_file(self):
        # Use sample config to generate a new config
        archive_config_path = os.path.join(os.getcwd(), "config_files")
        self.config.read(os.path.join(archive_config_path, "_sample_config.ini"))
        self._processing_config()
        archive_name, archive_type = self._archive_config()
        self.config['Archive'] = {
            'archive_name': archive_name,
            'archive_type': archive_type
        }

        # Write out the new config file
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)
            self.logger.info("Successfully created configuration file {}.".format(self.config_path))
        return self.config

    def _archive_config(self):
        # Set Archive settings
        archive_name = input("Full archive name (eg: 'TER/MA', 'West Wing Fanfiction Archive') - this will be used to "
                             "generate dummy emails\n>> ")
        # Prompt for archive type and remove unwanted section
        archive_type = input("Archive type (EF = eFiction, AA = AutomatedArchive, or Other)\n>> ")
        archive_type = archive_type if archive_type in ['EF', 'AA'] else 'Other'
        if archive_type == "EF":
            self.config.remove_section('AutomatedArchive')
        return archive_name, archive_type

    def _processing_config(self):
        # Set Processing settings
        self.config['Processing'] = {
            'code_name': self.code_name,
            'working_dir': self.working_dir,
            'next_step': "01",
            'done_steps': ""
        }

    def _create_or_get_archive_config(self):
        config = configparser.ConfigParser()
        config_path = get_full_path(self.config_path)
        print(config_path)
        if os.path.exists(config_path):
            print(f"Found existing config file {self.config_path}.")
            config.read(config_path)
        else:
            config = self._new_config_file()
        return config

    def save(self):
        """
        Save both the original ini file in the project and the backup copy kept in the working directory
        :return: 0 if there is no config to save
        """
        if len(self.config.keys()) != 0:
            backup_path = os.path.join(self.config['Processing']['working_dir'], os.path.basename(self.config_path))
            with open(backup_path, 'w') as backup_config:
                self.config.write(backup_config)

            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
        else:
            return 0
