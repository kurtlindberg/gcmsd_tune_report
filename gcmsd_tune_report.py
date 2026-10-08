# Python script for extracting Agilent GC-MSD tuning results

import argparse
from pypdf import PdfReader
import csv
from datetime import datetime


def get_report_text(report):
    
    # Parse all PDF report text into a single string using pypdf
    reader = PdfReader(f"{report}")
    page = reader.pages[0]
    page_text = page.extract_text()
    
    # Divide text string by newline (\n) characters
    page_text_lines = page_text.splitlines()
    lines_dict = {}
    
    # Split line strings into lists by spaces
    # Put each line list into an indexed dict key
    for line in range(len(page_text_lines)):
        line_text_list = page_text_lines[line].split()
        lines_dict.update({f"{line}": line_text_list})
        
    # Print text dict line by line    
    # for key, value in lines_dict.items():
        # print(f"{key}: {value}")
        
    return lines_dict   
    

def make_report_csv(text, username):
    
    # Manually define table headers since it's used multiple times
    mz_headers = ["Target_mz", "Actual_mz", "Abund", "Rel_Abund", "Iso_mz", "Iso_Abund", "Iso_Ratio"]
    
    # Reformat report data from mm/dd/yy to yyyymmdd
    date_str = text["41"][2]
    date_obj = datetime.strptime(date_str, "%m/%d/%Y")
    ymd_date = date_obj.strftime("%y%m%d")
    
    # Define all column names
    column_names = [
        "User",
        "Date",
        text["3"][0],
        *mz_headers * 3,
        text["29"][2],
        text["29"][4],
        text["29"][6],
        text["29"][8],
        text["29"][10],
        "Column_1_Flow",
        "Column_2_Flow",
        "Interface_Temp",
        "Electron_Multiplier_Gain",
        "Gain Factor",
    ]
    
    # Define data for all columns
    report_data = [
        username,
        # text["41"][2],
        ymd_date,
        text["3"][1],
        *text["20"],
        *text["21"],
        *text["22"],
        text["29"][3],
        text["29"][5],
        text["29"][7],
        text["29"][9],
        text["29"][11],
        text["30"][2],
        text["30"][4],
        text["30"][8],
        text["32"][11],
        text["33"][9],
    ]

    # Write the columns and data as a .csv file
    with open(
        f'atune_hot{text["17"][2]}C_fil{text["3"][1]}_{ymd_date}.csv',
        mode='w',
        newline='',
        encoding='utf-8'
    ) as file:
        writer = csv.writer(file)
        
        writer.writerow(column_names)
        writer.writerow(report_data)
        

def main():
    
    ap = argparse.ArgumentParser()
    ap.add_argument("--filename")
    ap.add_argument("--user")
    args = ap.parse_args()
    
    report_text = get_report_text(args.filename)
    make_report_csv(report_text, args.user)
    
    
if __name__ == "__main__":
    main()
