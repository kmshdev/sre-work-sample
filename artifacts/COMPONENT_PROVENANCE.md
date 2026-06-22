# Component Provenance

This repository uses the following devl component pages and shadcn registry
items as visual and structural references for the static candidate guidance
page:

- `https://www.devl.dev/c/timelines/changelog`
- `https://www.devl.dev/c/tours/checklist`
- `https://www.devl.dev/c/layouts/focus-mode`
- `https://www.devl.dev/c/tables/issues`
- `https://www.devl.dev/r/timelines/changelog.json`
- `https://www.devl.dev/r/tours/checklist.json`
- `https://www.devl.dev/r/layouts/focus-mode.json`
- `https://www.devl.dev/r/tables/issues.json`

Reference extraction commands:

```sh
npx shadcn@latest init
npx shadcn@latest registry add @coss
npx shadcn@latest add https://www.devl.dev/r/timelines/changelog.json
npx shadcn@latest add https://www.devl.dev/r/tours/checklist.json
npx shadcn@latest add https://www.devl.dev/r/layouts/focus-mode.json
npx shadcn@latest add https://www.devl.dev/r/tables/issues.json
```

The implementation uses original HTML and CSS in this repository. It does not
vendor the React components, assets, or package dependencies into the candidate
template. The static page adapts the visible component anatomy to assignment
guidance: changelog timeline, onboarding checklist, focus-mode reading layout,
and issue-table evidence tracking.
