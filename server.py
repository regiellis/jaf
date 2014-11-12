#!/usr/bin/env python
# -*- coding; utf-8 -*-

"""
jaf.aerver
AUTHOR: Regi E.<regi@persona.io>
CREATE/UPDATED: 20141004
"""
from jaf import create_app
from termcolor import colored

app = create_app('production')
print("{}".format(colored("Gunicon Started", "green")))
