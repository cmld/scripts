flutter_path="/Users/clmdc/Downloads/flutter"
bp="/Users/clmdc/.bash_profile"

user_path="/Users/clmdc" 
env_path="$user_path/.zshrc"
if [ -e $env_path ]
then
	echo "export PATH=\${PATH}:$flutter_path/bin
	export PUB_HOSTED_URL=https://pub.flutter-io.cn
	export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
	" >> "$user_path/Desktop/test.txt"

	echo "exist"
else
	echo "no exist"
fi
