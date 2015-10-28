#!/usr/bin/python

import argparse
import sys
import time
from htmlstat import htmlstat, drudge
from datetime import datetime
from time import mktime


DEFAULT_SAMPLE_RATE = 10

def main(args):
    """
    Main program
    :param args: command line args
    """
    begin_time = time.strptime(args.begin_date, "%Y/%m/%d")
    end_time = time.strptime(args.end_date, "%Y/%m/%d")
    samples = DEFAULT_SAMPLE_RATE
    if args.samples is not None:
        samples = args.samples

    begin_date = datetime.fromtimestamp(mktime(begin_time))
    end_date = datetime.fromtimestamp(mktime(end_time))
    d = drudge.DrudgeSelector(begin_date, end_date, samples)
    results = d.query()
    counter = htmlstat.HrefCounter()
    counter.parse_contents_list(results)

    print "Top Ten:"
    for url, cnt in counter.top_ten():
        print("{0:>3} {1}".format(cnt, url))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("begin_date", help="Date to start gathering results (YYYY/MM/DD)")
    parser.add_argument("end_date", help="Date to stop gathering results (YYYY/MM/DD)")
    parser.add_argument("-s", dest="samples", help="Change number of samples to get")
    args = parser.parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception as e:
        print "Error: {0}".format(e)
        sys.exit(1)
    sys.exit(0)