#! /usr/bin/env python3

import json
import xlrd
from nested_dict import nested_dict

def map_title(row_lst):
    title_index_lst = []
    for title in table_title_lst:
        if title in row_lst:
            title_index_lst.append(row_lst.index(title))
        else:
            raise Exception(f"{title} field is not in table title list, contact me!")
    return title_index_lst

def gen_json_file(sheet, dic):
    with open(f"./{sheet}.json", "w", encoding='utf8') as file:
        str_ = json.dumps(dic, indent=4, separators=(',', ':'), ensure_ascii=False)
        file.write(str(str_))

def excel_transfor_json():
    reg_data = xlrd.open_workbook('./uncore_register.xlsx')
    sheet_name_lst = reg_data.sheet_names()
    for sheet_name in sheet_name_lst:
        print(f"{sheet_name} is Running!")
        result_dic = nested_dict()
        reg_name, title_index_lst = "", []
        reg_flag, bit_flag = False, False
        table_sheet = reg_data.sheet_by_name(f'{sheet_name}')
        for row in range(table_sheet.nrows):
            row_lst = table_sheet.row_values(row)
            if row_lst[0] == "命名":
                reg_name = ""
                reg_flag = True
                title_index_lst = map_title(row_lst)

            if row_lst == list(reversed(row_lst)):
                reg_flag = False
                bit_flag = False

            if reg_flag and bit_flag:
                bits_name = table_sheet.cell(row, title_index_lst[4]).value
                definition = table_sheet.cell(row, title_index_lst[5]).value
                description = table_sheet.cell(row, title_index_lst[6]).value
                reset_value = str(table_sheet.cell(row, title_index_lst[7]).value)
                if row_lst[0] != "":
                    reg_name = table_sheet.cell(row, title_index_lst[0]).value
                    address = table_sheet.cell(row, title_index_lst[1]).value
                    bit_widths = table_sheet.cell(row, title_index_lst[2]).value
                    if reg_name in result_dic:
                        raise Exception("{reg_name} register name existed in table title list")
                    result_dic[reg_name] = nested_dict({
                        "SW_visible": "NA",
                        "MSR_address": "NA",
                        "global_address": address,
                        "local_address": address,
                        "32bit/64bit": bit_widths,
                        "fields": {
                            bits_name: {
                                "RW": "NA",
                                "definition": definition,
                                "description": description,
                                "reset_value": reset_value,
                                "ucode_reset_value": "NA"
                            }
                        }
                    })
                    if bit_widths == "64bit":
                        addr_lst = address.split("h")
                        addr_int_num = int(f"0x{addr_lst[1]}", 16) + 1
                        address = addr_lst[0] + hex(addr_int_num).replace("0x", "h")
                        result_dic[reg_name]["local_address_hi"] = address
                else:
                    if bits_name in result_dic[reg_name]:
                        raise Exception("{bits_name} existed in {reg_name} register name")
                    result_dic[reg_name]["fields"][bits_name] = {
                        "RW": "NA",
                        "definition": definition,
                        "description": description,
                        "reset_value": reset_value,
                        "ucode_reset_value": "NA"
                    }
            if reg_flag:
                bit_flag = True
        gen_json_file(sheet_name, result_dic)

def main():
    excel_transfor_json()

if __name__ == "__main__":
    table_title_lst = ['命名', '地址', '位宽', '个数', '位域',
                       '域名', '描述', '初始值', '线程相关性', '备注']
    main()
