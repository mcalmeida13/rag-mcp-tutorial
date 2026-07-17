# CLAUDE.md — Project Conventions for rag-mcp-tutorial

This file is read automatically by Claude Code whenever it works in this repository. It defines a standing instruction: **at the end of each completed step of this tutorial, open a branch + PR for review, and only after I've reviewed and merged it on GitHub, create a semver tag and push it** — without needing to be asked again each time.

The flow has **two separate triggers** now instead of one: "prepare the PR" and "finalize the tag." Do not collapse them into a single automatic action — the whole point is that I get to review the PR on GitHub before anything gets tagged.

## Trigger 1 — Prepare the PR

Fire this **only** when both of these are true:

1. I have just finished one of the tutorial steps (ingestion, packaging, retrieval/generation, MCP server, documentation, or any other discrete step we agree on going forward), **and**
2. I have confirmed the step works (e.g. I ran the relevant demo/script/CLI command and it behaved as expected, or I explicitly said something like "looks good" / "this step is done").

Do **not** branch, commit, or open a PR mid-step, on partial/broken code, or just because files changed. If it's unclear whether a step is actually finished and verified, ask me first instead of assuming.

### What to do when Trigger 1 fires

1. Run `git status` and `git diff` to review exactly what changed.
2. Make sure you're branching off the latest `main` (or whatever the default branch is) — pull first if needed.
3. Create a new branch named after the step, e.g. `step/a-ingestion`, `step/a2-packaging`, `step/b-retrieval-generation`, `step/c-mcp-server`, `step/d-documentation`.
4. Stage only the files relevant to the completed step (avoid `git add -A`/`git add .` if there are stray or unrelated files — add them by name).
5. Write a commit message using [Conventional Commits](https://www.conventionalcommits.org/) style, summarizing what the step added, e.g.:
   - `feat(ingestion): add chunking, embeddings, and local vector index`
   - `feat(packaging): expose CLI via pipx with ingest/ask/serve-mcp subcommands`
   - `feat(retrieval): add cosine-similarity retrieval and RAG generation demo`
   - `feat(mcp): add MCP server exposing search_documents tool`
   - `docs: add architecture diagram, glossary, and example query trace`
6. Push the branch to `origin`.
7. Open a pull request into the default branch with `gh pr create`, using the commit message (or a short expansion of it) as the PR title/description. Include a short "What to review" checklist in the PR description relevant to that step (e.g. for ingestion: chunk size choice, embedding model, index format).
8. **Stop here.** Give me the PR URL and tell me explicitly that you're waiting for me to review and merge it on GitHub before anything gets tagged. Do not merge the PR yourself and do not create a tag at this point, even if the code looks correct to you.

## Trigger 2 — Finalize the tag (after I've reviewed and merged)

Fire this **only** when I tell you the PR has been reviewed and merged (e.g. "mergeei o PR" / "pode taguear" / "PR aprovado, segue"), or when you check and confirm the PR is actually merged.

### What to do when Trigger 2 fires

1. Verify the PR is actually merged before doing anything: `gh pr view <number-or-branch> --json state,mergedAt` (or equivalent). If it's not merged yet, tell me and stop — don't tag an unmerged branch.
2. Switch to the default branch locally and pull the merge commit: `git checkout main && git pull origin main`.
3. Determine the next tag using **semantic versioning**, incrementing the **minor** version once per completed step, starting at `v0.1.0`:
   - Run `git tag --list "v0.*"` (or `git tag --sort=-v:refname`) to find the current highest tag.
   - If no tags exist yet, this is `v0.1.0`.
   - Otherwise, bump the minor version by one (e.g. `v0.1.0` → `v0.2.0` → `v0.3.0` → `v0.4.0`), keeping the patch at `.0` for step-level tags.
   - Only bump patch (e.g. `v0.2.1`) if I explicitly ask you to tag a fix/adjustment within an already-tagged step, rather than a new step.
   - When every step originally planned (ingestion → packaging → retrieval/generation → MCP server → documentation) is committed and tagged, ask me whether the next tag should be `v1.0.0` instead of continuing the `v0.x` sequence, since that marks the tutorial as "complete."
4. Create an **annotated tag** (not a lightweight one), pointing at the merge commit on the default branch, with a short message describing the step:
   ```
   git tag -a v0.2.0 -m "Retrieval and generation: cosine-similarity search + RAG demo"
   ```
5. Push the tag to `origin`:
   ```
   git push origin <tag>
   ```
6. Delete the now-merged local and remote step branch if it's no longer needed (`git branch -d <branch>`, `git push origin --delete <branch>`) — ask me first if you're unsure whether I still want it around.
7. Confirm to me what tag was created and pushed, and show a link/reference I can use to find it on GitHub.

## Hard constraints (never violate these)

- Never merge a PR yourself unless I explicitly ask you to (e.g. "pode mesclar você mesmo") — by default, merging on GitHub is my call, not yours.
- Never force-push (`--force`, `--force-with-lease`), rewrite history, or delete/move existing tags without me explicitly asking.
- Never use `--no-verify` or `--no-gpg-sign`.
- Never commit files that look like secrets (`.env`, API keys, credentials) — if something like that is staged, stop and warn me instead of committing it.
- Never create a tag on top of an unmerged or uncommitted state — the tag must point at the actual merge commit on the default branch for that specific completed step.
- If `gh auth status` or the git remote isn't configured correctly, stop and tell me what's wrong rather than trying to work around it.

## Notes specific to this project

- The vector index files generated by `rag/ingest.py` and any `.env` files should already be excluded via `.gitignore` (set up in the GitHub-repo creation step) — double check they're not accidentally staged before committing.
- Steps map roughly to the tutorial prompts: ingestion (Prompt A), packaging (Prompt A2), retrieval/generation (Prompt B), MCP server (Prompt C), documentation (Prompt D). If we add more steps later (e.g. new exercises), treat each as its own step for branching/PR/tagging purposes unless I say otherwise.
- If I ask you to do an automated self-review of the diff before or alongside opening the PR (rather than relying only on my manual review), that's a separate, explicit request — don't do it by default as part of Trigger 1.
