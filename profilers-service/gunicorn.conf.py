# gunicorn_config.conf
workers = 1  # Number of worker processes
bind = "0.0.0.0:5000"  # IP and port to bind
timeout = 300  # Maximum time a request is allowed to process
reload = True