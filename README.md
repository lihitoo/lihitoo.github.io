# ThunderPunch Studio

Official website: https://lihitoo.github.io/

A responsive static HTML/CSS site. No framework, JavaScript, backend, external fonts, or build dependencies.

## Local preview and validation

```sh
python scripts/check_site.py
python -m http.server 8080 --bind 127.0.0.1
```

Open http://127.0.0.1:8080/. Stop the server with Ctrl+C.

HTML, CSS and download links use relative paths. The social preview image uses the absolute production URL.

## Deployment

Repository **Settings > Pages > Build and deployment > Source** must be **GitHub Actions**. The workflow in `.github/workflows/pages.yml` validates the site, stages only its public files, and deploys on pushes to `main`. It also supports **Actions > Deploy ThunderPunch Studio > Run workflow**. It needs `contents: read`, `pages: write`, and `id-token: write`, and uses the `github-pages` environment.

Check the workflow's deployment URL and successful run before considering a release live. Pages CDN/browser caches may briefly serve the previous version.

Reference: [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Contact information

Contact and product support: [trinhtuu.05@gmail.com](mailto:trinhtuu.05@gmail.com).

The four ThunderPunch PNGs in assets/ are the originals supplied by the studio. They are downloadable under Brand assets.

## Diagnosis (22 November 2026)

- The initial commit contained only a default README and no `index.html`.
- Failed Pages run `45029461144` attempted to build `./docs`, which does not exist. Current settings at inspection were already `main` and `/(root)`; the public URL returned the old Lihto HTML with HTTP 200.
- Only one `index.html` exists. Its favicon and both logo images referenced `assets/lihto-logo.png`, but the actual file is `lihto-logo.png` at the root. Those references were fixed without moving the logo.
- The former default-page symptom was not reproducible at inspection. The missing original entry point and failed `/docs` builds explain earlier publishing failures; an old cached page is also possible but was not proven.
- Deployment now explicitly publishes a validated static artifact through Actions, avoiding an implicit Jekyll/README fallback.
