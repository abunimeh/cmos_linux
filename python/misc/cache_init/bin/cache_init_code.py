#! /usr/bin/env python3
""" cache initial code"""
import os
import re
import itertools
import configparser
from jinja2 import Template
from  nested_dict import nested_dict

def gen_cfg(cfg_file_iter, dlts=("=", ":")):
    """to generate pj system config by reading config files"""
    config = configparser.ConfigParser(allow_no_value=True, delimiters=dlts)
    config.optionxform = str
    config.SECTCRE = re.compile(r"\[\s*(?P<header>[^]]+?)\s*\]")
    for cfg_file in cfg_file_iter:
        config.read(cfg_file)
    return config

class CacheInitialCode(object):
    """cache initial for Pj"""
    def __init__(self, cache_cfg_file):
        self.cache_str = ""
        self.cache_type = ""
        self.cache_cfg_file = cache_cfg_file
        self.section_dic = nested_dict()

    def gen_template(self, templt_lst, range_lst, format_lst):
        """gen template"""
        for templt_str in templt_lst:
            template = Template(templt_str)
            if range_lst:
                for items_lst in itertools.product(*range_lst[1]):
                    temp_dic = {}
                    for index, item in enumerate(range_lst[0]):
                        temp_dic[item] = items_lst[index]
                    if format_lst:
                        for fmt_idx, templt in enumerate(format_lst[1]):
                            temp_dic[format_lst[0][fmt_idx]] = Template(templt).render(temp_dic)
                    self.cache_str += "  "
                    self.cache_str += template.render(temp_dic)
                    self.cache_str += "\n"
            else:
                temp_dic = {}
                self.cache_str += "  "
                self.cache_str += template.render(temp_dic)
                self.cache_str += "\n"

    def gen_template_input(self):
        """gen template data format"""
        core_tuple = self.section_dic.get("core_id", None)
        for section, section_dic in self.section_dic.items():
            if section == "core_id":
                continue
            addr_range = section_dic.get("range_addr", None)
            if addr_range:
                addr_end = addr_range[1] + 1
                self.cache_str += f"for (int i=0; i<{addr_end}; i++) begin\n"
            lines_lst = section_dic.get("lines", None)
            range_lst = section_dic.get("range", None)
            format_lst = section_dic.get("format", None)
            if core_tuple:
                if range_lst:
                    range_lst[0].insert(0, "core_id")
                    range_lst[1].insert(0, core_tuple)
                else:
                    range_lst = [["core_id"], [core_tuple]]
            self.gen_template(lines_lst, range_lst, format_lst)
            self.cache_str += "end\n\n"

    def cfg_format_transfer(self):
        """format data constructure """
        config = gen_cfg([self.cache_cfg_file])
        for section in config.sections():
            for item in config[section]:
                item_val = config[section][item]
                if section.endswith("core"):
                    item_val = eval(item_val)
                    self.section_dic["core_id"] = range(item_val[0], item_val[1]+1)
                else:
                    if item.endswith("addr"):
                        self.section_dic[section]["range_addr"] = eval(item_val)
                        continue
                    if item.startswith("range"):
                        type_key = "range"
                        item = f'{item.split("_")[1]}_id'
                        item_val = eval(item_val)
                        item_val = range(item_val[0], item_val[1]+1)
                    elif item.startswith("format"):
                        type_key = "format"
                    elif item.startswith("line"):
                        if self.section_dic[section]["lines"]:
                            self.section_dic[section]["lines"].append(item_val)
                        else:
                            self.section_dic[section]["lines"] = [item_val]
                        continue
                    if self.section_dic[section][type_key]:
                        self.section_dic[section][type_key][0].append(item)
                        self.section_dic[section][type_key][1].append(item_val)
                    else:
                        self.section_dic[section][type_key] = [[item], [item_val]]

def run_cache(cache_cfg_dir):
    """gen all configs to .sv file"""
    for cache_cfg_file in os.listdir(cache_cfg_dir)[:1]:
        print(cache_cfg_file)
        cache_initial = CacheInitialCode(f"{cache_cfg_dir}/{cache_cfg_file}")
        cache_initial.cfg_format_transfer()
        cache_initial.gen_template_input()
        cache_cfg_nm = cache_cfg_file.split(".cfg")[0]
        with open(f"../output/{cache_cfg_nm}.sv", "w") as file:
            file.write(cache_initial.cache_str)

if __name__ == "__main__":
    run_cache(os.path.abspath("../input/"))
