import csv
import io
import os
from pathlib import Path

from mutagen.easyid3 import EasyID3
from pydub import AudioSegment
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile

current = Path(__file__).parent
voicevox_core_path = current / "voicevox_core"
voicevox_onnxruntime_path = (
    voicevox_core_path / "onnxruntime/lib/" / Onnxruntime.LIB_VERSIONED_FILENAME
)
open_jtalk_dict_dir = voicevox_core_path / "dict/open_jtalk_dic_utf_8-1.11"
synthesizer = Synthesizer(
    Onnxruntime.load_once(filename=str(voicevox_onnxruntime_path)),
    OpenJtalk(open_jtalk_dict_dir),
)

with VoiceModelFile.open(voicevox_core_path / "models/vvms/4.vvm") as model:
    synthesizer.load_voice_model(model)

fmt: str = "mp3"
style_id: int = 21  # ねこつか
s1_path = Path("./silent1sec.wav")
s5_path = Path("./silent5sec.wav")


def ensure_silent_wav(path: Path, ms: int):
    if not path.exists():
        silent = AudioSegment.silent(duration=ms)
        silent.export(path, format="wav")


ensure_silent_wav(s1_path, 1000)
ensure_silent_wav(s5_path, 5000)


s1: AudioSegment = AudioSegment.from_file(s1_path)
s5: AudioSegment = AudioSegment.from_file(s5_path)


def main():
    with open("./data.csv", "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    for row in reader[1:]:
        path = f"{row[0].zfill(2)}_{row[1]}"
        file = Path(path) / f"{row[2].zfill(2)}_{row[3][:8]}.{fmt}"
        textQ = f"問題、{row[3]}"
        textA = f"答え、{row[4]}"
        if row[5].upper() != "Y":
            continue
        print(file)
        os.makedirs(path, exist_ok=True)

        # wave_bytes = synthesizer.tts(textQ, style_id)  # 音声合成を行う

        q = AudioSegment.from_file(io.BytesIO(synthesizer.tts(textQ, style_id)), format="wav")
        a = AudioSegment.from_file(io.BytesIO(synthesizer.tts(textA, style_id)), format="wav")
        # with open("Q.wav", "wb") as f:
        #     f.write(wave_bytes)  # ファイルに書き出す
        # wave_bytes = synthesizer.tts(textA, style_id)  # 音声合成を行う
        # with open("A.wav", "wb") as f:
        #     f.write(wave_bytes)  # ファイルに書き出す
        # q = AudioSegment.from_file(
        #     io.BytesIO(synthesizer.tts(textQ, style_id)), format="wav"
        # )
        # a = AudioSegment.from_file(
        #     io.BytesIO(synthesizer.tts(textA, style_id)), format="wav"
        # )

        out = s1 + q + s5 + a + s1
        out.export(file, format=fmt)

        try:
            tags = EasyID3(file)
        except Exception:
            tags = EasyID3()

        tags["title"] = f"{path}_{row[2].zfill(2)}"
        tags["artist"] = f"{path}"
        tags["albumartist"] = f"{path}"
        tags["album"] = f"{path}"
        tags["tracknumber"] = f"{row[2].zfill(2)}"
        tags.save()



if __name__ == "__main__":
    main()
