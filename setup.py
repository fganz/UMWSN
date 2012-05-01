from distutils.core import setup

setup(
    name='UMiddlewareWSNetworks',
    version='0.1',
    packages=['core', 'core.plugins', 'core.plugins.processing', 'core.plugins.abstraction'],
    url='https://github.com/fganz/UMWSN',
    license='LGPL',
    author='Frieder Ganz',
    author_email='f.ganz@surrey.ac.uk',
    description='Middleware for Wireless Sensor Networks',
    install_requires=['pandas','mako','numpy','pymongo','cherrypy','matplotlib','scipy','googlemaps','pywapi']
)
