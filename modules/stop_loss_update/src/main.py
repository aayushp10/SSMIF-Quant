#!/usr/bin/env python3
"""
stop loss update script
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

import pandas as pd
from loguru import logger
from tabulate import tabulate
from typing import Optional, List
from datetime import date
from ssmif_sdk.models.current_holdings import get_current_holdings
from ssmif_sdk.models.stop_loss import Stop_Loss
from ssmif_sdk.models.users import Users
from ssmif_sdk.models.utils import initialize_databases
from ssmif_sdk.utils.stop_losses import get_stop_loss_prices
from ssmif_sdk.utils.stock_price import get_stock_timeframe
from ssmif_sdk.utils.main import get_start_end_week
from ssmif_sdk.utils.emails import execute_send_email


def get_stop_loss_data(today: Optional[date] = None) -> str:
    """
    Check Stop Loss Status of all assets and send email report
    """
    if today is None:
        today = date.today()

    start_date, end_date = get_start_end_week(today)
    if today < end_date:
        raise ValueError('script only runs at the end of the week')

    stop_loss_cross_ticker = {}

    # to compare the data to the stoplosses
    for ticker in get_current_holdings():
        count = 0
        stop_loss_cross_day = {}

        current_stop_loss_data = Stop_Loss.select().where(
            Stop_Loss.ticker == ticker).get()
        current_stop_losses = get_stop_loss_prices(ticker, current_stop_loss_data.risk_ratio,
                                                   current_stop_loss_data.date, today)
        prices = get_stock_timeframe(
            ticker, start_date, end_date, today=today).values()

        for price, current_date in prices:
            if price <= current_stop_losses[2]:
                stop_loss_cross_day[
                    current_date] = f"Stop&nbsp;3:&nbsp;{current_stop_losses[2]:.2f}<br>&emsp;{price:.2f}"
            elif price <= current_stop_losses[1]:
                stop_loss_cross_day[
                    current_date] = f"Stop&nbsp;2:&nbsp;{current_stop_losses[1]:.2f}<br>&emsp;{price:.2f}"
            elif price <= current_stop_losses[0]:
                stop_loss_cross_day[
                    current_date] = f"Stop&nbsp;1:&nbsp;{current_stop_losses[0]:.2f}<br>&emsp;{price:.2f}"
            else:
                count += 1
                stop_loss_cross_day[current_date] = f'No&nbsp;Stop:&nbsp;<br>&emsp;{price:.2f}'
        if count < 5:
            stop_loss_cross_ticker[ticker] = stop_loss_cross_day

    if len(stop_loss_cross_ticker) == 0:
        logger.info('No Stop Loss Cross')
        return ''

    # make df and send email
    df = pd.DataFrame(stop_loss_cross_ticker)
    df = df.T
    logger.info(tabulate(df, tablefmt='simple',
                         headers='keys', stralign='center'))

    return df.to_html(escape=False, justify='left', border=1)


def send_email(table: str, report_date: Optional[date] = None, recipients: Optional[List[str]] = None) -> None:
    """
    send email to email list
    """
    if report_date is None:
        report_date = date.today()

    start_of_week, end_of_week = get_start_end_week(report_date)
    date_format = '%m/%d'
    start_week_str = start_of_week.strftime(date_format)
    end_week_str = end_of_week.strftime(date_format)
    subject = f'SSMIF Stop Loss Report {start_week_str}-{end_week_str}'

    html_content = f"""
    <html>
    <head></head>
    <body>
    <p>Hello everyone,</p>
    <p>We hope you are suffering only mildly. Below you will find a report
    detailing our fund's Stop Loss statuses for this past week.</p>
    <p>Kindly reach out to Quant Asset Allocation with any questions or
    feedback. Thanks!</p>
    <p>Best,<br/>Asset Allocation
    {table}
    </body>
    </html>
    """

    if recipients is None:
        recipients = list(map(lambda member: member.email,
                              Users.select(Users.email).where(Users.receives_weekly_report)))

    execute_send_email(subject, recipients, html_content)


def lambda_handler(_event, _context) -> str:
    """
    handler for aws lambda
    """
    initialize_databases()
    html_body = get_stop_loss_data()
    if len(html_body) == 0:
        return 'no stop loss updates for this time interval'
    send_email(html_body)
    return 'sent stop loss updates'


@logger.catch(reraise=True)
def main():
    """
    main function
    """
    initialize_databases()
    html_body = get_stop_loss_data(date(2021, 4, 11))
    if len(html_body) > 0:
        logger.info(html_body)
        # uncomment next line if you want to send the email
        # send_email(html_body, recipients=['email@example.com'])


if __name__ == "__main__":
    main()
