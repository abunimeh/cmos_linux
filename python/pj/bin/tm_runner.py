"""
Author: Junxiu Liu @ CPU Verification Platform Group
Email: liujx@cpu.com.cn
Description: pj tm sub cmd entrence
"""

import pcom
import tm_log_parser

LOG = pcom.gen_logger(__name__)

def run_tm(args):
    """to run tm sub cmd"""
    if args.tm_report_file:
        tm_log_parser.TmParser(
            {"dt_file": args.tm_report_file,
             "level": args.tm_hier_level,
             "group": args.tm_path_group}).parse_tm_log()
    else:
        raise Exception("missing main arguments")
