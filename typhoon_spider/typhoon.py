# -*- encoding=utf-8 -*-
import json
from urllib import request

charset = "utf-8"
storage_path = "C://typhoon_spider//data//"
typhoon_number = {
    2016: 26, 2017: 27
}
typhoon_url = {
    "List": "http://typhoon.zjwater.gov.cn/Api/TyphoonList/{Year}",
    "Event": "http://typhoon.zjwater.gov.cn/Api/TyphoonEvent/{Year}{Serial_number}/Flase",
    "Info": "http://typhoon.zjwater.gov.cn/Api/TyphoonInfo/{Year}{Serial_number}"
}


def download(url):
    # To crawl the data from xhr file by url
    # And decode the data by charset
    data = json.loads(request.urlopen(url).read().decode(charset))
    return data


def write_data(year, serial_number, data_type_value, data, path):
    # To write the data into a jsonfile in the storage path
    # The filename is named accroding to the year and serial number
    # Different types of data will be write into different files
    filename = "{Year}{Serial_number}_{Data_type}.json"
    data_type = {
        0: "List", 1: "Event", 2: "Info"
    }
    with open(path + filename.format(
            Year=year,
            Serial_number=serial_number,
            Data_type=data_type[data_type_value]), "a+") as typhoon_data:
        json.dump(data, typhoon_data, ensure_ascii=False)

if __name__ == '__main__':
    for i in range(0, 2):
        # Download the list of typhoon by loop
        List_data = download(typhoon_url["List"].format(Year=str(2016 + i)))
        write_data(str(2016 + i), "", 0, List_data, storage_path)

    for i in range(0, 2):
        # Download the info and event of typhoon
        for j in range(1, typhoon_number[2016 + i] + 1):
            # Download by the serial number
            typhoon_year = str(2016 + i)
            typhoon_snum = str(j).zfill(2)
            Event_data = download(typhoon_url["Event"].format(Year=typhoon_year, Serial_number=typhoon_snum))
            write_data(typhoon_year, typhoon_snum, 1, Event_data, storage_path)
            Info_data = download(typhoon_url["Info"].format(Year=typhoon_year, Serial_number=typhoon_snum))
            write_data(typhoon_year, typhoon_snum, 2, Info_data, storage_path)
