"""Utilities"""

from datetime import datetime
import logging
import os
import sys

def create_project_dir(name):
        # • Get the script path, script (module) name, etc., and deduce the project directory.
    # We want to make sure the *logs* folder is created inside the project directory, regardless
    # of the current working directory
    #
    SCRIPT_PATH = os.path.realpath(sys.argv[0])
    # ↳ *sys.argv[0]* contains the script name (it is operating system dependent whether this is a full pathname or not)
    # ↳ *realpath* eliminates symbolic links and returns the canonical path.
    #
    SCRIPT_FILENAME = os.path.basename(SCRIPT_PATH)
    #
    # Trim the '.py' extension to get the name of the script (module). If the script filename does not have a '.py'
    # extention, don't trim anything.
    if SCRIPT_FILENAME[-3:] == '.py':
        SCRIPT_NAME = SCRIPT_FILENAME[:-3]
    else:
        SCRIPT_NAME = SCRIPT_FILENAME
    #
    # Package directory = the directory that the script/module file resides in
    # Project directory = one level higher than the package directory
    # *os.path.dirname* goes one level up in the directory
    PACKAGE_DIRECTORY = os.path.dirname(SCRIPT_PATH)
    PROJECT_DIRECTORY = os.path.dirname(PACKAGE_DIRECTORY)

    # Assemble the logs directory
    CREATED_DIRECTORY = os.path.join(PROJECT_DIRECTORY, name)
    # Create the directory if it does not exist
    os.makedirs(CREATED_DIRECTORY, exist_ok=True)
    return CREATED_DIRECTORY, SCRIPT_NAME

def configure_root_logger():
    """Create a logger and set its configurations."""

    # Create a RootLogger object
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
    ''' 
    ↳ The logger discards any logging calls with a level of severity lower than the level of the logger.
    Next, each handler decides to accept/discard the call based on its own level.
    By setting the level of the logger to NOTSET, we hand the power to handlers, and we don't filter out anything
    at the entrance. In effect, this is the same as setting the level to DEBUG (lowest level possible).
    '''

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    LOGS_DIRECTORY, SCRIPT_NAME = create_project_dir('logs')

    # Assemble the log file name
    LOG_FILE_NAME = datetime.today().strftime('%Y-%m-%d_%H-%M-%S ') + SCRIPT_NAME + '.log'
    LOG_FILE_PATH = os.path.join(LOGS_DIRECTORY, LOG_FILE_NAME)

    # Create a file handler
    file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and set it to the handlers
    formatter = logging.Formatter('%(name)-18s: %(levelname)-8s %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def store_trained_model(clf, name):
    MODELS_DIR, _ = create_project_dir('models')
    MODEL_FILE_NAME = name + '.pickle'
    LOG_FILE_PATH = os.path.join(MODELS_DIR, MODEL_FILE_NAME)
    
    
'''
The following lines will be executed any time this .py file is run as a script or imported as a module.
'''
# Create a logger object. The root logger would be the parent of this logger
# Note that if you run this .py file as a script, this logger will not function, because it is not configured.
logger = logging.getLogger(__name__)