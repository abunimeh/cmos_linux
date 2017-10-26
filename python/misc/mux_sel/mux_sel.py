#! /usr/bin/env python3
"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: mux verilog code generation flow
"""

import os
import configparser
import argparse
import itertools
import pprint
import jinja2

def gen_args_top():
    """to parse mux_sel top arguments"""
    parser = argparse.ArgumentParser()
    h_str = ("input mux config file")
    parser.add_argument('-mf', dest='mux_file', required=True, help=h_str)
    h_str = ("input ins config files")
    parser.add_argument('-if', dest='ins_file_lst', required=True, nargs='+', help=h_str)
    return parser.parse_args()

def ren_tempfile(temp_in, temp_out, temp_dic):
    """to render jinja2 template files"""
    template_loader = jinja2.FileSystemLoader(os.path.dirname(temp_in))
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(os.path.basename(temp_in))
    with open(temp_out, "w") as ttf:
        ttf.write(template.render(temp_dic))

class MuxProc(object):
    """mux processor class"""
    def __init__(self, mux_cfg_file):
        self.mux_cfg = mux_cfg = configparser.ConfigParser(allow_no_value=True, delimiters=("="))
        self.mux_cfg.optionxform = str
        self.mux_cfg.read(mux_cfg_file)
        self.mapping_cfg = mux_cfg["mapping"]
        self.level_lst = [c_c for c_c in mux_cfg.sections() if c_c.startswith("level_")]
        self.level_lst.sort()
        self.path_dic = {}
    def pre_order(self, level_i, pre_v, s_n, e_n):
        """pre order traveral recursive function"""
        if level_i >= len(self.level_lst):
            return "miss"
        se_key = f"{s_n}_{e_n}"
        level_str = self.mux_cfg[self.level_lst[level_i]].get(pre_v, "")
        for m_v in level_str.split(","):
            m_v = m_v.strip()
            self.path_dic[se_key].append(m_v)
            if m_v == e_n:
                self.mux_cfg[self.level_lst[level_i]][pre_v] = m_v
                return "hit"
            else:
                rec = self.pre_order(level_i+1, m_v, s_n, e_n)
                if rec == "hit":
                    self.mux_cfg[self.level_lst[level_i]][pre_v] = m_v
                    return "hit"
            self.path_dic[se_key].pop()
    def proc_mux_cfg(self, s_n, e_n):
        """pre order wrapper function"""
        se_key = f"{s_n}_{e_n}"
        self.path_dic[se_key] = []
        for root_v in self.mux_cfg[self.level_lst[0]]["root"].split(","):
            root_v = root_v.strip()
            if root_v != s_n:
                continue
            self.path_dic[se_key].append(root_v)
            self.pre_order(1, root_v, s_n, e_n)
        if self.path_dic[se_key] == [s_n]:
            print(f"Warning: path from {s_n} to {e_n} not found")
            del self.path_dic[se_key]
    def proc_ins_dic(self, ins_dic):
        """to process ins dic for ins file config"""
        for ins_k, ins_v in ins_dic["ins"].items():
            self.proc_mux_cfg(ins_k, ins_v)
        # pprint.pprint([dict(cc) for _, cc in self.mux_cfg.items()])
        n_lst = []
        for _, p_lst in self.path_dic.items():
            for p_i in range(len(p_lst)-1):
                node_name = "_".join(p_lst[p_i:p_i+2])
                if node_name not in n_lst:
                    n_lst.append(node_name)
        return n_lst, ins_dic.get("con_str", "")

class InsProc(object):
    """ins cfg processor class"""
    def __init__(self, mux_cfg_file, ins_file):
        self.mux_cfg_file = mux_cfg_file
        self.ins_file = ins_file
        self.ins_cfg = configparser.ConfigParser(allow_no_value=True, delimiters=("="))
        self.ins_cfg.optionxform = str
        self.ins_cfg.read(ins_file)
        self.con_lst = [c_c for c_c in self.ins_cfg.sections() if c_c.startswith("con_")]
        self.top_dic = {}
        self.wire_lst = []
        self.assign_dic = {}
    def proc_sin_range(self, ins_dic, var_dic_lst, sec_tup):
        """to process range condition single cycle"""
        ins_dic = {"con_str": "", "ins": {}}
        m_p = MuxProc(self.mux_cfg_file)
        mapping_cfg = (
            self.ins_cfg["mapping"] if self.ins_cfg.has_section("mapping") else
            m_p.mapping_cfg)
        for v_i, var_dic in enumerate(var_dic_lst):
            am_k = f"{var_dic['v_name']}__h_{hex(sec_tup[v_i])[2:]}"
            am_v = (
                f"({var_dic['name']}=="
                f"{var_dic['width']}'h{hex(sec_tup[v_i])[2:]}) ? 1'b1 : 1'b0")
            ins_dic["con_str"] += (f" & {am_k}")
            self.assign_dic[am_k] = am_v
            self.wire_lst.append(am_k)
            for ins_k, ins_v in self.ins_cfg["ins"].items():
                if var_dic["name"] not in ins_v:
                    continue
                ins_v = ins_v.replace(var_dic["name"], str(sec_tup[v_i]))
                ins_v = str(eval(ins_v))
                if ins_v not in mapping_cfg:
                    print(f"Warning: node {ins_v} not in mapping range")
                    continue
                ins_dic["ins"][ins_k] = mapping_cfg[ins_v]
        node_lst, con_str = m_p.proc_ins_dic(ins_dic)
        self.wire_lst.extend(node_lst)
        in_k = os.path.splitext(os.path.basename(self.ins_file))[0]
        self.wire_lst.append(in_k)
        self.top_dic[f"{in_k}{con_str}"] = node_lst
    def proc_range(self):
        """to process range condition"""
        var_dic_lst = []
        range_lst = []
        for sec_k, sec_v in self.ins_cfg["range"].items():
            sec_v_lst = [c_c.strip() for c_c in sec_v.split(",")]
            range_lst.append(range(int(sec_v_lst[0]), int(sec_v_lst[1])+1))
            v_name = sec_k.replace("[", "_").replace("]", "_").replace(":", "_")
            var_dic_lst.append({"name": sec_k, "width": sec_v_lst[2], "v_name": v_name})
        for sec_tup in itertools.product(*range_lst):
            if not self.con_lst:
                self.proc_sin_range({"con_str": "", "ins": {}}, var_dic_lst, sec_tup)
            else:
                for con in self.con_lst:
                    pre_con = self.ins_cfg[con].pop("con_str")
                    self.ins_cfg["ins"].update(self.ins_cfg[con])
                    self.proc_sin_range(
                        {"con_str": f" & ({pre_con})", "ins": {}}, var_dic_lst, sec_tup)
                    self.ins_cfg[con]["con_str"] = pre_con
    def proc_con(self):
        """to process con condition"""
        for con in self.con_lst:
            ins_dic = {"con_str": f" & ({self.ins_cfg[con].pop('con_str')})", "ins": {}}
            self.ins_cfg["ins"].update(self.ins_cfg[con])
            m_p = MuxProc(self.mux_cfg_file)
            mapping_cfg = (
                self.ins_cfg["mapping"] if self.ins_cfg.has_section("mapping") else
                m_p.mapping_cfg)
            for ins_k, ins_v in self.ins_cfg["ins"].items():
                if ins_v not in mapping_cfg:
                    print(f"Warning: node {ins_v} not in mapping range")
                    continue
                ins_dic["ins"][ins_k] = mapping_cfg[ins_v]
            node_lst, con_str = m_p.proc_ins_dic(ins_dic)
            self.wire_lst.extend(node_lst)
            in_k = os.path.splitext(os.path.basename(self.ins_file))[0]
            self.wire_lst.append(in_k)
            self.top_dic[f"{in_k}{con_str}"] = node_lst
    def proc_normal(self):
        """to process normal condition"""
        m_p = MuxProc(self.mux_cfg_file)
        mapping_cfg = (
            self.ins_cfg["mapping"] if self.ins_cfg.has_section("mapping") else m_p.mapping_cfg)
        ins_dic = {"con_str": "", "ins": {}}
        for ins_k, ins_v in self.ins_cfg["ins"].items():
            if ins_v not in mapping_cfg:
                print(f"Warning: node {ins_v} not in mapping range")
                continue
            ins_dic["ins"][ins_k] = mapping_cfg[ins_v]
        node_lst, con_str = m_p.proc_ins_dic(ins_dic)
        self.wire_lst.extend(node_lst)
        in_k = os.path.splitext(os.path.basename(self.ins_file))[0]
        self.wire_lst.append(in_k)
        self.top_dic[f"{in_k}{con_str}"] = node_lst
    def proc_ins_cfg(self):
        """top function to process ins file config"""
        if self.ins_cfg.has_section("range"):
            self.proc_range()
        elif self.con_lst:
            self.proc_con()
        else:
            self.proc_normal()
        return self.top_dic, self.wire_lst, self.assign_dic

class CodeGen(object):
    """code generator class"""
    def __init__(self, top_dic, wire_lst, assign_dic):
        self.top_dic = top_dic
        self.wire_lst = []
        for wire_name in wire_lst:
            if wire_name not in self.wire_lst:
                self.wire_lst.append(wire_name)
        self.assign_dic = assign_dic
    def gen_temp_dic(self):
        """to re-org node dic into template dic"""
        for node_k, node_v_lst in self.top_dic.items():
            for node in node_v_lst:
                if node not in self.assign_dic:
                    self.assign_dic[node] = ""
                if node_k not in self.assign_dic[node]:
                    self.assign_dic[node] = (
                        f"{self.assign_dic[node]} | {node_k.strip()}".strip("| "))
    def gen_code(self):
        """to generate verilog code by using jinja2 template"""
        self.gen_temp_dic()
        exec_dir = os.path.dirname(__file__)
        ren_tempfile(
            f"{exec_dir}{os.sep}temp_in.v", f"{exec_dir}{os.sep}temp_out.v",
            {"wire_lst": self.wire_lst, "assign_dic": self.assign_dic})

def main():
    """mux_sel main entrance"""
    args = gen_args_top()
    if not os.path.isfile(args.mux_file):
        os.sys.exit(f"mux config file {args.mux_file} is NA")
    top_dic = {}
    wire_lst = []
    assign_dic = {}
    for i_file in args.ins_file_lst:
        if not os.path.isfile(i_file):
            print(f"Warning: ins config file {i_file} is NA")
        t_d, w_l, am_d = InsProc(args.mux_file, i_file).proc_ins_cfg()
        top_dic.update(t_d)
        wire_lst.extend(w_l)
        assign_dic.update(am_d)
    CodeGen(top_dic, wire_lst, assign_dic).gen_code()

if __name__ == "__main__":
    main()
