import os

manifest_path = 'mobile_app/android/app/src/main/AndroidManifest.xml'
if os.path.exists(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if '<uses-permission android:name="android.permission.INTERNET"/>' not in text:
        text = text.replace(
            '<application',
            '    <uses-permission android:name="android.permission.INTERNET"/>\n    <application'
        )
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(text)
