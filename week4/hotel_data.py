import urllib.request
import json
import csv

#url_ch = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
#url_en = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

def get_hotel_data(url_ch, url_en):
    with urllib.request.urlopen(url_ch) as response:
        raw_data_ch = response.read().decode("utf-8")
        parsed_data_ch = json.loads(raw_data_ch) # TypeError: string indices must be integers, not 'str'

    with urllib.request.urlopen(url_en) as response:
        raw_data_en = response.read().decode("utf-8")
        parsed_data_en = json.loads(raw_data_en)

    # dictionary with key: "name", "list"
    # "_id", "_importdate", "旅館類別", "旅宿名稱", "地址", "電話或手機號碼", "傳真", "房間數"
    # {"date": "2025-09-30 14:58:41.986272", "timezone_type": 3, "timezone": "Asia/Taipei"}

    data_ch = parsed_data_ch ["list"]
    data_en = parsed_data_en["list"]

    hotels_list = []
    hotels_adden = []
    districts_list = []

    class HotelCh:
        def __init__(self, obj):
            for k, v in obj.items():
                setattr(self, k, v)
            self.n = None
            self.a = None

    class HotelEn:
        def __init__(self, obj):
            for k, v in obj.items():
                setattr(self, k, v)

    # {"_id": 521, "_importdate": {"date": "2025-09-30 14:58:42.458090", "timezone_type": 3, "timezone": "Asia/Taipei"}, "旅館類別": "旅館", "旅宿名稱": "君帥旅館", "地址": "臺北市萬華區成都路68號8-10樓", "電話或手機號碼": "02-23718812", "傳真": "02-23899989", "房間數": "35"}
    for n in data_ch:
        h = HotelCh(n)
        hotels_list.append(h)

    for n in data_en:
        h = HotelEn(n)
        hotels_adden.append(h)

    # test1: print(hotels_list)

    def func_merge(list1, list2):
        for i in list1:
            for j in list2:
                if i._id == j._id:
                    i.n = getattr(j,"hotel name")  # 複寫 -> 點後面不能加""，所以用getattr
                    i.a = getattr(j,"address")
                    break

    func_merge(hotels_list, hotels_adden)

    # test2: print(hotels_list)
    hotels_j = []

    for obj in hotels_list:
        j = json.dumps(obj.__dict__, ensure_ascii=False) # 中文字編碼
        hotels_j.append(j)

    # hotels.csv
    target_keys = ["_id","旅宿名稱", "n", "地址", "a", "電話或手機號碼", "房間數"]
    target_values = []

    for obj in hotels_list:
        i_list = []
        
        for j in target_keys:
            i_obj = getattr(obj, j, "") 
            i_list.append(i_obj)
            
        target_values.append(i_list)

    return target_values

#with open("hotels.csv", "w", newline="", encoding="utf-8-sig") as file:
#    writer = csv.writer(file)
#    writer.writerows(target_values)