import os

def num_cpus():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

preload = True
workers = num_cpus() * 2 + 1
bind = '127.0.0.1:8000'
pid = '/home/guardabosques/GuardabosquesUSB/var/gunicorn.prod.pid'
django_settings = 'devlabs.settings.local'

# log files
accesslog = '/home/guardabosques/GuardabosquesUSB/server/gunicorn-access.log'
errorlog = '/home/guardabosques/GuardabosquesUSB/gunicorn-error.log'
loglevel = 'debug'
