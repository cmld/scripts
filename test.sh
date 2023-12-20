# flutter_path="/Users/clmdc/Downloads/flutter"
# bp="/Users/clmdc/.bash_profile"

# user_path="/Users/clmdc" 
# env_path="$user_path/.zshrc"
# if [ -e $env_path ]
# then
# 	echo "export PATH=\${PATH}:$flutter_path/bin
# 	export PUB_HOSTED_URL=https://pub.flutter-io.cn
# 	export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
# 	" >> "$user_path/Desktop/test.txt"

# 	echo "exist"
# else
# 	echo "no exist"
# fi

# ipaPath=/Users/yk/Desktop/jt-out-malaysia/build/ios/ipa/jt_out_malaysia.ipa
# store_api_key="RB9S793N8C"
# store_issuer_id="a069fa47-aa6d-4256-8f6b-9ad3851f03c4"

# xcrun altool --upload-app --type ios -f $ipaPath --apiKey $store_api_key --apiIssuer $store_issuer_id --verbose

# 获取当前文件夹下指定后缀的文件名，不递归子目录
extension=".xcworkspace"
file=$(find . -maxdepth 1 -type f -name "*$extension" | head -n 1)
projectName=$(basename "$file" "$extension")
if [ -z "$projectName" ]; then
    echo "没有找到后缀为 $extension 的文件"
    test="hh"
fi
echo "$filename" 
echo "$test"