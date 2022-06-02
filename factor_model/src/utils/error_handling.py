#!/usr/bin/env python3
"""
Handle Errors
"""
from inspect import getfile, getsourcefile, cleandoc, getsourcelines
from os.path import abspath
from loguru import logger
from functools import wraps


def HandleErrors(f):
    """
    Decorator to handle errors more gracefully
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)

        except Exception as err:
            logger.error(f"Error rasied at: {abspath(getfile(f))}")
            logger.error(f"Of Type: {err.__class__}")
            logger.error(f"For Function: {f.__name__}")
            logger.error(f"Defined at: {getsourcefile(f)}")
            logger.error(f"On Line: {getsourcelines(f)[1]}")
            raise err
    return wrap
