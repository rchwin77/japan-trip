#!/usr/bin/env python3
"""카톡에서 복사한 링크 묶음을 links.json에 합칩니다 (중복은 자동 제거).

사용법:  python add_links.py 붙여넣은파일.txt
- 같은 인스타 게시물은 뒤에 붙는 추적용 ?xxx= 값이 달라도 같은 링크로 봅니다.
- 이미 있는 링크의 요약/메모는 그대로 둡니다.
"""
import json, re, sys
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).parent
DB = HERE / "links.json"

LINE = re.compile(r"^\[(?P<who>[^\]]+)\]\s*\[(?P<time>[^\]]+)\]\s*(?P<body>.*)$")
DATE = re.compile(r"^(\d{4})년 (\d{1,2})월 (\d{1,2})일")
URL = re.compile(r"https?://\S+")


def key_and_type(url):
    u = urlparse(url)
    host = u.netloc.lower().replace("www.", "").replace("m.", "", 1) if u.netloc.lower().startswith("m.") else u.netloc.lower().replace("www.", "")
    path = u.path.rstrip("/")
    if "instagram.com" in host:
        m = re.search(r"/(reel|reels|p|tv)/([^/]+)", path)
        code = m.group(2) if m else path
        return f"ig:{code}", "instagram", f"https://www.instagram.com/{'p' if m and m.group(1)=='p' else 'reel'}/{code}/"
    if "youtu" in host:
        m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{6,})", url)
        vid = m.group(1) if m else path
        return f"yt:{vid}", "youtube", f"https://www.youtube.com/watch?v={vid}"
    if "blog.naver.com" in host:
        return f"nv:{path}", "blog", f"https://m.blog.naver.com{path}"
    if "chatgpt.com" in host or "chat.openai.com" in host:
        return f"gpt:{path}", "chatgpt", f"https://chatgpt.com{path}"
    return f"web:{host}{path}", "web", url.split("#")[0]


def main(src):
    data = json.loads(DB.read_text(encoding="utf-8")) if DB.exists() else {"links": []}
    seen = {l["key"]: l for l in data["links"]}
    date, added, dup = None, 0, 0
    for raw in Path(src).read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        d = DATE.match(raw)
        if d:
            date = f"{d.group(1)}-{int(d.group(2)):02d}-{int(d.group(3)):02d}"
            continue
        m = LINE.match(raw)
        who, time, body = (m.group("who"), m.group("time"), m.group("body")) if m else ("", "", raw)
        for url in URL.findall(body):
            key, typ, clean = key_and_type(url)
            if key in seen:
                dup += 1
                continue
            title_hint = body.replace(url, "").strip(" -:")
            item = {"key": key, "type": typ, "url": clean, "from": who,
                    "sent": f"{date or ''} {time}".strip(), "title": title_hint,
                    "summary": "", "status": "unread", "tags": [], "day": None}
            data["links"].append(item)
            seen[key] = item
            added += 1
    DB.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"새 링크 {added}개 추가, 중복 {dup}개 건너뜀, 전체 {len(data['links'])}개")


if __name__ == "__main__":
    main(sys.argv[1])
