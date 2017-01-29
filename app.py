#!/usr/bin/env python
import imp
import os
import sys

PYCART_DIR = ''.join(['python-', '.'.join(map(str, sys.version_info[:2]))])


try:
   zvirtenv = os.path.join(os.environ['OPENSHIFT_HOMEDIR'], PYCART_DIR,
                           'virtenv', 'bin', 'activate_this.py')
   exec(compile(open(zvirtenv).read(), zvirtenv, 'exec'),
        dict(__file__ = zvirtenv) )
except:
   pass


def run_simple_httpd_server(app, ip, port=8080):
   from wsgiref.simple_server import make_server
   make_server(ip, port, app).serve_forever()


#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
# 


#
#  main():
#
'''
from threading import Timer
from wsgi.application import Tu
def retronombri():
  Timer(1.0, retronombri).start()
  Tu.update(tempoO=Tu.tempoO-1).where(Tu.vico==Tu.uzantoO).execute()
  Tu.update(tempoX=Tu.tempoX-1).where(Tu.vico==Tu.uzantoX).execute()
retronombri()
'''
if __name__ == '__main__' and 'OPENSHIFT_REPO_DIR' in os.environ:
   ip   = os.environ['OPENSHIFT_PYTHON_IP']
   port = 8080
   zapp = imp.load_source('application.py', 'wsgi/application.py')

   print('Starting WSGIServer on %s:%d ... ' % (ip, port))
   run_simple_httpd_server(zapp.application, ip, port)
elif __name__ == '__main__':   
    zapp = imp.load_source('application.py', 'wsgi/application.py')
    run_simple_httpd_server(zapp.application, 'localhost', 8080)
