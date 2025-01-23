
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

####
####
####
#### 找出项目中所有的待翻译文本
directory_path = '/Users/yk/Desktop/jt-station-indonesia-ios/JtStation-Indonesia-iOS/Classes'

regex_pattern = r'"([^"]*?)-r"'
matchs = extract_strings(directory_path, regex_pattern)
matchs =  [s.strip() for s in list(set(matchs))] 
print("\n待匹配：", matchs, "\n\n\n")
for extracted_string in matchs:
    print(extracted_string)


# sys.exit()





####
####
####
####
#### 对比本地文件
filename = '/Users/yk/Desktop/jt-station-indonesia-ios/JtStation-Indonesia-iOS/Classes/Manager/Lanaguage/zh-Hans.lproj/Localizable.strings'

exsitArr = []
# 打开文件
with open(filename, 'r') as file:
    # 逐行读取文件内容
    for line in file:
        # 处理每一行内容，例如打印或者其他操作
        for item in matchs:
            itemStr = "\"%s\"" % (item)
            if itemStr in line:
                print(line.strip())  # 使用 strip() 方法去除行尾的换行符
                exsitArr.append(item)

filtered_array = [x for x in matchs if x not in exsitArr]
print("\n-------- 本地文件 未匹配的：\n")
for item in filtered_array:
    print(item)
print("\n-------- 本地文件 未匹配的\n")

# sys.exit()





####
####
####
####
#### 匹配Excel文件上的翻译

matchs = filtered_array

def char_in_array(char, arr):
    while char in arr:
        char = f"{char}1"
    return char

# 打开 Excel 文件
workbook = openpyxl.load_workbook('/Users/yk/Downloads/987987987.xlsx')
sheet = workbook.worksheets[0] # 选择工作表（Sheet），默认选择第一个工作表 索引从0开始
column = 0 # 文本从第几列开始
matchDic = {}
def read2output(language, matchs): # language：要提取第几列内容
    # 读取每行的第一项
    for row in sheet.iter_rows(min_row=1, values_only=True):
        if row and row[column] and row[language]:  # 确保行非空
            columnValu = row[column].strip()
            languageValue = row[language].strip()
            if columnValu in matchs and row[column + 1] :
                key = row[column + 1].lower().replace(" ", "_")
                key = char_in_array(key, list(matchDic.values()))
                formatted_string = "\"%s\" = \"%s\"; // %s" % (key, languageValue, columnValu)
                matchDic["%s" % (columnValu)] = key
                print(formatted_string)
                # matchs = [value for value in matchs if value != row[0]]
    print("\n")

read2output(column, matchs)
matchDic = {}
read2output(column+1, matchs)
matchDic = {}
read2output(column+2, matchs)
# matchDic = {}
# read2output(3, matchs)

# 关闭 Excel 文件
workbook.close()

print(list(matchDic.keys()))
filtered_array = [x for x in matchs if x not in list(matchDic.keys())]

print("\n-------- Excel 未匹配的：\n")
for item in filtered_array:
    print(item)
print("\n-------- Excel 未匹配的\n")
