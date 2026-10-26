<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.
<!-- LOVABLE:END -->

## Architecture rules
- Render the decorative research-studio background once in the root layout; animate it only with CSS and disable motion for reduced-motion users so pages share a lightweight, accessible backdrop.
- All backend calls go through `src/lib/api.ts` (fetch client + normalizers); components never call fetch directly — keeps the Spring Boot contract in one place.
- Raw API responses are normalized into `src/types/api.ts` view-models with tolerant field aliases — the backend schema wasn't available when built.
- Never fabricate data: missing fields render as "—"/unavailable states, no mock data in real flows.
- Comparison job IDs are tracked in localStorage (`trackedComparisons` in `src/lib/queries.ts`) because the backend has no list-comparisons endpoint; content is always fetched from the server.
