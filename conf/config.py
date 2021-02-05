# Logger
import logging
import os

LOG_FILE_NAME = 'faro-community.log'
LOG_LEVEL = os.getenv('FARO_LOG_LEVEL', "INFO")

logging.basicConfig(
        level=LOG_LEVEL,
        format="%(levelname)s: %(name)20s: %(message)s",
        handlers=[logging.StreamHandler()]
    )