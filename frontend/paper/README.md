# Welcome to your Lovable project

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Open your project in the [Lovable editor](https://lovable.dev) and keep building.

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: connect the project to GitHub and every change made in Lovable is committed straight to your repository.
- **Full ownership**: this code is yours. Push to your repository and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```

## Built with

- TanStack Start
- TypeScript
- React
- Tailwind CSS

## PaperTrail frontend

Set `VITE_API_BASE_URL` (default `http://localhost:8080`) to point at the Spring Boot API. The browser never calls the Python AI service directly.

Connected endpoints: `GET /api/health`, `GET/POST /api/papers` (multipart field `files`), `GET/DELETE /api/papers/{id}`, `POST /api/compare` (`{ paperIds, question? }`), `GET /api/compare/{jobId}` (polled), `POST /api/evidence/verify` (`{ claim, paperIds }`), `GET /api/reports/{comparisonId}/markdown`.

Missing backend capabilities (UI shows honest unavailable states):
- No endpoint to list comparisons/reports — the UI lists comparison IDs started in this browser.
- No page-level text endpoint for papers — shown only if `GET /api/papers/{id}` returns a `pages` array.
- No verification history endpoint — history is not shown.
- No retry-processing or cancel-comparison endpoint.
- No dedicated research-gap endpoint — gaps come from `researchGaps`/`gaps` in comparison results.

Request/response field names were not verified against an OpenAPI spec; normalizers in `src/lib/api.ts` accept common variants. Confirm against the backend and adjust there.
