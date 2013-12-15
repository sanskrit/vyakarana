# -*- coding: utf-8 -*-
"""
    vyakarana.fabfile
    ~~~~~~~~~~~~~~~~~

    Helpful commands for debugging and testing.

    :license: MIT and BSD
"""

import code
from fabric.api import *
from vyakarana.ashtadhyayi import Ashtadhyayi

PROJECT_NAME = 'vyakarana'


@task
def shell():
    """Create an interactive shell with some useful locals."""

    banner = """
    {1}~~~~~~
    {0} shell
    {1}~~~~~~
    """.format(PROJECT_NAME, '~' * len(PROJECT_NAME))

    a = Ashtadhyayi()
    context = {
        'a': a,
        'rules': a.rules,
    }
    for rule in a.rules:
        context['r' + rule.name.replace('.', '_')] = rule

    code.interact(banner, local=context)
