#!/usr/bin/env python3
"""
prep_video.py - free local replacement for the "watch + transcribe" half of
Sandcastles' analyze_video. It does NOT label the video; it prepares the
evidence so the agent can label it (topic, hooks, format, structure...).

For one video URL (YouTube / TikTok via yt-dlp; Instagram needs a direct
videoUrl from the Apify reel scraper because instagram.com is behind login):
  1. downloads the video (<=720p) to DIR/video.mp4  (skip with --no-video)
  2. extracts 16 kHz mono audio -> DIR/audio.wav
  3. transcribes with stt_words.py (faster-whisper, CPU, free) ->
     DIR/words.json + DIR/transcript.txt   (first 3 s also in hook_words)
  4. grabs the opening frames at 0, 0.5, 1, 2, 3 s -> DIR/hook_*.jpg
     and a 4x3 contact sheet of the whole video -> DIR/sheet.jpg
  5. writes DIR/analysis.json: the metadata you pass in plus EMPTY label
     fields for the agent to fill after reading the transcript and frames.

Usage:
  python3 prep_video.py URL --dir out/<id> [--lang en] [--meta video.json]
         [--model small] [--no-stt] [--no-video]
"""
import argparse, json, os, subprocess, sys

STT = os.environ.get("STT_WORDS", "/workspace/exports/bot-video/tools/stt_words.py")
# faster-whisper lives in /workspace/tools/venv (not in system python)
STT_PY = os.environ.get("STT_PYTHON") or next(
    (p for p in ("/workspace/tools/venv/bin/python",) if os.path.exists(p)), sys.executable)
LABEL_FIELDS = [
    "video_summary", "topic", "idea_seed", "why_interesting", "unique_angle",
    "spoken_hook", "spoken_hook_category", "spoken_hook_madlib",
    "visual_hook", "text_hook", "hook_alignment",
    "format_category", "why_format_works",
    "contrast_common_belief", "contrast_reality",
    "story_structure", "cta_type", "cta_placement", "visual_layout",
    "production_notes",
]


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def duration(path):
    p = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    try:
        return float(p.stdout.strip())
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("--dir", required=True)
    ap.add_argument("--lang", default="en"); ap.add_argument("--model", default="small")
    ap.add_argument("--meta", help="normalized video JSON (one object) to embed")
    ap.add_argument("--no-stt", action="store_true"); ap.add_argument("--no-video", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.dir, exist_ok=True)
    vid = os.path.join(a.dir, "video.mp4")
    out = {"url": a.url, "errors": []}
    if a.meta:
        out["meta"] = json.load(open(a.meta, encoding="utf-8"))
    if not os.path.exists(vid):
        p = sh(["yt-dlp", "-f", "bv*[height<=720]+ba/b[height<=720]/b", "--merge-output-format", "mp4",
                "-o", vid, a.url], timeout=600)
        if p.returncode != 0:
            out["errors"].append("download failed: " + (p.stderr.strip().splitlines() or ["?"])[-1])
            json.dump(out, open(os.path.join(a.dir, "analysis.json"), "w"), indent=1, ensure_ascii=False)
            sys.exit(f"download failed for {a.url}")
    dur = duration(vid)
    out["duration_s"] = dur
    wav = os.path.join(a.dir, "audio.wav")
    sh(["ffmpeg", "-y", "-v", "error", "-i", vid, "-ac", "1", "-ar", "16000", wav])
    for t in (0, 0.5, 1, 2, 3):
        if dur and t < dur:
            sh(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", vid, "-frames:v", "1",
                "-vf", "scale=360:-2", os.path.join(a.dir, f"hook_{t}s.jpg")])
    if dur:
        fps = 12 / dur
        sh(["ffmpeg", "-y", "-v", "error", "-i", vid, "-vf",
            f"fps={fps:.4f},scale=240:-2,tile=4x3", "-frames:v", "1", os.path.join(a.dir, "sheet.jpg")])
    if not a.no_stt:
        wj = os.path.join(a.dir, "words.json")
        p = sh([STT_PY, STT, wav, wj, "--lang", a.lang, "--model", a.model], timeout=1800)
        if p.returncode == 0 and os.path.exists(wj):
            words = json.load(open(wj))
            text = " ".join(w["w"] for w in words)
            open(os.path.join(a.dir, "transcript.txt"), "w").write(text)
            out["transcript"] = text
            out["hook_words_first_3s"] = " ".join(w["w"] for w in words if w["start"] < 3.0)
            out["non_verbal"] = len(words) < 5
        else:
            out["errors"].append("stt failed: " + (p.stderr.strip().splitlines() or ["?"])[-1])
    if a.no_video:
        os.remove(vid)
    out["frames"] = sorted(f for f in os.listdir(a.dir) if f.endswith(".jpg"))
    out["labels"] = {k: None for k in LABEL_FIELDS}
    out["labels_by"] = "agent, from transcript + frames (fill in; never invent)"
    json.dump(out, open(os.path.join(a.dir, "analysis.json"), "w"), indent=1, ensure_ascii=False)
    print(f"ready: {a.dir}/analysis.json ({dur and round(dur,1)} s, frames: {len(out['frames'])}, "
          f"errors: {len(out['errors'])})")


if __name__ == "__main__":
    main()
