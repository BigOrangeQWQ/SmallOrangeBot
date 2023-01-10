# import re

# regex = r"[\u4e00-\u9fa5]{1,100}"

# test_str = ("d测试的我大弯发定位发我发文日发的\n"
# 	"大武当发发我发违法打完饭fafaw\n"
# 	"的玩法与无服务互客户付iahfiwuyh\n")

# matches = re.search(regex, test_str, re.MULTILINE)

# if matches is not None:
#     print(matches.group())
# for matchNum, match in enumerate(matches, start=1):
    # for groupNum in range(0, len(match.groups())):
    #     groupNum = groupNum + 1
    #     print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
# a = ''
# # print(a is None)
# if a:
#     print('a')

# print(1 | 0)
# print(1 | 1)
# print(0 | 0)

# import onedice
# rd_para = onedice.RD("1d3+1d5")
# print(rd_para.originData)
# rd_para.roll()
# print('----------------')
# if rd_para.resError != None:
#     print(rd_para.resError)
# else:
#     print(rd_para.resInt)
#     print(rd_para.resIntMax)
#     print(rd_para.resIntMin)
#     print(rd_para.resIntMaxType)
#     print(rd_para.resIntMinType)
#     print(rd_para.resDetail)
#     print(rd_para.resDetailData)
#     print(rd_para.resMetaTuple)
#     print(rd_para.resMetaTupleEnable)
# print('================')

from pathlib import Path


a = Path('./data/log_cache.txt')
print(a.absolute())
print(a.as_posix())