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
directory_path = '/Users/yk/Desktop/JTS-Malaysia-VIP-iOS/Malaysia Customer App/Main'
regex_pattern = r'"([^"]*?)-r"'
matchs = extract_strings(directory_path, regex_pattern)
matchs = list(set(matchs))
print("\n待匹配：", matchs, "\n")
# for extracted_string in matchs:
#     print(extracted_string)


############

## 以下是搜索输出
matchs = ['邮箱验证', '验证成功', '请再次输入密码', '确认', '请输入验证码', '邮箱收不到验证码？试试发送手机验证码！']

matchDic = {}

# 打开 Excel 文件
workbook = openpyxl.load_workbook('transfiden1.xlsx')
sheet = workbook.worksheets[1] # 选择工作表（Sheet），默认选择第一个工作表 索引从0开始
column = 1 # 文本从第几列开始
def read2output(language, matchs):
    
    # 读取每行的第一项
    for row in sheet.iter_rows(min_row=1, values_only=True):
        if row and row[column] and row[language]:  # 确保行非空
            if row[column] in matchs :
                key = row[column + 1].lower().replace(" ", "_")
                formatted_string = "\"%s\" = \"%s\"; // %s" % (key, row[language], row[column])
                matchDic["%s" % (row[column])] = key
                print(formatted_string)
                # matchs = [value for value in matchs if value != row[0]]

    print("\n")


read2output(1, matchs)
read2output(2, matchs)
read2output(3, matchs)

# 关闭 Excel 文件
workbook.close()

filtered_array = [x for x in matchs if x not in list(matchDic.keys())]
print("\n未匹配的：", filtered_array)


