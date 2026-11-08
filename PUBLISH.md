# Putting the site online

Everything that is meant to be public is in the `site/` folder. `sh tools/build.sh` rebuilds it, and `make-site.py` also writes
**`van-site.zip`**: the whole of `site/` in one zip with `index.html` at the top, ready to upload.

## The easy way (no account setup, a few minutes)

1. Unzip `van-site.zip` into a folder (or just use the `site/` folder).
2. Upload that folder to a static web host. Any of these works, drag and drop:
   - **Netlify Drop**: go to app.netlify.com/drop and drag the folder onto the page. You get a link at once.
   - **Cloudflare Pages**: Workers and Pages, Create, Pages, Upload assets, drop the folder.
   - **Any web host** (your own domain): upload the contents of the folder (not the folder itself) with the host's file manager or FTP.
3. Open the link. The home page is `index.html`, with a card for every page, and the bar across the top moves between them.

## Good to know

- Every page asks search engines not to list it (a `noindex` tag), but there is **no password**: anyone who has the link can open it.
  If you want a password, use the host's password setting (Netlify and Cloudflare both have one).
- The 3D pages load the three.js library from cdnjs.cloudflare.com, so the person looking needs an internet connection.
- The notes on the electrical page quote your own messages (for example "user (2026-11-05): ..."). Tell me if you want those taken out first.
- The photos in `site/photos/` have the GPS location, camera and date removed. **Never publish the rest of this repository**: the top-level
  `photos/` folder still has the GPS data. If you use GitHub Pages, put only the contents of `site/` in a separate new repository.

## Updating it later

Ask for the change, then upload the new `van-site.zip` (or folder) to the same host. On Netlify Drop, drag the new folder onto the site's Deploys page.
