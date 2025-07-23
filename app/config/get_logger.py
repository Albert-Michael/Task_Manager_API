import logging

def get_logger(name='app_logger', log_file='task_app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    #prevent duplicate handlers
    if logger.handlers:
        return logger
    

# define log message format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a file handler to write logs to a file
    file_handler = logging.FileHandler('task_app.log')
    file_handler.setFormatter(formatter)  # Set the format for the log messages
    logger.addHandler(file_handler)  # Add the file handler to the logger

#Stream Handler to log in console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

#Prevent duplicate logs in console
    logger.propagate = False
    return logger 