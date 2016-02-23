from setuptools import find_packages, setup

setup(
    name='Flask-Copilot',
    version='0.2.0',
    author='Jon Banafato',
    author_email='jon@jonafato.com',
    description='Simple navbar generation for Flask applications.',
    license='BSD',
    keywords='flask navigation',
    url='https://github.com/jonafato/Flask-Copilot',
    packages=find_packages(exclude=('docs', 'tests')),
    install_requires=(
        'Flask',
        'sortedcontainers',
    ),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ),
)
