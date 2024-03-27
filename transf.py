import os
import re
import openpyxl
import sys

# 获取命令行参数
args = sys.argv

# 打印命令行参数
print("Script name:", args[0])  # 第一个参数是脚本本身的名称
print("Arguments:", args[1:])  # 其他参数是传递给脚本的命令行参数


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


# 找出项目中所有的待翻译文本
directory_path = '/Users/yk/Desktop/jt-station-indonesia-ios/JtStation-Indonesia-iOS/Classes'
regex_pattern = r'"([^"]*?)-r"'
matchs = extract_strings(directory_path, regex_pattern)
matchs = list(set(matchs))
print("\n待匹配：", matchs, "\n")
# for extracted_string in matchs:
#     print(extracted_string)


############

## 以下是搜索输出
matchs = ['保存修改', '日期+货架号+单号后4位', '尾号', '更换', '模板选择', '条', '请获取运单号']

matchDic = {}

# 打开 Excel 文件
workbook = openpyxl.load_workbook('transfiden1.xlsx')

def read2output(language, matchs):
    # 选择工作表（Sheet），默认选择第一个工作表
    sheet = workbook.active

    # 读取每行的第一项
    for row in sheet.iter_rows(min_row=1, values_only=True):
        if row and row[0] and row[language]:  # 确保行非空
            if row[0] in matchs :
                key = row[1].lower().replace(" ", "_")
                formatted_string = "\"%s\" = \"%s\"; // %s" % (key, row[language], row[0])
                matchDic["%s" % (row[0])] = key
                print(formatted_string)
                # matchs = [value for value in matchs if value != row[0]]

    print("\n")


read2output(0, matchs)
read2output(1, matchs)
read2output(2, matchs)

# 关闭 Excel 文件
workbook.close()

filtered_array = [x for x in matchs if x not in list(matchDic.keys())]
print("\n未匹配的：", filtered_array)


