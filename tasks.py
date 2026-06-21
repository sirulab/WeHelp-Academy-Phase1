# task1------------
print("------task1------")

def func1(name):
    points = {"⾟巴":(-3,3), "悟空":(0,0), "弗利沙":(4,-1), "特南克斯":(1,-2), "丁滿":(-1,4), "貝吉塔":(-4,-1)}
    # 查了一下數學上怎麼判斷點在線的哪一邊
    # y = -1.2x + 1.8 
    # (0,1.8)/ (1.5,0)
    # 1.2x + y - 1.8 ><= 0
    target0 = points[name]
    side_num_target0 = 1.2* target0[0] +target0[1]-1.8
    dis_list = []
    side_list = []
    name_list = ["⾟巴", "悟空", "弗利沙", "特南克斯", "丁滿", "貝吉塔"]
    total_list = []
    for p in points:
        target = points[p]
        side_num_target = 1.2* target[0] +target[1]-1.8
        if side_num_target0 > 0 and side_num_target< 0: # 邊界條件:沒有剛好是12或18的座標，所以不會有0
            side = 2
        elif side_num_target0 < 0 and side_num_target> 0:
            side = 2
        else:
            side = 0
        side_list.append(side)
        dis_x = target[0] - target0[0] # tuple不能相減/ points[p] 取得key 而不value
        dis_y = target[1] - target0[1]
        dis = abs(dis_x) + abs(dis_y)
        dis_list.append(dis)
    # return dis_list, side_list   # list to do: max逐一比較而不是列出整個list，可能比較有效率
    # 先相加 再找名字
    for n in range(len(name_list)): # 邊界條件:0是自己
        total = dis_list[n] +side_list[n]
        total_list.append(total)

    for n in range(len(name_list)):
        if total_list[n] == 0:
            total_list.pop(n) # 不會有兩個0; 修改的原始序列不是好行為
            name_list.pop(n)
            break # 不然會報錯: list index out of range

    furthest = max(total_list)
    nearest = min(total_list)

    furthest_name = []
    nearest_name = []
    
    for n in range(len(name_list)):
        if total_list[n] == furthest:
            furthest_name.append(name_list[n]) # 有兩個怎麼辦 -> list 解決
        if total_list[n] == nearest:
            nearest_name.append(name_list[n])

    # return furthest, nearest, furthest_name, nearest_name #試著用OOP寫?
    return print(f"最遠{", ".join(furthest_name)}；最近{"、".join(nearest_name)}")

# 最遠dis_list.max()；最近dis_list.min() # 要人名不是數值  # points[p]
# print(func1("⾟巴"))

func1("⾟巴") # print 最遠弗利沙；最近丁滿、⾙吉塔
func1("悟空") # print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙") # print 最遠⾟巴，最近特南克斯 # correction
func1("特南克斯") # print 最遠丁滿，最近悟空


# task2------------
print("------task2------")

time_available = {
    "S1": list(range(1, 25)),
    "S2": list(range(1, 25)),
    "S3": list(range(1, 25))
}
time_booked = {
    "S1": [], "S2": [], "S3": []
}

# 思考一下: 為什麼有ss和services, services為什麼可以不放前面

def func2(ss, start, end, criteria):
    # order matters: 有時間庫存
    # 先檢查符合條件的車廂名，再檢查有時間庫存
    # criteria分3類 -> 對應3個條件: 是c 是r 是name ->得到check_field(cf), op and target_value
    if criteria[0] == "c":
        cf = "c"
        if criteria[1:3] == ">=": # [cite2] 只有這三種
            op = ">="
            target_value = int(criteria.split(">=")[1])
        elif criteria[1:3] == "<=":
            op = "<="
            target_value = int(criteria.split("<=")[1])
        else: # "="
            op = "="
            target_value = int(criteria.split("=")[1])

    elif criteria[0] == "r":
        cf = "r"
        if criteria[1:3] == ">=":
            op = ">="
            target_value = float(criteria.split(">=")[1])
        elif criteria[1:3] == "<=":
            op = "<="
            target_value = float(criteria.split("<=")[1])
        else: # "="
            op = "="
            target_value = float(criteria.split("=")[1])

    elif "name" in criteria:
        cf = "name"
        op = "="
        target_value = str(criteria.split("=")[1])

    else:
        return print("Sorry")
    
    diff_min = float('inf')
    best_name = ""
    for s in ss:
        val = s[cf] # value
        is_match = False

        if op == "=" and val == target_value:
            is_match = True
        elif op == ">=" and val >= target_value: 
            is_match = True
        elif op == "<=" and val <= target_value:
            is_match = True

        if is_match:
            if cf != "name":
                diff = abs(val - target_value)
                if diff < diff_min:
                    diff_min = diff            
                    best_name = s["name"]
            else:
                best_name = s["name"]

    if best_name == "":
        return print("Sorry")

    time_requested = list(range(start, end))
    avail_list = time_available[best_name]
    
    can_book = True
    for t in time_requested:
        if t not in avail_list:
            can_book = False
            break
            
    if can_book:
        for t in time_requested:
            avail_list.remove(t)
            time_booked[best_name].append(t)
        return print(best_name)
        
    return print("Sorry")

services=[
    {"name":"S1", "r":4.5, "c":1000},
    {"name":"S2", "r":3, "c":1200},
    {"name":"S3", "r":3.8, "c":800}
    ]

func2(services, 15, 17, "c>=800") # S3
func2(services, 11, 13, "r<=4") # S3
func2(services, 10, 12, "name=S3") # Sorry
func2(services, 15, 18, "r>=4.5") # S1
func2(services, 16, 18, "r>=4") # Sorry
func2(services, 13, 17, "name=S1") # Sorry
func2(services, 8, 9, "c<=1500") # S2

# task3------------
print("------task3------")

def func3(index):
    # 規律是 減2[1], 減3[2], 加1[3], 加2[4]
    # 先不考慮index == 0
    q = index//4
    r = index%4
    # index +1 第幾個數字 index = 6; 6//4 = 1; 6%4 = 2; 25-2*q+ -5
    if r == 1:
        r_num = -2
    elif r == 2:
        r_num = -5
    elif r == 3:
        r_num = -4
    elif r == 0:
        r_num = -2
    val = 25-2*q+r_num

    return print(val)

    # 老師應該不是要我用這個式子，應該是要印出整個list之後找index，用while<之類的，之後再檢討

func3(1) # print 23
func3(5) # print 21
func3(10) # print 16
func3(30) # print 6

# task4------------
print("------task4------")

def func4(sp, stat, n):
    # 先用stat_list，找出可以對照的車廂 -> 新的sp_list [x, 1, x, 4, 3, 2] -> 用task2的絕對值方法找出最接近的
    
    sp_list = list(sp) # 剛好不用備分sp
    stat_list = list(stat)
    for nn in range(len(stat_list)): # 在此我假設sp_list的長度=stat_list
        if stat_list[nn] == "1":
            sp_list[nn] = "x"
    dis_list = []
    dis_pm_list = []
    for vv in sp_list:
        if vv != "x":
            pre_dis = vv - n # 這裡報錯: vv可能是字母
            dis = abs(pre_dis)
            dis_list.append(dis)
            if pre_dis >= 0:
                dis_pm = "p"
            else:
                dis_pm = "m"
            dis_pm_list.append(dis_pm)
        else:
            dis_list.append(float('inf')) # 這裡修正
            dis_pm_list.append("x")
    

    dis_min = min(dis_list)
    cart_num_list = []
    for nn in range(len(dis_list)):
        if dis_list[nn] == dis_min:
            cart_num_list.append(nn)

    # 檢查list中的正負，以正為主
    final_ans = cart_num_list[0]
    for vv in cart_num_list:
        if dis_pm_list[vv] == "p":
            final_ans = vv
            break
    return print(final_ans)

func4([3, 1, 5, 4, 3, 2], "101000", 2) # print 5
func4([1, 0, 5, 1, 3], "10100", 4) # print 4
func4([4, 6, 5, 8], "1000", 4) # print 2
