
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
directory_path = '/Users/yk/Desktop/jt-customer-malaysia-ios/JTExpressMy'

regex_pattern = r'"([^"]*?)-r"'
matchs = extract_strings(directory_path, regex_pattern)
matchs = list(set(matchs))
print("\n待匹配：", matchs, "\n")
# for extracted_string in matchs:
#     print(extracted_string)


## 对比本地
filename = '/Users/yk/Desktop/jt-customer-malaysia-ios/JTExpressMy/Public/Lanauage/zh-Hans.lproj/Localizable.strings'

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
print("\n未匹配的：", filtered_array)