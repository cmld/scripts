

projectName=JtStation-Indonesia-iOS

#获取当前环境路径
prejectFilePath=`pwd` 
workspacePath=$prejectFilePath/$projectName.xcworkspace

echo $workspacePath

time=$(date "+%Y-%m-%d-%H:%M:%S")

# ipa导出成功后的存放路径
output=/Users/yk/Desktop/archives/$projectName/$time
# 构建完成功后文件存放路径
archiveOutput=$output/$projectName.xcarchive
# 导出相关设置文件的位置路径 第一次需要用xcode Preoject->Archive, .xcarchive显示包内容中获取到
plistPath=/Users/yk/Desktop/archives/$projectName/ExportOptions-ad.plist


# 命令
xcodebuild clean -workspace $workspacePath -scheme $projectName -configuration Release 
xcodebuild archive -workspace $workspacePath -scheme $projectName -archivePath $archiveOutput -destination 'generic/platform=iOS'
xcodebuild -exportArchive -archivePath $archiveOutput -exportPath $output -exportOptionsPlist $plistPath


#--------------------------------------------#
# 需要配置绝对路径
ipaPath=$output/$projectName.ipa


### 方法简要说明：
### 1. 是先查找一个字符串：带双引号的key。如果没找到，则直接返回defaultValue。
### 2. 查找最近的冒号，找到后认为值的部分开始了，直到在层数上等于0时找到这3个字符：,}]。
### 3. 如果有多个同名key，则依次全部打印（不论层级，只按出现顺序）
### @author lux feary
###
### 3 params: json, key, defaultValue
function getJsonValuesByAwk() {
    awk -v json="$1" -v key="$2" -v defaultValue="$3" 'BEGIN{
        foundKeyCount = 0
        while (length(json) > 0) {
            # pos = index(json, "\""key"\""); ## 这行更快一些，但是如果有value是字符串，且刚好与要查找的key相同，会被误认为是key而导致值获取错误
            pos = match(json, "\""key"\"[ \\t]*?:[ \\t]*");
            if (pos == 0) {if (foundKeyCount == 0) {print defaultValue;} exit 0;}

            ++foundKeyCount;
            start = 0; stop = 0; layer = 0;
            for (i = pos + length(key) + 1; i <= length(json); ++i) {
                lastChar = substr(json, i - 1, 1)
                currChar = substr(json, i, 1)

                if (start <= 0) {
                    if (lastChar == ":") {
                        start = currChar == " " ? i + 1: i;
                        if (currChar == "{" || currChar == "[") {
                            layer = 1;
                        }
                    }
                } else {
                    if (currChar == "{" || currChar == "[") {
                        ++layer;
                    }
                    if (currChar == "}" || currChar == "]") {
                        --layer;
                    }
                    if ((currChar == "," || currChar == "}" || currChar == "]") && layer <= 0) {
                        stop = currChar == "," ? i : i + 1 + layer;
                        break;
                    }
                }
            }

            if (start <= 0 || stop <= 0 || start > length(json) || stop > length(json) || start >= stop) {
                if (foundKeyCount == 0) {print defaultValue;} exit 0;
            } else {
                print substr(json, start, stop - start);
            }

            json = substr(json, stop + 1, length(json) - stop)
        }
    }'
}



# API2.0
# RESULT=`curl -H "Content-Type: application/json" -s -X POST "https://www.pgyer.com/apiv2/app/getCOSToken?_api_key=$apiKey&buildType=ipa"`    
# echo $RESULT ;

# data=`getJsonValuesByAwk "$RESULT" "data" "defaultValue"`

# params=`getJsonValuesByAwk "$data" "params" "defaultValue"`

# signature=`getJsonValuesByAwk "$params" "signature" "defaultValue"`
# echo $signature
# token=`getJsonValuesByAwk "$params" "x-cos-security-token" "defaultValue"`
# echo $token
# key=`getJsonValuesByAwk "$params" "key" "defaultValue"`
# echo $key
# endpoint=`getJsonValuesByAwk "$data" "endpoint" "defaultValue"`
# echo $endpoint

# 上传接口失败 不知道为啥么
# curl -H "Content-Type: multipart/form-data" -D - --form-string "key=$key" --form-string "signature=$signature" --form-string "x-cos-security-token=$token" -F "file=@/Users/yk/Desktop/Payload.ipa" $endpoint

# 蒲公英用户信息
apiKey=90fbb4990c5322bf4d524a739fad2d0d
userKey=a7d0381752b8f4a5b4ad2176f1d815c3

# API 1.0
UPLOAD=`curl -F "file=@$ipaPath" \
-F "uKey=$userKey" \
-F "_api_key=$apiKey" \
http://www.pgyer.com/apiv1/app/upload`

data=`getJsonValuesByAwk "$UPLOAD" "data" "defaultValue"`
buildV=`getJsonValuesByAwk "$data" "appBuildVersion" "defaultValue"`
shortUrl=`getJsonValuesByAwk "$data" "appShortcutUrl" "defaultValue"`

echo "http://www.pgyer.com/"$shortUrl | tr -d '"'
echo "build:" $buildV
