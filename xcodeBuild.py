import subprocess
import time
import sys



# 根据项目设置
projectName = "Retail_REA"
workspacePath = "/Users/clmd/Desktop/REA-APP-iOS/Retail_REA.xcworkspace"
appversion = sys.argv[1]
# 蒲公英相关
api_key = "90fbb4990c5322bf4d524a739fad2d0d"
appKey = "9970b513367a1df81dd2fa4d127c4b2a"

# 下面的参数自己设置
# ipa导出成功后的存放路径
output = f"/Users/clmd/Desktop/archives/{projectName}_{appversion}-" + time.strftime("%Y-%m-%d-%H-%M", time.localtime())
# 构建完成功后文件存放路径
archiveOutput = f"{output}/{projectName}.xcarchive"
# 导出相关设置文件的位置路径
plistPath = "/Users/clmd/Desktop/archives/optionsPlists/ExportOptions.plist"


# 清理项目
cleanOption = f"xcodebuild clean -workspace {workspacePath}  -scheme {projectName} -configuration Release"
print(cleanOption + "\n")
# 构建项目
buildArchive = f"xcodebuild archive -workspace {workspacePath} -scheme {projectName} -archivePath {archiveOutput}"
print(buildArchive + "\n")
# 导出ipa
exportOption = f"xcodebuild -exportArchive -archivePath {archiveOutput} -exportPath {output} -exportOptionsPlist {plistPath}"
print(exportOption + "\n")
# 上传ipa到蒲公英
uploadOption = f"sudo curl -F \'file=@{output}/{projectName}.ipa\' -F \'_api_key={api_key}\' -F \'appKey={appKey}\' https://www.pgyer.com/apiv2/app/upload" 
print(uploadOption + "\n")

# 执行shell
subprocess.call([cleanOption], shell=True)
subprocess.call([buildArchive], shell=True)
subprocess.call([exportOption], shell=True)
subprocess.call([uploadOption], shell=True)



