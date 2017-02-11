Arias
======

Quick Start
==========

```bash
# install deps
~ $ sudo apt-get install redis-server vim git python-dev -y
~ $ pip install virtualenv

# clone project
~ $ git clone https://github.com/micumatei/arias
~ $ cd arias

# create a virtual env for this project
~ arias/ $ virtualenv .venv/arias

# activate the venv
~ arias/ $ source .venv/arias/bin/activate

# install the project
~ arias/ $ pip install ../arias
~ arias/ $ python setup.py install

# genetare a config file
~ arias/ $ oslo-config-generator --config-file etc/arias/arias-config-generator.conf
~ arias/ $ sudo mkdir /etc/arias/

# copy the config file in /etc/arias
~ arias/ $ sudo cp etc/arias/arias.conf.sample /etc/arias/arias.conf
```
