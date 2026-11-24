#!/data/data/com.termux/files/usr/bin/bash
set -e
pkg update -y
pkg upgrade -y
pkg install -y python git cmake clang make ffmpeg wget
python -m pip install --upgrade yt-dlp
mkdir -p "$HOME/bro_clipper"
if [ ! -d "$HOME/whisper.cpp" ]; then
  git clone --depth 1 https://github.com/ggml-org/whisper.cpp.git "$HOME/whisper.cpp"
fi
cd "$HOME/whisper.cpp"
cmake -B build
cmake --build build --config Release -j2
bash ./models/download-ggml-model.sh tiny
mkdir -p "$HOME/storage/shared/Movies/BRO_CLIPPER"
echo
echo "BRO CLIPPER AI instalado. Copia bro_clipper.py a ~/bro_clipper/"
echo "Luego ejecuta: python ~/bro_clipper/bro_clipper.py"
