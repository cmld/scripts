import re
import baidu_tf


path = '/Users/clmdc/Desktop/live2120/lib/l10n/intl_zh_TW.arb'
out_path = '/Users/clmdc/Desktop/script/intl_zh_TW.arb'

# source_language = 'aotu'
source_language = 'cht'
# target_language = 'cht' #繁体cht  en
target_language = 'zh' #繁体cht  en
line_range = 15

f_in = open(path)
f_out = open(out_path, 'w')

line = f_in.readlines()

allOutLines = ['{\n']

for i in range(line_range):
	text = line[i]
	# print(text)

	kv = re.findall(r"\"(.+?)\"",text)
	
	if len(kv) > 1:
		dst = baidu_tf.translate(toLang=target_language,q=kv[1],fromLang=source_language)
		# dst = 'test'
		print(dst)
		outLine = '\"'+kv[0]+'\": '+'\"'+dst+'\",\n'
		allOutLines.append(outLine)
# allOutLines[-1]= allOutLines[-1][:-2] +'\n'

allOutLines.append('}')

f_out.writelines(allOutLines)
