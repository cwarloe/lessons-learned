# Lesson: GitHub Pages custom-domain HTTPS stuck

**Date:** 2026-09-20  
**Project:** Mr. Life Manager (`cwarloe/mr-life-manager`, domain `mrlifemanager.com`)  
**Context:** Cut over from Cloudflare Pages placeholder to GitHub Pages with grey-cloud DNS.

## What happened

DNS was correct for days (apex A/AAAA → GitHub Pages IPs; `www` CNAME → `cwarloe.github.io`; DNS-only / not proxied). HTTP served the real site (`Server: GitHub.com`). HTTPS stayed broken: browsers got `CN=*.github.io`, and the Pages API refused Enforce HTTPS with **"The certificate does not exist yet."** Waiting alone did nothing useful.

## Root cause

GitHub’s Let’s Encrypt issuance for custom domains can stall with almost no UI. Correct DNS + working HTTP does **not** guarantee the cert job is progressing. A leftover Cloudflare Pages binding can also keep answering the hostname — we had already removed that; the remaining failure was GitHub’s stuck cert state.

## What fixed it

1. Confirmed DNS still pointed at GitHub and stayed grey-cloud.
2. **Cleared then re-added** the custom domain on the repo Pages config (`cname` → `null`, then `cname` → `mrlifemanager.com`).
3. API message flipped to **"The certificate has not finished being issued"** (issuance actually running).
4. Within minutes: cert SAN included apex + www; set **`https_enforced: true`**.

## Lesson / avoid next time

- After custom-domain DNS is correct and HTTP is GitHub, **do not wait days** on “certificate does not exist yet.” If it’s still that after ~1 hour, **clear and re-add the custom domain once** to kick issuance.
- Keep GitHub Pages hostnames **DNS-only** until HTTPS is enforced; don’t orange-cloud the apex for Pages.
- Delete/unbind any Cloudflare Pages/Workers custom domain on the same hostname before or during cutover.
- Optional: a short watch that tries Enforce HTTPS and, on repeated “does not exist yet,” performs one clear/re-add kick.

## Done when

`https_enforced: true` and `https://<domain>/` serves the site with a cert whose SAN includes that domain (and www if used).