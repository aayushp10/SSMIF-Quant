import pdblp
import os
import pandas as pd


def main():
    con = pdblp.BCon(timeout=10000)
    con.start()
    frame = con.bdh(['SPX Index'], ["PX_LAST"],
                    start_date="20180101", end_date="20181101")
    frame.to_csv("benchmark.csv")


if __name__ == "__main__":
    main()

"""
sometimes if bloomberg isn't working, run the following in your terminal and try again
start C:\blp\DAPI\bbcomm.exe
"""
