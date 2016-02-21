from setuptools import find_packages, setup

setup(
    name='Flask-Copilot',
    version='0.1.0',
    author='Jon Banafato',
    author_email='jon@jonafato.com',
    description='',
    license='BSD',
    keywords='',
    url='',
    packages=find_packages(exclude=('docs', 'tests')),
    install_requires=(
        'Flask',
        'sortedcontainers',
    ),
)
