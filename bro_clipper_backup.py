#!/usr/bin/env python3
import os, re, json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path.home() / "bro_clipper"
WORK = ROOT / "work"
OUT = Path.home() / "storage" / "shared" / "Movies" / "BRO_CLIPPER"
MODEL = Path.home() / "whisper.cpp" / "models" / "ggml-tiny.bin"
WHISPER = Path.home() / "whisper.cpp" / "build" / "bin" / "whisper-cli"

def run(cmd):
    print("\n▶", " ".join(map(str, cmd)))
    subprocess.run(list(map(str, cmd)), check=True)

def score(text):
    t = text.lower()
    cues = [
        "pero", "porque", "imagina", "increíble", "nunca", "siempre",
        "secreto", "error", "problema", "solución", "verdad", "mentira",
        "importante", "atención", "wow", "cómo", "por qué", "qué pasó",
        "no puede ser", "te voy a", "la clave", "lo mejor", "lo peor"
    ]
    value = sum(2 for w in cues if w in t)
    value += min(text.count("?") * 2 + text.count("!") * 2, 8)
    value += min(len(re.findall(r"\b\w+\b", text)) / 35, 3)
    if len(text.strip()) < 100:
        value -= 3
    return value

def main():
    print("\n=== BRO CLIPPER AI · BETA ===")
    print("Usa videos propios o cuyo uso tengas autorizado.\n")
    url = input("Pega el enlace de YouTube: ").strip()
    if not url:
        print("No pegaste ningún enlace."); return
    try:
        count = int(input("¿Cuántos clips quieres? (1-10, recomendado 5): ") or "5")
        count = max(1, min(10, count))
    except ValueError:
        count = 5

    for p in (WORK, OUT):
        p.mkdir(parents=True, exist_ok=True)

    video = WORK / "source.mp4"
    audio = WORK / "audio.wav"
    transcript_base = WORK / "transcript"

    if not shutil.which("yt-dlp") or not shutil.which("ffmpeg"):
        print("Faltan yt-dlp o ffmpeg. Ejecuta primero install.sh."); return
    if not WHISPER.exists() or not MODEL.exists():
        print("No encuentro Whisper o el modelo. Ejecuta primero install.sh."); return

    print("\n1/4 Descargando el video autorizado...")
    run(["yt-dlp", "--no-playlist", "-f", "bv*[height<=720]+ba/b[height<=720]",
         "--merge-output-format", "mp4", "-o", str(video), url])
    if not video.exists():
        print("No se encontró el archivo descargado."); return

    print("\n2/4 Preparando audio...")
    run(["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
         str(audio)])

    print("\n3/4 Transcribiendo en el teléfono (puede tardar)...")
    run([str(WHISPER), "-m", str(MODEL), "-f", str(audio), "-l", "auto",
         "-oj", "-of", str(transcript_base), "-np"])
    data_path = Path(str(transcript_base) + ".json")
    if not data_path.exists():
        print("Whisper no generó el archivo de transcripción."); return
    data = json.loads(data_path.read_text(encoding="utf-8"))
    segments = data.get("transcription", data.get("segments", []))
    if not segments:
        print("No se detectó voz suficiente para seleccionar clips."); return

    # Rank sliding windows using transcript content. This is an offline
    # heuristic selector, not a generative language model.
    print("\n4/4 Buscando momentos y exportando...")
    def stamp(value):
        if isinstance(value, (int, float)):
            n = float(value)
            return n / 1000 if n > 10000 else n
        value = str(value or "0").replace(",", ".")
        bits = value.split(":")
        try:
            return sum(float(part) * (60 ** i) for i, part in enumerate(reversed(bits)))
        except ValueError:
            return 0.0

    normalized = []
    for seg in segments:
        ts = seg.get("timestamps", {})
        a = stamp(seg.get("offset", seg.get("start", ts.get("from", 0))))
        if "duration" in seg:
            b = a + stamp(seg["duration"])
        else:
            b = stamp(seg.get("end", ts.get("to", a)))
        normalized.append((a, b, str(seg.get("text", ""))))

    duration = float(data.get("result", {}).get("duration", 0) or
                     max((b for a, b, txt in normalized), default=0))
    candidates = []
    start = 0.0
    while start < duration:
        end = min(start + 45.0, duration)
        parts = []
        for a, b, segment_text in normalized:
            if a < end and b > start:
                parts.append(segment_text)
        text = " ".join(parts).strip()
        if text:
            candidates.append((score(text), start, end, text))
        start += 15.0

    candidates.sort(reverse=True, key=lambda x: x[0])
    chosen = []
    for item in candidates:
        _, a, b, _ = item
        if all(b <= x[1] or a >= x[2] for x in chosen):
            chosen.append(item)
        if len(chosen) >= count:
            break
    chosen.sort(key=lambda x: x[1])

    if not chosen:
        print("No pude encontrar fragmentos. Prueba con un video con voz clara."); return

    for i, (sc, a, b, txt) in enumerate(chosen, 1):
        # Keep the last short segment from being needlessly tiny.
        target = OUT / f"BRO_CLIP_{i:02d}.mp4"
        print(f"\nClip {i}: {a:.0f}s–{b:.0f}s | puntuación {sc:.1f}")
        print("Texto:", txt[:240].replace("\n", " "))
        run(["ffmpeg", "-y", "-ss", f"{a:.2f}", "-i", str(video),
             "-t", f"{b-a:.2f}", "-vf",
             "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
             "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
             str(target)])

    print("\n¡Listo! Clips guardados en:")
    print(OUT)
    print("\nNota: la selección de esta versión es automática por señales del texto,")
    print("no comprende el contexto como un editor humano. Revisa cada clip antes de publicar.")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print("\nEl proceso falló. Revisa la conexión, el enlace y el espacio libre.")
        sys.exit(e.returncode)
