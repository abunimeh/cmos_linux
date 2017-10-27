"""
Author: Huan Chen @ CPU Verification Platform Group
Email: chenh@cpu.com.cn
Description: pj reg sub cmd entrence
"""

import os
import re
import json
from collections import OrderedDict
from  nested_dict import nested_dict
import xlsxwriter
import pcom
import env_booter

LOG = pcom.gen_logger(__name__)

class RegProc(object):
    """auto reg processor for pj"""
    def __init__(self):
        self.ced, self.cfg_dic = env_booter.EnvBooter().boot_env()
        self.local_address_set = set()
        self.global_address_dic = {}
        self.sw_rtl_dic = nested_dict()
    @classmethod
    def gen_xls(cls, data_dic, sheet, sheet_fmt):
        """gen xls"""
        index = 1
        sheet.set_column('A:F', 30, sheet_fmt)
        sheet.set_default_row(20)
        bits_title_lst = [
            "bit", "definition", "RW", "reset value", "ucode reset value", "description"]
        for reg, reg_dic in data_dic.items():
            sheet.write(f"A{index}", "register name", sheet_fmt)
            sheet.write(f"B{index}", reg)
            index += 1
            for para, para_dic in reg_dic.items():
                if para == "fields":
                    continue
                sheet.write(f"A{index}", para, sheet_fmt)
                sheet.write(f"B{index}", para_dic)
                index += 1
            sheet.write_row(f"A{index}", bits_title_lst)
            index += 1
            for bits, bits_dic in reg_dic["fields"].items():
                sheet.write_row(
                    f"A{index}", [
                        bits, bits_dic["definition"], bits_dic["RW"], bits_dic["reset_value"],
                        bits_dic["ucode_reset_value"], bits_dic["description"]])
                index += 1
            index += 2
    @classmethod
    def fmt_v_data(cls, data):
        """format verilog data"""
        data_dic = nested_dict()
        for reg, reg_dic in data.items():
            reg = reg.lower()
            for para, para_dic in reg_dic.items():
                if para == "fields":
                    for bits, bits_dic in para_dic.items():
                        inter_lst = re.findall(r"\d+", bits)
                        if ":" not in bits:
                            bits_dic["interval"] = ""
                            bits_dic["st_ed"] = [int(inter_lst[0]), int(inter_lst[0])]
                        else:
                            number = int(inter_lst[0]) - int(inter_lst[1])
                            bits_dic["st_ed"] = [int(inter_lst[0]), int(inter_lst[1])]
                            bits_dic["interval"] = f"[{number}:0]"
                        define = bits_dic["definition"]
                        bits_dic["definition"] = define.lower().replace(
                            " ", "_") if define else None
                        bits_dic["interval_type"] = (
                            reg_dic["32bit/64bit"].replace("bit", "")
                            if bits in ("[31:0]", "[63:0]") else "kbwk")
                        data_dic[reg][para][bits] = bits_dic
                else:
                    data_dic[reg][para] = para_dic
        return data_dic
    @classmethod
    def fmt_ralf_data(cls, data):
        """format ralf data"""
        data_dic = nested_dict()
        data_dic["blk_bytes"] = 0
        for reg, reg_dic in data.items():
            reg = reg.lower()
            for para, para_dic in reg_dic.items():
                if para == "fields":
                    for bits, bits_dic in para_dic.items():
                        inter_lst = re.findall(r"\d+", bits)
                        if ":" not in bits:
                            bits_dic["bits"] = 1
                            bits_dic["st_bit"] = int(inter_lst[0])
                        else:
                            bits_dic["st_bit"] = int(inter_lst[1])
                            bits_dic["bits"] = int(inter_lst[0]) - int(inter_lst[1]) + 1
                        define = bits_dic["definition"]
                        bits_dic["definition"] = define.lower().replace(
                            " ", "_") if define else reg
                        bits_dic = {
                            key: bits_dic[key] for key
                            in bits_dic.keys()-{"RW", "description", "ucode_reset_value"}}
                        data_dic[reg][para][bits] = bits_dic
                elif para == "32bit/64bit":
                    data_dic[reg][para] = round(int(re.findall(r"\d+", para_dic)[0])/8)
                    data_dic["blk_bytes"] += data_dic[reg][para]*(
                        2 if reg_dic["ST/MT"] == "MT" else 1)
                elif para in ("local_address", "ST/MT"):
                    if para_dic == "MT":
                        hex_num = re.match(
                            r"[\da-f]*", reg_dic["local_address"].split("'h")[1]).group(0)
                        mt_address = "12" + hex(
                            int(f"0x{hex_num}", 16) + 2048).replace("0x", "'h")
                        data_dic[reg]["mt_address"] = mt_address
                    data_dic[reg][para] = para_dic
        return data_dic
    @classmethod
    def check_public_register(cls, public_reg_dic, template_dic, fmt_dic):
        """to generate same register in all cfg files for ralf file gen"""
        for module_nm, reg_dic in template_dic.items():
            if not module_nm:
                break
            if module_nm == "blk_bytes":
                continue
            for reg_nm, para_dic in reg_dic.items():
                if reg_nm == "blk_bytes":
                    continue
                if reg_nm in fmt_dic:
                    public_reg_dic[reg_nm] = para_dic
    @classmethod
    def hex_add_num(cls, h_addr, step=0):
        """hex add num """
        base = h_addr.replace(" ", "")
        base_lst = base.split("'")
        if base_lst[1].startswith("h"):
            hex_num = re.match(r"[\da-f]*", base.split("'h")[1]).group(0)
            lint_num = int(f"0x{hex_num}", 16) + step
            hint_num = lint_num + 1
            hbase = base_lst[0] + hex(hint_num).replace("0x", "'h")
            lbase = base_lst[0] + hex(lint_num).replace("0x", "'h")
        elif base_lst[1].startswith("b"):
            bin_num = re.match(r"[\da-f]*", base.split("'b")[1]).group(0)
            lint_num = int(f"0b{bin_num}", 2) + step
            hint_num = lint_num + 1
            hbase = base_lst[0] + bin(hint_num).replace("0b", "'b")
            lbase = base_lst[0] + bin(lint_num).replace("0b", "'b")
        return [lbase, hbase]
    def detect_address(self, regr_nm, addr_type, address_lst):
        """detect address exists"""
        if addr_type == "local_address":
            for addr_val in address_lst:
                if addr_val in self.local_address_set:
                    raise Exception(f"{regr_nm} register {addr_val} local address exists!")
                else:
                    self.local_address_set.add(addr_val)
        if addr_type == "global_address":
            for addr_val in address_lst:
                if addr_val in self.global_address_dic:
                    if self.global_address_dic[addr_val] != regr_nm:
                        LOG.warning(
                            f"same global address {addr_val} has different register name: "
                            f"{regr_nm} and {self.global_address_dic[addr_val]}")
                else:
                    self.global_address_dic[addr_val] = regr_nm
    def expand_id_fmt(self, reg_dic, data_dic, reg_real, id_num):
        """to expand <id> fmt in json file"""
        for para, para_dic in reg_dic.items():
            if para in ("range",):
                continue
            if "_address" in para:
                base = para_dic.get("base", None)
                if not base:
                    raise Exception(f"{reg_real}-{para} has no base field!")
                if base == "NA":
                    data_dic[reg_real][para] = base
                else:
                    step = id_num * int(para_dic["step"] if para_dic.get("step", None)
                                        else id_num)
                    temp_lst = self.hex_add_num(base, step)
                    address_lst = temp_lst if reg_dic["32bit/64bit"] == "64bit" else temp_lst[:1]
                    if reg_dic["32bit/64bit"] == "64bit":
                        data_dic[reg_real][f"h{para}"] = address_lst[1]
                    data_dic[reg_real][para] = address_lst[0]
                    self.detect_address(reg_real, para, address_lst)
            elif para == "fields":
                for bits, bits_dic in para_dic.items():
                    for b_k, b_v in bits_dic.items():
                        data_dic[reg_real][para][bits][b_k] = b_v.replace(
                            "<id>", str(id_num)) if b_k in ("definition", "description") else b_v
            else:
                data_dic[reg_real][para] = para_dic
    def expand_data(self, data):
        """to expand data in original json file"""
        data_dic = nested_dict()
        for reg, reg_dic in data.items():
            if "<id>" in reg:
                if not reg_dic.get("range", None):
                    raise Exception(f"auto step register {reg} has no range field")
                mop = pcom.REOpter(reg_dic["range"])
                if not mop.match(re.compile(r"\s*(\d*)\s*\,\s*(\d*)\s*")):
                    raise Exception(f"{reg} register range foramt error!")
                for id_num in range(int(mop.group(1)), int(mop.group(2))+1):
                    reg_real = reg.replace("<id>", str(id_num))
                    self.expand_id_fmt(reg_dic, data_dic, reg_real, id_num)
            else:
                local_address = reg_dic.get("local_address")
                global_address = reg_dic.get("global_address")
                if reg_dic["32bit/64bit"] == "64bit":
                    local_addr_lst = self.hex_add_num(local_address)
                    global_addr_lst = self.hex_add_num(global_address)
                else:
                    local_addr_lst = [local_address]
                    global_addr_lst = [global_address]
                self.detect_address(reg, "local_address", local_addr_lst)
                self.detect_address(reg, "global_address", global_addr_lst)
                if reg_dic["32bit/64bit"] == "64bit":
                    reg_dic["hlocal_address"] = local_addr_lst[1]
                    reg_dic["hglobal_address"] = global_addr_lst[1]
                data_dic[reg] = reg_dic
        return data_dic
    def fmt_sw_data(self, data_dic):
        """formate software doc """
        filter_fields = {"SW_visible", "local_address", "global_address", "local_address_hi"}
        for reg, reg_dic in data_dic.items():
            if reg_dic["SW_visible"] == "no":
                continue
            if reg in (self.sw_rtl_dic["NA"], self.sw_rtl_dic["MSR"]):
                reg_type = "NA" if reg in self.sw_rtl_dic["NA"] else "MSR"
                diff_keys = (reg_dic["fields"].keys() -
                             self.sw_rtl_dic[reg_type][reg]["fields"].keys())
                if diff_keys:
                    for key in diff_keys:
                        self.sw_rtl_dic[reg_type][reg]["fields"][key] = reg_dic["fields"][key]
            else:
                reg_type = "NA" if reg_dic["MSR_address"] == "NA" else "MSR"
                self.sw_rtl_dic[reg_type][reg] = {
                    key:reg_dic[key] for key in reg_dic.keys()-filter_fields}
    def proc_reg(self, reg_module_lst):
        """reg process main"""
        proc_dic = {}
        proc_dic["reg_doc_dir"] = os.path.abspath(
            os.path.expandvars(pcom.rd_cfg(self.cfg_dic["proj"], "reg_dir", "doc", True)))
        proc_dic["workbook_hw"] = xlsxwriter.Workbook(
            f"{proc_dic['reg_doc_dir']}{os.sep}YJD_register.xlsx")
        proc_dic["workbook_sw"] = xlsxwriter.Workbook(
            f"{proc_dic['reg_doc_dir']}{os.sep}CPU_register.xlsx")
        proc_dic["sheet_sw"] = proc_dic["workbook_sw"].add_worksheet("CPU1_regsiter")
        proc_dic["format_sw"] = proc_dic["workbook_sw"].add_format({"font_size": "15"})
        proc_dic["reg_rtl_dir"] = os.path.abspath(
            os.path.expandvars(pcom.rd_cfg(self.cfg_dic["proj"], "reg_dir", "rtl", True)))
        proc_dic["reg_cfg_dir"] = f"{self.ced['SHARE_CONFIG']}{os.sep}pj_reg"
        proc_dic["reg_temp_dir"] = f"{self.ced['SHARE_TEMPLATES']}{os.sep}pj_reg"
        proc_dic["reg_cfg_iter"] = [
            f"{proc_dic['reg_cfg_dir']}{os.sep}{cc}.json" for cc
            in reg_module_lst] if reg_module_lst else pcom.find_iter(
                proc_dic["reg_cfg_dir"], "*.json")
        proc_dic["reg_ralf_dir"] = os.path.abspath(
            os.path.expandvars(pcom.rd_cfg(self.cfg_dic["proj"], "reg_dir", "ralf", True)))
        proc_dic["ralf_dic"] = {"blk_bytes": 0}
        proc_dic["public_reg_dic"] = {}
        for reg_cfg_json in proc_dic["reg_cfg_iter"]:
            if not os.path.isfile(reg_cfg_json):
                raise Exception(f"reg cfg file {reg_cfg_json} is NA")
            LOG.info("processing reg config file %s", reg_cfg_json)
            sin_dic = {}
            sin_dic["json_dir"], sin_dic["json_name"] = os.path.split(reg_cfg_json)
            sin_dic["module_cname"], _ = os.path.splitext(sin_dic["json_name"])
            sin_dic["module_name"] = sin_dic["module_cname"].lower()
            sin_dic["rtl_dir"] = sin_dic["json_dir"].replace(
                proc_dic["reg_cfg_dir"], proc_dic["reg_rtl_dir"])
            os.makedirs(sin_dic["rtl_dir"], exist_ok=True)
            sin_dic["sheet_hw"] = proc_dic["workbook_hw"].add_worksheet(sin_dic["module_cname"])
            sin_dic["format_hw"] = proc_dic["workbook_hw"].add_format({"font_size": "15"})
            with open(reg_cfg_json, encoding="gb18030") as file:
                data = json.load(file)
            data_dic = self.expand_data(data)
            pcom.ren_tempfile(
                f"{proc_dic['reg_temp_dir']}{os.sep}reg_base.v",
                f"{sin_dic['rtl_dir']}{os.sep}{sin_dic['module_name']}.v",
                {"module_name": sin_dic["module_name"], "data": self.fmt_v_data(data_dic)})
            self.gen_xls(data_dic, sin_dic["sheet_hw"], sin_dic["format_hw"])
            self.fmt_sw_data(data_dic)
            ralf_data_dic = self.fmt_ralf_data(data_dic)
            proc_dic["ralf_dic"][sin_dic["module_name"]] = ralf_data_dic
            proc_dic["ralf_dic"]["blk_bytes"] += ralf_data_dic["blk_bytes"]
            self.check_public_register(
                proc_dic["public_reg_dic"], proc_dic["ralf_dic"], ralf_data_dic)
        os.makedirs(proc_dic["reg_ralf_dir"], exist_ok=True)
        pcom.ren_tempfile(
            f"{proc_dic['reg_temp_dir']}{os.sep}reg_base.ralf",
            f"{proc_dic['reg_ralf_dir']}{os.sep}reg.ralf",
            {"public_data": proc_dic["public_reg_dic"], "data": proc_dic["ralf_dic"]})
        sw_data_dic = OrderedDict(self.sw_rtl_dic["NA"])
        self.sw_rtl_dic["MSR"] = OrderedDict(
            sorted(self.sw_rtl_dic["MSR"].items(),
                   key=lambda reg: int(f'0x{reg[1]["MSR_address"].split("h")[1]}', 16)))
        sw_data_dic.update(self.sw_rtl_dic["MSR"])
        self.gen_xls(sw_data_dic, proc_dic["sheet_sw"], proc_dic["format_sw"])
        os.makedirs(proc_dic["reg_doc_dir"], exist_ok=True)
        proc_dic["workbook_sw"].close()
        proc_dic["workbook_hw"].close()

def run_reg(args):
    """to run reg sub cmd"""
    if args.reg_gen:
        RegProc().proc_reg(args.reg_module_lst)
        LOG.info("running auto reg done")
        # ced, cfg_dic = env_booter.EnvBooter().module_env(args.reg_module)
        # tb_top = pcom.rd_cfg(cfg_dic["simv"], "DEFAULT", "tb_top", True, "test_top")
        # reg_str_lst = []
        # for reg_file in pcom.find_iter(ced["MODULE_REG"], "*.ralf"):
        #     reg_str_lst.append(f"ralgen -full64 -t {tb_top} -uvm -c F -a {reg_file} ")
        # subprocess.run(" && ".join(reg_str_lst), shell=True)
    else:
        raise Exception("missing main arguments")
