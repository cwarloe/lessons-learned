# Build it in stages, and publish a demo at each stage

**Standing preference (author, 2026-11-19):** whenever a project can be built in stages or layers, prototype it that way and publish a phone-friendly demo as soon as there is something to show. Do this by default, without being asked.

Why: a demo you can open on your phone turns "describe it" into "try it". It surfaces decisions early (a look, a camera angle, a cost), and it makes change cheap, which is the point of building in layers.

## The recipe (worked on the 5BX sprite-boy video)

1. **Build in layers that are real files**, not workspace state. Backdrop, character, props, text, audio: each its own file, combined by a script, each one swappable. Keep config (look, wording, character, exercises) in small JSON files, not in code.
2. **Write a builder for the demo itself** (`make_demo.py`) that reads the project's own assets and config. The demo is then regenerated, never hand-assembled, so it cannot drift.
3. **Put four things in the demo:** a short reel (under about 2 MB, under a minute), an interactive viewer where the author can switch layers, add things and recolor, a plain table of what each kind of change costs, and an honest "what's next / what isn't built / what hasn't been checked".
4. **Test it in a real browser at phone width** before saying it works: no console errors, no failed loads, no sideways scroll, the key interaction actually changes pixels (recolor: count pixels before and after), the media loads, and any copy button puts the right text on the clipboard.
5. **Publish two ways.**
   - A private claude.ai artifact link for an immediate look on the phone. Say who can open it.
   - GitHub Pages from a separate `gh-pages` branch holding **only** the demo files (see below), so nothing else in the repo gets published with it. Ask first if the branch rules limit pushes, and say that a public repo means a public demo.
6. **Say what was and was not tested.** "I have not tried a real phone or Safari" is a fine thing to write.
7. **Publish the recipe, not just the result.** Prompts, settings, what failed and the fix, so the work can be redone with other tools (see `AI_SPRITE_VIDEO_LESSONS.md`).

## `gh-pages` with only the demo (a fresh branch, no history from the project)

```bash
git worktree add --detach /tmp/ghp HEAD && cd /tmp/ghp
git checkout --orphan gh-pages && git rm -rq --cached . && find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -r path/to/demo/. . && touch .nojekyll
git add -A && git commit -m "Publish the demo" && git push -u origin gh-pages
git worktree remove --force /tmp/ghp
```

- In the 5BX case (a public repo) the site went live about a minute after the push, with no settings change. That may differ for other repos or private ones. If it does not appear, the setting is Settings → Pages → deploy from a branch → `gh-pages` / root.
- The URL is `https://<owner>.github.io/<repo>/`.
- Confirm with `curl -I` on the page and its media, then load it in a browser. A "failed request" for a video that was cut off by navigating away is the browser cancelling the download, not a failure.

## Gotchas hit on the way

- Chaining `VAR=... && cd ... && server &` runs the **whole chain** in the background, so the variable is unset in the foreground. Set variables on their own line, and start servers with the tool's background option.
- `pkill -f` and `ps | grep | kill` can match your own shell. Find the process by exact command-line match in `/proc` and kill that.
- A status tool that echoes every prompt makes huge output when polled for many jobs at once. Poll fewer, or save the output to a file and parse it.
- A relative link from one artifact page to another page in the same artifact is untested. Pages is the reliable home for multi-page demos.
- Repo notes that name the author should be neutral ("author decision") when the text is meant to be pasted into other tools or published.

## Suggested line for your saved preferences

If you want this automatic in every conversation, add this to your Claude preferences (I cannot change them from a session):

> When a project can be built in stages or layers, prototype it that way and publish a phone-friendly demo at each stage (private link first, GitHub Pages `gh-pages` branch on request). Keep the layers as separate files and publish the prompts and settings, so changes are quick and the work is portable.
