# Project rules (what goes into a new project's `CLAUDE.md`)

Show this to the user at kickoff and put in only what is approved. Do not add rules the user did not ask for. Use the block in the project's document language (`references/doc-style.md`).

English:

```markdown
# <Project name>: project rules

This project follows the sdd skill. Start it with `/skill:sdd <request>` in omp, `/sdd <request>` in Claude Code.

## Process

- Work in small steps. Do one step at a time and move on only after confirming with the user.
- Flow of development: input material → drawing out the intent (brainstorming) → spec → domain → ADR → plan → implementation.
- Implement by plan task. Tests **MUST** be written before the code.
- Test command: `<the command that runs all tests>`

## Work journal

- At the end of every step, the step **MUST** be recorded in `docs/journal/YYYY-MM-DD.md`.
- Items written for every step: request or question, what was done, verification. A step that only commits or pushes writes the first two. Write the other items only when they have content.
- Project documents hold only conclusions. The process goes into the journal.

## Documents

- Document language: <Korean or English>. Code identifiers, paths and technical terms **MAY** stay in their original form.
- Requirement levels are written with RFC 2119 keywords.
```

Korean:

```markdown
# <프로젝트 이름>: 프로젝트 규칙

이 프로젝트는 sdd 스킬을 따른다. omp에서는 `/skill:sdd <요청>`, Claude Code에서는 `/sdd <요청>`으로 시작한다.

## 진행 방식

- 작게 나누어 진행한다. 한 번에 한 스텝만 하고, 사용자와 확인한 뒤에 다음으로 넘어간다.
- 개발 흐름: 입력 자료 → 의도 끌어내기(브레인스토밍) → 스펙 → 도메인 → ADR → 계획 → 구현.
- 계획의 작업 단위로 구현한다. 테스트는 코드보다 **반드시 먼저 써야 한다**.
- 테스트 명령: `<모든 테스트를 실행하는 명령>`

## 작업 저널

- 모든 스텝이 끝나면 그 스텝을 `docs/journal/YYYY-MM-DD.md`에 **반드시 기록해야 한다**.
- 스텝마다 쓰는 항목: 요청 또는 질문, 한 일, 검증. 커밋이나 푸시만 하는 스텝은 앞의 두 가지를 쓴다. 다른 항목은 내용이 있을 때만 쓴다.
- 프로젝트 문서에는 결론만 둔다. 과정은 저널에 쓴다.

## 문서

- 문서 언어: <한국어 또는 영어>. 코드 식별자, 경로, 기술 용어는 원래 형태로 **둘 수 있다**.
- 요구 수준은 RFC 2119 키워드로 쓴다.
```
