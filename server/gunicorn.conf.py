import os

def num_cpus():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

preload = True
workers = num_cpus() * 2 + 1
bind = '127.0.0.1:8000'
pid = '/home/kpantic/devlabs-test/var/gunicorn.prod.pid'
django_settings = 'devlabs.settings.local'

# log files
accesslog = '/home/kpantic/devlabs-test/server/gunicorn-access.log'
errorlog = '/home/kpantic/devlabs-test/server/gunicorn-error.log'
loglevel = 'debug'
