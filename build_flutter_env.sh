echo '开始搭建FLutter环境 作者：clmd'

# 下载FLutter sdk 文件
user_path="/Users/builder" #自己的用户文件路径
flutter_path="$user_path/Library/flutter" #flutterSDK存放的位置

if [ -e $flutter_path ]
then
	echo "flutter SDK 在当前路径下已存在"
else
	echo "flutter SDK 开始下载"
	# flutterSDK的下载地址 查看列表_url-> https://mirrors.tuna.tsinghua.edu.cn/flutter/flutter_infra/releases/stable/macos
	flutter_download_url="https://mirrors.tuna.tsinghua.edu.cn/flutter/flutter_infra/releases/stable/macos/flutter_macos_3.10.0-stable.zip" 

	curl -o "$user_path/Downloads/flutter.zip" $flutter_download_url

	unzip -d "$user_path/Library" "$user_path/Downloads/flutter.zip"

	echo 'fLutter SDK 下载完成！！'
fi

# 配置FLutter环境变量
env_path="$user_path/.zshrc"

if [ -e $env_path ]
then
	echo "export PATH=\${PATH}:$flutter_path/bin
	export PUB_HOSTED_URL=https://pub.flutter-io.cn
	export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
	" >> $env_path
else
	touch $env_path

fi

if [ -e $env_path ]
then
	echo "export PATH=\${PATH}:$flutter_path/bin
	export PUB_HOSTED_URL=https://pub.flutter-io.cn
	export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
	" > $env_path
fi

source $env_path

echo 'flutter 环境配置完成！！'

flutter --version

flutter doctor 