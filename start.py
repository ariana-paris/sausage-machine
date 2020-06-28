import atexit
import sys

from opendoors import progress
from opendoors.config import ArchiveConfig
from opendoors.logging import Logging
from opendoors.utils import make_banner, create_or_set_working_dir


@atexit.register
def save_config_and_exit():
    print("Saving config...")
    config.save()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        code_name = sys.argv[1]
    else:
        code_name = input(
            ">> Please provide a short, lowercase code name with no spaces or punctuation for the archive "
            "you are processing (and make a note of it as you'll need it in future!):")

    banner_text = f"""Starting processing for archive "{code_name}"..."""
    banner = make_banner('=', banner_text)

    working_dir = sys.argv[2] if len(sys.argv) > 2 else create_or_set_working_dir(code_name)

    logger = Logging(working_dir, code_name).logger()
    logger.info(banner)

    config = ArchiveConfig(logger, code_name, working_dir)
    archive_config = config.config

    progress.continue_from_last(archive_config, logger)
