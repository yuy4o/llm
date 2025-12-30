try:
    3 == 4
    # print(x)

except Exception as e:
    print(e)

# 3==4 返回False，没有抛出异常，不会执行 except 部分
# try except 用于捕获和处理异常的

# try:
#     x = 5
#     print(y)
#
# except Exception as e:
#     y = 3
#     print(e)
#
# print(y)