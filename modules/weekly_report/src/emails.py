#!/usr/bin/env python3
"""
Make and send email
"""

from loguru import logger
from datetime import date
from ssmif_sdk.misc.report_file_path import get_file_path
from ssmif_sdk.models.users import Users
from ssmif_sdk.models.utils import initialize_databases
from ssmif_sdk.utils.emails import execute_send_email
from ssmif_sdk.utils.main import get_start_end_week


def send_email(report_date: date):
    """
    send email to email list
    """
    start_of_week, end_of_week = get_start_end_week(report_date)
    date_format = '%m/%d'
    start_week_str = start_of_week.strftime(date_format)
    end_week_str = end_of_week.strftime(date_format)
    subject = f'SSMIF Performance Report {start_week_str}-{end_week_str}'

    html_content = """
    <html>
    <head></head>
    <body>
    <p>Hello everyone,</p>
    <p>We hope you are doing well. Attached you will find a report
    detailing our fund's performance this past week, and a snapshot
    of our holdings.</p>
    <p>Kindly reach out to senior management with any questions or
    feedback. Thanks!</p>
    <p>Best,<br/>SSMIF SM
    </body>
    </html>
    """

    recipients = list(map(lambda member: member.email,
                          Users.select(Users.email).where(Users.receives_weekly_report)))

    weekly_report_path = get_file_path(report_date)
    execute_send_email(subject, recipients, html_content,
                       attachment_path=weekly_report_path)


@logger.catch(reraise=True)
def main():
    """
    main function for testing
    """
    initialize_databases()
    send_email(date.today())


if __name__ == '__main__':
    main()
