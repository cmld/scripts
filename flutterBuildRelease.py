import subprocess

projectDir = "/Users/clmdc/Desktop/live2120"


# 上线相关
ipaFile = "/Users/clmdc/Desktop/live2120/build/ios/ipa/live120.ipa"
# APP Store 相关
store_api_key = "ZJMYF5549N"
store_issuer_id = "a8f0a29b-e82f-4783-af5d-0128710b4bd1"


# 上线相关命令
buildReleaseOption = "flutter build ipa --release --dart-define=LANGUAGE_ENV=cht"
uploadToStoreOption = f"xcrun altool --upload-app --type ios -f {ipaFile} --apiKey {store_api_key} --apiIssuer {store_issuer_id}"

subprocess.run(buildReleaseOption, shell=True, cwd=projectDir)
print("flutter build finish")
subprocess.run(uploadToStoreOption, shell=True)
print("upload ipa finish")