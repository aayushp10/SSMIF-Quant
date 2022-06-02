#!/usr/bin/env python3
"""
Run the weekly report builder
"""

##################################
# for handling relative imports  #
# compatible with lambda runtime #
##################################
if __name__ != '__main__':
    import sys
    from pathlib import Path
    current_file = Path(__file__).resolve()
    root = next(elem for elem in current_file.parents
                if str(elem).endswith('/src'))
    sys.path.append(str(root))
#################################

from ssmif_sdk.models.utils import initialize_databases
from loguru import logger
from report.build import BuildExcel
from save_s3 import save_s3
from emails import send_email


def main():
    """
    main entrypoint
    """
    initialize_databases()
    generated_report = BuildExcel()
    save_s3(generated_report.today)
    send_email(generated_report.today)


def lambda_handler(_event, _context):
    """
    handler for aws lambda
    """
    main()


@logger.catch(reraise=True)
def run_main():
    """
    run main function for testing
    """
    initialize_databases()
    generated_report = BuildExcel()
    save_s3(generated_report.today)
    send_email(generated_report.today)


if __name__ == '__main__':
    run_main()
