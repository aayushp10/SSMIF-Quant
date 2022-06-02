#!/usr/bin/env python3
"""
logger

initialize the logger

warning - don't use logger.success, as it won't work with spark
you can use the following:
logger.debug('a')
logger.info('b')
logger.warning('c')
logger.error('d')
logger.critical('e')
"""

import os
import sys
from urllib.parse import unquote
from typing import Optional, Union
from loguru import logger as loguru_logger
from loguru._logger import Logger
from pyspark import SparkContext
from py4j.java_gateway import JavaObject

sc: SparkContext = None
logger: Union[Logger, JavaObject] = None

LOADED: bool = False


def setup_logger() -> None:
    """
    setup application to run under spark
    """
    global LOADED
    global logger
    global sc

    if LOADED:
        logger.info('logger already initialized')
        return

    spark_indexes = [i for i, arg in enumerate(
        sys.argv) if arg in ['--spark', '-s']]

    if len(spark_indexes) not in [0, 1]:
        raise ValueError('invalid spark argument provided')

    if len(spark_indexes) == 0:
        logger = loguru_logger
        LOADED = True
        return

    # set environment variables
    spark_index = spark_indexes[0] + 1
    if spark_index < len(sys.argv) - 1:
        spark_env = sys.argv[spark_index]
        if len(spark_env) > 0 and not spark_env.startswith('-'):
            env_variables = {key: unquote(val) for (key, val) in [
                elem.split('=') for elem in spark_env.split(',')]}
            for key, val in env_variables.items():
                os.environ[key] = val

    sc = SparkContext.getOrCreate()
    log4jLogger = sc._jvm.org.apache.log4j
    logger = log4jLogger.LogManager.getLogger('factor-model')

    LOADED = True


# you always want to run setup_logger on import, so there shouldn't be a run catch block
setup_logger()
