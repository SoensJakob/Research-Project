# testJson = [{"element": "heading", "Xmin": 235.2234344482422, "Ymin": 165.1385040283203, "Xmax": 460, "Ymax": 207}, {"element": "checkbox", "Xmin": 21.339384078979492, "Ymin": 439.400146484375, "Xmax": 73, "Ymax": 473}, {"element": "picture", "Xmin": 5.139520168304443, "Ymin": 209.4918670654297, "Xmax": 200, "Ymax": 429}, {"element": "text", "Xmin": 221.10891723632812, "Ymin": 223.43052673339844, "Xmax": 588, "Ymax": 419}]


# print("json to html")

# Y_priority = sorted(testJson, key=lambda d: d['Ymin'])


# for i in Y_priority: 
#     x = round((i['Xmin'] / 32)) + 1
#     y = round((i['Ymin'] / 32)) + 1

#     w = round(((i["Xmax"] - i["Xmin"]) / 32))
#     h = round(((i["Ymax"] - i["Ymin"]) / 32))

#     print(i["element"])
#     print((x,y),(w,h))

# for i in Y_priority:
#     grid = {}

#     # y position
#     if i["Xmin"] > 340:
#         x = 1
#     else:
#         x = 0
    
#     if (i["Xmin"] - i["Xmax"]) > 340: 
#         xlen = 2
#     else:
#         xlen = 1

#     grid["x"] = x
#     grid["xlen"] = xlen

#     if i["Ymin"] > 340:
#         y = 1
#     else:
#         y = 0
    
#     if (i["Ymin"] - i["Ymax"]) > 340: 
#         ylen = 2
#     else:
#         ylen = 1

#     grid["y"] = x
#     grid["ylen"] = xlen
    
#     i["pos"] = grid

#     print(i)
