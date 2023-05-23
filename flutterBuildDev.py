import subprocess
import time
import sys
import requests # pip3 install requests
import json

user_path = '/Users/clmdc'
sudo_password = '\'\'\'\''

projectDir = f"{user_path}/Desktop/live2120"

# dev相关
buildFile = f"{projectDir}/build/ios/iphoneos/Runner.app"

outfile = f"{user_path}/Desktop/Payload"
zipOutfile = f"{user_path}/Desktop/ipas/Payload-" + time.strftime("%Y-%m-%d-%H-%M", time.localtime()) + ".ipa"
# zipOutfile ="/Users/clmdc/Desktop/ipas/Payload-2023-05-22-15-59.ipa"

# 蒲公英相关
api_key = "90fbb4990c5322bf4d524a739fad2d0d"
appKey = "f2853bd956733635858257483daaea71"


# 执行命令
flutterBuildOption = "flutter build ios --dart-define=LANGUAGE_ENV=cht"

rmOption = f"rm -R {user_path}/Desktop/Payload/Runner.app"

cpOption = f"cp -r {buildFile} {outfile}"

zipOption = f"zip -q -r {zipOutfile} ./Payload/Runner.app"

print("==============================================")

print(flutterBuildOption + "\n")
subprocess.run(flutterBuildOption, shell=True, cwd=projectDir)
print("flutter build finish \n")

print("==============================================")

print(rmOption + "\n")
subprocess.call(rmOption, shell=True)
print("rm option finish \n")

print("==============================================")

print(cpOption + "\n")
subprocess.call(cpOption, shell=True)
print("cp option finish \n")

print("==============================================")

print(zipOption + "\n")
subprocess.run(zipOption, shell=True,cwd=f'{user_path}/Desktop/')
print("zip option finish \n")

print("==============================================")


# 蒲公英 上传APP API 1.0 即将弃用
# uploadOption = f"sudo curl -F \'file=@{zipOutfile}\' -F \'_api_key={api_key}\' -F \'appKey={appKey}\' https://www.pgyer.com/apiv2/app/upload" 
# print(uploadOption + "\n")

# subprocess.run(uploadOption, shell=True)
# print("upload option finish")


# 蒲公英 上传APP API 2.0 
uploadType = 'ipa'

url = 'https://www.pgyer.com/apiv2/app/getCOSToken'
params = {'_api_key':api_key,'buildType':uploadType}
result= requests.post(url=url, params=params)
print('\n'+result.text+'\n')

resultData = json.loads(result.text)

params_2 = resultData['data']['params']
key=params_2['key']
signature=params_2['signature']
token = params_2['x-cos-security-token']

endpoint = resultData['data']['endpoint']

uploadOption = f"echo \"{sudo_password}\" | sudo -S curl -D - --form-string \'key={key}\' --form-string \'signature={signature}\' --form-string \'x-cos-security-token={token}\' -F \'file=@{zipOutfile}\' {endpoint}" 
print(uploadOption + "\n")
subprocess.run(uploadOption, shell=True)
print("file upload finish")

