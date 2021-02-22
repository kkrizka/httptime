import sys, os
import datetime
import logging
import http.client

def enable_logging(outfile=None):
    """
    Enable logging of all `http.client` requests via the 
    `logging` module.

    If `outfile` is `None`, then the filename is built using the
    program name and current time. The results are saved to
    `~/.httptime/argv[0]_%Y-%m-%d %H:%M:%SZ%z.txt`.

    Currently all of `logger` messages are saved to `outfile`.

    Parameters:
     `outfile`: Path where the output will be saved.
    """

    if outfile==None: # Automatic location
        odir=os.path.expanduser('~/.httptime')
        prog=os.path.basename(sys.argv[0])
        date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%SZ%z')
        outfile=f'{odir}/{prog}-{date}.txt'
        if not os.path.exists(odir):
            os.makedirs(odir)
    
    logging.basicConfig(filename=outfile,
                            filemode='w',
                            format='%(asctime)s.%(msecs)03d\t%(name)s\t%(levelname)s\t%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)

    #
    # Use logger for http.client
    # Credit: https://stackoverflow.com/questions/16337511/log-all-requests-from-the-python-requests-module
    httpclient_logger = logging.getLogger("http.client")
    def httpclient_log(*args):
        httpclient_logger.log(logging.DEBUG, " ".join(args))

    # mask the print() built-in in the http.client module to use
    # logging instead
    http.client.print = httpclient_log
    # enable debugging
    http.client.HTTPConnection.debuglevel = 1
