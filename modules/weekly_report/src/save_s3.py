#!/usr/bin/env python3
"""
Save report to s3
"""

from loguru import logger
from datetime import date
from os.path import join, basename
from ssmif_sdk.misc.report_file_path import get_file_path
from ssmif_sdk.utils.aws import s3_client
from ssmif_sdk.utils.config import REPORTS_S3_BUCKET
from ssmif_sdk.utils.constants import PERFORMANCE_REPORTS_FOLDER


def save_s3(report_date: date) -> None:
    """
    send email to email list
    """
    file_path = get_file_path(report_date)
    file_name = basename(file_path)
    logger.info(f'saving report {file_name}')
    with open(file_path, 'rb') as report_file:
        s3_client.put_object(Body=report_file, Bucket=REPORTS_S3_BUCKET, Key=join(
            PERFORMANCE_REPORTS_FOLDER, file_name))
    logger.info('done saving report to s3')


@logger.catch(reraise=True)
def main():
    """
    main function for testing
    """
    save_s3(date.today())


if __name__ == '__main__':
    main()
