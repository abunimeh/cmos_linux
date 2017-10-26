"""
Author: Junxiu Liu @ CPU Verification Platform Group
Email: liujx@cpu.com.cn
Description: TmParser class for parsing dc timing related logs
"""

import os
import re
import fnmatch
import collections
import texttable
import pcom

LOG = pcom.gen_logger(__name__)

class TmParser(object):
    """dc flow timing log parser"""
    def __init__(self, tm_dic):
        self.tm_dic = tm_dic
        self.tm_dic["dt_file"] = os.path.abspath(os.path.expandvars(tm_dic["dt_file"]))
        self.sum_dic = {
            "l_dic": {},
            "nl_dic": {},
            "sum_nl_dic": collections.defaultdict(list),
            "sum_l_dic": collections.defaultdict(list)}
    @classmethod
    def statistics_sum(cls, k_tuple, sum_dic, slack_str):
        """to sum up the statistics of timing violations"""
        slack_value = float(slack_str)
        if k_tuple not in sum_dic:
            sum_dic[k_tuple].append(1)
        else:
            sum_dic[k_tuple][0] = sum_dic[k_tuple][0]+1
        if len(sum_dic[k_tuple]) == 1:
            sum_dic[k_tuple].append([0, 0, 0, 0, 0, 0])
        if slack_value > -0.05:
            sum_dic[k_tuple][1][0] = sum_dic[k_tuple][1][0]+1
        if slack_value > -0.1:
            sum_dic[k_tuple][1][1] = sum_dic[k_tuple][1][1]+1
        elif slack_value > -0.3:
            sum_dic[k_tuple][1][2] = sum_dic[k_tuple][1][2]+1
        elif slack_value > -0.5:
            sum_dic[k_tuple][1][3] = sum_dic[k_tuple][1][3]+1
        elif slack_value > -1.0:
            sum_dic[k_tuple][1][4] = sum_dic[k_tuple][1][4]+1
        elif slack_value <= -1.0:
            sum_dic[k_tuple][1][5] = sum_dic[k_tuple][1][5]+1
    @classmethod
    def gen_table(cls, sum_dic):
        """to generate ASCII table by using texttable module"""
        table = texttable.Texttable()
        rows = [
            ["group", "Startpoint", "Endpoint", "num", "-50", "-100", "-300", "-500", "-1000", "~"]]
        for dic_k, dic_v in sum_dic.items():
            rows.append(
                [dic_k[0], dic_k[1], dic_k[2], dic_v[0], dic_v[1][0], dic_v[1][1],
                 dic_v[1][2], dic_v[1][3], dic_v[1][4], dic_v[1][5]])
        align_lst = ["c", "l", "l", "c", "c", "c", "c", "c", "c", "c"]
        valign_lst = ["m", "m", "m", "m", "m", "m", "m", "m", "m", "m"]
        cols_width = [7, 20, 20, 8, 8, 8, 8, 8, 8, 8]
        table.set_cols_align(align_lst)
        table.set_cols_valign(valign_lst)
        table.set_cols_width(cols_width)
        table.add_rows(rows)
        return table.draw()
    def parse_tm(self):
        """to parse dc timing log"""
        if not os.path.isfile(self.tm_dic["dt_file"]):
            return
        slk_pat = re.compile(r"(.*?)\s*\(.*\)\s*(.*)")
        with open(self.tm_dic["dt_file"]) as dtf:
            blk_flag = False
            for line in dtf:
                line = line.strip()
                if line.startswith("Startpoint:"):
                    blk_flag = True
                    blk_dic = {}
                if not blk_flag:
                    continue
                line_lst = line.split(":")
                if line_lst[0] in ("Startpoint", "Endpoint", "Path Group"):
                    blk_dic[line_lst[0]] = line_lst[1].strip()
                if line.startswith("slack "):
                    blk_flag = False
                    mop = pcom.REOpter(line)
                    if mop.match(slk_pat):
                        if float(mop.group(2)) >= 0:
                            continue
                        bpg = blk_dic["Path Group"]
                        if self.tm_dic["group"] and (
                                not any(fnmatch.fnmatch(bpg, cc) for cc in self.tm_dic["group"])):
                            continue
                        if "in2" in bpg or "2out" in bpg:
                            nl_dic = self.sum_dic["nl_dic"]
                            nl_dic[bpg] = nl_dic[bpg]+1 if bpg in nl_dic else 1
                            self.statistics_sum(
                                (blk_dic["Path Group"], blk_dic["Startpoint"],
                                 blk_dic["Endpoint"]), self.sum_dic["sum_nl_dic"], mop.group(2))
                        else:
                            l_dic = self.sum_dic["l_dic"]
                            l_dic[bpg] = l_dic[bpg]+1 if bpg in l_dic else 1
                            spt_lst = blk_dic["Startpoint"].split("/")
                            ept_lst = blk_dic["Endpoint"].split("/")
                            spt = os.path.join(*spt_lst[0:self.tm_dic["level"]])
                            ept = os.path.join(*ept_lst[0:self.tm_dic["level"]])
                            self.statistics_sum(
                                (blk_dic["Path Group"], spt, ept),
                                self.sum_dic["sum_l_dic"], mop.group(2))
                    else:
                        LOG.info("line %s is not matched pattern %s", line, slk_pat)
    def gen_tm_table(self):
        """to generate dc timing ASCII table"""
        LOG.info("generating Path_Group sum table")
        pg_rows = [
            ["Path_Group"],
            [sum(self.sum_dic["l_dic"].values())+sum(self.sum_dic["nl_dic"].values())]]
        for nl_k, nl_v in self.sum_dic["nl_dic"].items():
            pg_rows[0].append(nl_k)
            pg_rows[1].append(nl_v)
        for l_k, l_v in self.sum_dic["l_dic"].items():
            pg_rows[0].append(l_k)
            pg_rows[1].append(l_v)
        sum_table = texttable.Texttable()
        sum_table.add_rows(pg_rows)
        total_table = sum_table.draw()
        LOG.info("generating path group summary table")
        LOG.info(f"{sum_table.draw()}{os.linesep*2}")
        LOG.info("generating no level table")
        nl_table = self.gen_table(self.sum_dic["sum_nl_dic"])
        LOG.info(f"{nl_table}{os.linesep*2}")
        LOG.info("generating level table")
        lev_table = self.gen_table(self.sum_dic["sum_l_dic"])
        LOG.info(lev_table)
        tmf_str = (
            f"path group table{os.linesep}{total_table}{os.linesep*2}"
            f"no hierarchy level table{os.linesep}{nl_table}{os.linesep*2}"
            f"hierarchy level table{os.linesep}{lev_table}{os.linesep}")
        with open(f"{os.path.dirname(self.tm_dic['dt_file'])}{os.sep}sum_tm", "w") as tmf:
            tmf.write(tmf_str)
    def parse_tm_log(self):
        """top execution function"""
        self.parse_tm()
        self.gen_tm_table()
