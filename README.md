# 設定方法

## VOICEVOX Core の Linux 版のインストール
### ubuntuでの作業
#### 他のライブラリ
```zsh
sudo apt update
sudo apt install -y ffmpeg libgomp1 libsndfile1
```
#### VOICEVOXの導入
```zsh
mkdir ./.downloads
cd ./downloads
wget https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.3/download-linux-x64
chmod +x download-linux-x64
./download-linux-x64
mv ./.downloads/voicevox_core/ ./voicevox_core
```

#### ライブラリ
```powershell
uv add pydub mutagen

uv add https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.3/voicevox_core-0.16.3-cp310-abi3-manylinux_2_34_x86_64.whl
```