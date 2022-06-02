#!/usr/bin/env python3
"""
Spark config
"""

import os
import sys
import random
from pyspark import SparkContext

DIST: str = "dist.zip"


def get_rand(_curr_val: int) -> bool:
    """
    test function for calculating pi
    """
    x, y = random.random(), random.random()
    return x*x + y*y < 1


def test_spark(sc: SparkContext) -> float:
    """
    test to see if spark is working
    """
    num_samples = 100000
    count = sc.parallelize(range(0, num_samples)).filter(get_rand).count()
    pi = 4 * count / num_samples
    return pi


def main() -> None:
    """
    main entrypoint using spark
    """
    conda_prefix = os.getenv('CONDA_PREFIX')
    if conda_prefix is not None:
        os.environ['PYSPARK_PYTHON'] = os.path.join(
            conda_prefix, 'bin/python')

    sc = SparkContext.getOrCreate()
    sc.addPyFile(DIST)
    from utils.logger import logger
    logger.info(f'spark web ui: {sc.uiWebUrl}')
    # logger.info(f'pi is roughly {test_spark(sc)}')
    from main import main as factor_model_main
    try:
        factor_model_main()
    except Exception as err:
        logger.exception(err)
        sc.stop()
        sys.exit('error with factor model')
    sc.stop()


if __name__ == '__main__':
    main()
