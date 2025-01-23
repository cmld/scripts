# 蒲公英用户信息
apiKey=90fbb4990c5322bf4d524a739fad2d0d
userKey=a7d0381752b8f4a5b4ad2176f1d815c3

# APP Store content上传相关  
# ++印尼驿站
# store_api_key="YF8Q5V5YV4" #生成的时候有个.p8文件需要下载放到用户文件目录下特定名字的文件夹里
# store_issuer_id="69a6de89-c6c9-47e3-e053-5b8c7c11a4d1"

# ++马来
store_api_key="RB9S793N8C" #生成的时候有个.p8文件需要下载放到用户文件目录下特定名字的文件夹里
store_issuer_id="a069fa47-aa6d-4256-8f6b-9ad3851f03c4"

#--------------------------------------------#

extension=".xcworkspace"
file=$(find . -regex ".*$extension" -maxdepth 1)
projectName=$(basename "$file" "$extension")

if [ -z "$projectName" ]; then
    echo "Error: 没有找到后缀为 $extension 的文件"
    exit
fi

#获取当前环境路径
prejectFilePath=`pwd` 
echo "当前环境路径: $prejectFilePath"

# 工作空间路径
workspacePath=$prejectFilePath/$projectName.xcworkspace
echo "工作空间路径: $workspacePath"

time=$(date "+%Y-%m-%d-%H:%M:%S")

if [ "$1" = "ipa" ];then
    # echo "生产包 上传App Store content"
    # ipa导出成功后的存放路径
    output=~/Desktop/archives/$projectName/Release/$time
    # 导出相关设置文件的位置路径 第一次需要用xcode Preoject->Archive, .xcarchive显示包内容中获取到
    plistPath=~/Desktop/archives/$projectName/ExportOptions-store.plist
else
    # echo "测试包 上传到蒲公英"
    # ipa导出成功后的存放路径
    output=~/Desktop/archives/$projectName/$time
    # 导出相关设置文件的位置路径 第一次需要用xcode Preoject->Archive, .xcarchive显示包内容中获取到
    plistPath=~/Desktop/archives/$projectName/ExportOptions-ad.plist
fi

# 构建完成功后文件存放路径
archiveOutput=$output/$projectName.xcarchive

# ipa文件路径
ipaFile=$output/$projectName.ipa

#--------------------------------------------#

build_pageage(){
    op=$1
    pp=$2
    config=$3

    echo "buildpath: $op | $pp | $config"
    # 命令
    xcodebuild clean -workspace "$workspacePath" -scheme "$projectName" -configuration "$config"
    xcodebuild archive -workspace "$workspacePath" -scheme "$projectName" -configuration "$config" -archivePath "$archiveOutput" -destination 'generic/platform=iOS'
    xcodebuild -exportArchive -archivePath "$archiveOutput" -exportPath "$op" -exportOptionsPlist "$pp"
    # if [ "$3" = "Release" ];then
    #     xcodebuild -exportArchive -archivePath "$archiveOutput" -exportPath "$op" -exportOptionsPlist "$pp"
    # else
    #     ipaDir=$output/Payload
    #     mkdir "$ipaDir"
    #     cp -r "$archiveOutput/Products/Applications/$projectName.app" "$ipaDir"
    #     ditto -c -k --sequesterRsrc --keepParent "$ipaDir" "$ipaFile"
    # fi
}


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


# API 1.0
upload_pgy(){
    ipaP=$1
    echo "ipa文件路径: $ipaP"

    UPLOAD=`curl -F "file=@\"$ipaP\"" \
    -F "uKey=$userKey" \
    -F "_api_key=$apiKey" \
    http://www.pgyer.com/apiv1/app/upload`

    echo $UPLOAD

    data=`getJsonValuesByAwk "$UPLOAD" "data" "defaultValue"`
    buildV=`getJsonValuesByAwk "$data" "appBuildVersion" "defaultValue"`
    shortUrl=`getJsonValuesByAwk "$data" "appShortcutUrl" "defaultValue"`

    echo "http://www.pgyer.com/"$shortUrl | tr -d '"'
    echo "build:" $buildV
}

#--------------------------------------------#


if [ "$1" = "ipa" ];then
    echo "生产包 上传App Store content"
    build_pageage "$output" "$plistPath" "Release"
    # 通过api_key上传到App Store content
    xcrun altool --upload-app --type ios -f "$ipaFile" --apiKey $store_api_key --apiIssuer $store_issuer_id --verbose
elif [ "$1" = "release" ]; then
    echo "测试包Release 上传到蒲公英"
    build_pageage "$output" "$plistPath" "Release"
    upload_pgy "$ipaFile"
else
    echo "测试包UAT 上传到蒲公英"
    build_pageage "$output" "$plistPath" "ReleaseUat"
    upload_pgy "$ipaFile"
fi

