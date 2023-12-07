# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    
    dates_formatted = [datetime.strptime(date_old, "%Y-%m-%d").strftime('%d %b %Y') for date_old in old_dates]
    
    return dates_formatted

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError()
    range_ = []
    k = datetime.strptime(start, '%Y-%m-%d')
    for i in range(n):
        range_.append(k + timedelta(days=i))
    return range_


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    
    date_range1 = date_range(start_date, len(values))
    return list(zip(date_range1, values))

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
        outfile."""
    headers_original = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    data_with_late_fees = defaultdict(float)
    
    with open(infile, 'r') as fl:
        linesData = DictReader(fl, fieldnames=headers_original)
        all_file = [row for row in linesData]

    all_file.pop(0)
    for line_in_file in all_file:
        patronID = line_in_file['patron_id']
        date_due_on = datetime.strptime(line_in_file['date_due'], "%m/%d/%Y")
        date_returned_on = datetime.strptime(line_in_file['date_returned'], "%m/%d/%Y")
        diff_days = (date_returned_on - date_due_on).days
        data_with_late_fees[patronID]+= 0.25 * diff_days if diff_days > 0 else 0.0
            
    tuned_rows = [
        {'patron_id': parton, 'late_fees': f'{lates:0.2f}'} for parton, lates in data_with_late_fees.items()
    ]
    with open(outfile, 'w') as fl_op:
        write_late_dates = DictWriter(fl_op,['patron_id', 'late_fees'])
        write_late_dates.writeheader()
        write_late_dates.writerows(tuned_rows)

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
