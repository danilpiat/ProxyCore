import os
import re
import glob
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def parseConfigPath():
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'C:/Users/MSI/PycharmProjects/ProxyCore/myproject/myapp/1proxy-core-413809-18a1c0120f6f.json', scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key("16v9YhtAK_bIn-qGubQqpz1kPirADkcRkKUaJlw5eN6o").worksheet("admin")

    header = sheet.row_values(2)
    external_ip_column = header.index("external_ip") + 1
    filename_column = header.index("3proxy_config") + 1
    port_column = header.index("port") + 1

    directory = "C:/Users/MSI/PycharmProjects/ProxyCore/configs1"


    regex_pattern = r'proxy -s(\d) -n -a -p(\d+) -i([\d.]+) -e([\d.]+)'

    ports_dict = {}

    for file_path in glob.glob(os.path.join(directory, "*")):
        if os.path.isfile(file_path) and file_path.endswith(".txt"):
            file_name = os.path.basename(file_path)

            with open(file_path, "r") as file:
                for line in file:
                    match = re.match(regex_pattern, line.strip())
                    if match:
                        external_ip = match.group(4)
                        port = match.group(2)

                        if (external_ip, file_name) in ports_dict:
                            ports_dict[(external_ip, file_name)].append(port)
                        else:
                            ports_dict[(external_ip, file_name)] = [port]

    for (external_ip, file_name), ports in ports_dict.items():
        try:
            row = sheet.find(external_ip).row
        except AttributeError:
            row_values = sheet.row_values(2)
            sheet.insert_row([""] * (len(row_values) - 1), 3)
            row = 3

        sheet.update_cell(row, external_ip_column, external_ip)
        sheet.update_cell(row, filename_column, file_name)
        try:
            exist_ports = sheet.cell(row, port_column).value
        except AttributeError:
            exist_ports = []
        # for cur_file_port in ports:
        #     if cur_file_port not in exist_ports:
        #         exist_ports += f',{cur_file_port}'
        # sheet.update_cell(row, port_column, ','.join(exist_ports))
        new_ports = []
        for cur_file_port in ports:
            if cur_file_port not in new_ports:
                new_ports.append(cur_file_port)
        sheet.update_cell(row, port_column, ','.join(new_ports))
        sheet = client.open_by_key("16v9YhtAK_bIn-qGubQqpz1kPirADkcRkKUaJlw5eN6o").worksheet("admin")
