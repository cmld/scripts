import os
import re
import openpyxl

def extract_strings(directory, pattern):
    matching_strings = []  # 存储匹配的字符串

    # 遍历目录下的所有文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # 打开文件并读取内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 使用正则表达式进行匹配
                    matches = re.findall(pattern, content)
                    # 将匹配到的字符串存储起来
                    matching_strings.extend(matches)
            except UnicodeDecodeError:
                print(f'UnicodeDecodeError: Unable to decode file {file_path}')

    return matching_strings

directory_path = '/Users/yk/Desktop/jt-station-indonesia-ios/JtStation-Indonesia-iOS/Classes'
regex_pattern = r'"([^"]*?)-r".localized'
# matchs = extract_strings(directory_path, regex_pattern)
# matchs = list(set(matchs))
# print(matchs)
# for extracted_string in matchs:
#     print(extracted_string)

matchs = ['快递公司ID未获取', '重量', '打印时间', '总体积', '手机号需超过8位', '批量打印完成', '打印失败', '折扣和优惠券，二者选最优惠的', '运费信息为空，请补全寄件信息', '功能操作待上线', '重复运单', '请选择结算方式', '金额(IDR)', '共%s单', '交接票数：%s票，是否确认交接', '扫一扫，在线寄快递', '当前产品类型没有保价类型可选', '正在获取信息，请稍后重试', '网点编号', '操作员', 'jms订单号', '请填写物品信息', '请填写收寄人信息', '先填写寄/收件人信息', '驿站名称']

# language = 0 # 中文
# language = 1 # 英文
language = 2 # 其他

matchDic = {}

# 打开 Excel 文件
workbook = openpyxl.load_workbook('transf-iden.xlsx')

# 选择工作表（Sheet），默认选择第一个工作表
sheet = workbook.active

# 读取每行的第一项
for row in sheet.iter_rows(min_row=1, values_only=True):
    if row and row[0] and row[language]:  # 确保行非空
        if row[0] in matchs :
            key = row[1].lower().replace(" ", "_")
            formatted_string = "\"%s\" = \"%s\"; // %s" % (key, row[language], row[0])
            matchDic["%s-r" % (row[0])] = key
            print(formatted_string)
            matchs = [value for value in matchs if value != row[0]]

# 关闭 Excel 文件
workbook.close()


print(matchs)

print(matchDic)



