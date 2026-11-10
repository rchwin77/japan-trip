# 도쿄 가족여행 (2026.11.15 ~ 11.18)

모바일용 여행 페이지 (GitHub Pages).

- `index.html` 메인 (일정 / 참고 링크 / 준비물)
- `route.html` 시부야 스카이 → 호텔 대중교통 안내
- `trip.json` 일정 데이터 — 일정이 바뀌면 여기만 고치면 됨
- `links.json` 가족이 보낸 링크 + 요약

## 링크 추가
카톡 대화를 그대로 `inbox/새파일.txt`로 저장한 뒤:

    python add_links.py inbox/새파일.txt

같은 인스타 게시물은 주소 뒤 추적값이 달라도 자동으로 중복 제거돼요.
