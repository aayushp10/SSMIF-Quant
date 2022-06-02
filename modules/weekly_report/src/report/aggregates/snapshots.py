#!/usr/bin/env python3
"""
Get the aggregate snapshots data
"""
#################################
# for handling relative imports #
#################################
if __name__ == '__main__':
    import sys
    from pathlib import Path
    current_file = Path(__file__).resolve()
    root = next(elem for elem in current_file.parents
                if str(elem).endswith('/src'))
    sys.path.append(str(root))
    # remove the current file's directory from sys.path
    try:
        sys.path.remove(str(current_file.parent))
    except ValueError:  # Already removed
        pass
#################################

from datetime import date
from loguru import logger
from typing import List, Optional
from ssmif_sdk.compute.snapshot import Snapshot
from ssmif_sdk.models.utils import initialize_databases
from ssmif_sdk.models.current_holdings import get_current_holdings


class AggregateSnapshots:
    """
    aggregate snapshots helper class
    """

    def __init__(self, today: Optional[date] = None):
        if today is None:
            today = date.today()
        logger.info('getting snapshots')
        current_holdings = get_current_holdings()
        if len(current_holdings) == 0:
            raise RuntimeError('could not find any current holdings...')

        self.snapshots: List[Snapshot] = [Snapshot(ticker, today=today)
                                          for ticker in current_holdings]
        self.total_invested_amount = sum(
            [snap.invested_amount for snap in self.snapshots])
        self.total_value_mtm = sum(
            [snap.current_value_mtm for snap in self.snapshots])
        self.total_month_open = sum(
            [snap.month_open_value for snap in self.snapshots])
        self.total_year_open = sum(
            [snap.year_open_value for snap in self.snapshots])

    def __str__(self) -> str:
        """
        to string method
        """
        return f'num snapshots: {len(self.snapshots)}'

    def __repr__(self) -> str:
        """
        return tostring representation
        """
        return str(self)


@logger.catch(reraise=True)
def main():
    """
    main function for testing
    """
    initialize_databases()
    snapshots = AggregateSnapshots()
    logger.info(snapshots)


if __name__ == '__main__':
    main()
