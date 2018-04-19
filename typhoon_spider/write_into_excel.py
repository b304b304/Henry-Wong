# -*- coding=utf-8 -*-
import re
import json
import pandas
storage_path = "/home/nico/data/typhoon_data/"
typhoon_number = {
    2016: 26, 2017: 27
}


def load_json_data(file_path):
    with open(file_path, encoding="gbk") as json_file:
        json_data = json.load(json_file)
    return json_data


def collect_basic_data():
    # Fetch the data from json file and collect into a excel file
    filename = "{Year}{Serial_number}_{Data_type}.json"
    typhoon_data_list = []
    for i in range(0, 2):
        year = str(2016 + i)
        for j in range(1, typhoon_number[2016 + i] + 1):
            serial_number = str(j).zfill(2)
            typhoon_data = load_json_data(storage_path + filename.format(
                Year=year,
                Serial_number=serial_number,
                Data_type="Info"
            ))
            tyid = year + serial_number
            print(tyid)
            name = typhoon_data[0]["name"]
            land_tuple = ("No-landed", "No-landed")
            if len(typhoon_data[0]["land"]) > 0:
                land_tuple = re.findall("在([\w\W]+?)登陆|登陆([\w\W]+)", typhoon_data[0]["land"][0]["info"])[0]
            if len(land_tuple[0]) < len(land_tuple[1]):
                land = land_tuple[1]
            else:
                land = land_tuple[0]
            enname = typhoon_data[0]["enname"]
            row = [tyid, name, land, enname, year]
            typhoon_data_list.append(row)
            print("succeed")
    return pandas.DataFrame(typhoon_data_list).to_excel("basic_data.xlsx")


def collect_route_data():
    # Fetch the data from json file and collect into a excel file
    filename = "{Year}{Serial_number}_{Data_type}.json"
    route_data_list = []
    for i in range(0, 2):
        year = str(2016 + i)
        for j in range(1, typhoon_number[2016 + i] + 1):
            serial_number = str(j).zfill(2)
            typhoon_data = load_json_data(storage_path + filename.format(
                Year=year,
                Serial_number=serial_number,
                Data_type="Info"
            ))
            # 	移动速度（m/s）	移动方向	7级风圈半径(Km)	10级风圈半径(Km)
            tyid = year + serial_number
            print(tyid)
            name = typhoon_data[0]["name"]
            for k in range(0, len(typhoon_data[0]["points"])):
                point = typhoon_data[0]["points"][k]
                date = point["time"].split(" ")[0]
                latitude = point["lat"]
                longitude = point["lng"]
                pressure = point["pressure"]
                c_speed = point["speed"]
                move_speed = point["movespeed"]
                direction = point["movedirection"]
                radius7 = point["radius7"]
                radius10 = point["radius10"]
                row = [
                    tyid, name, date, latitude, longitude, pressure, c_speed, move_speed, direction,
                    radius7, radius10
                ]
                route_data_list.append(row)
            print("succeed")
    return pandas.DataFrame(route_data_list).to_excel("route_data.xlsx")


def main():
    print(collect_basic_data())
    print("#---------------succeed---------------#")
    print(collect_route_data())
    print("#---------------succeed---------------#")

if __name__ == "__main__":
    main()