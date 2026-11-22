# The record, November 21, 2026

This folder is a dated public record of what I, Keith Adler, say in the film *This Is Disclosure*, in the cut released free at [thisisdisclosure.com](https://thisisdisclosure.com) on November 21, 2026 (2 hours 13 minutes 33 seconds). The record of the first cut is in `../2026-11-14/`.

| File | What it is |
|---|---|
| `CLAIMS.md` | My central claims, each quoted word for word from the film with the time it is spoken. |
| `narration.en.srt` | The complete narration of the film, timed to the second. |
| `narration.en.txt` | The same narration as plain text. |
| `predictions/` | My dated predictions, as published on the predictions page. |
| `SHA256SUMS` | SHA-256 fingerprints of every file here, of the film itself, and of the live site text. |
| `SHA256SUMS.ots` | An OpenTimestamps proof that `SHA256SUMS` existed by Bitcoin block 976,971 (mined 2026-11-22 01:14:15 UTC, hash 000000000000000000019cbc2251caffc2b5162c8e5326f9125b4405d6486715). |

## How anyone can check it

1. **The words are mine and unchanged.** Run `shasum -a 256 -c` on the folder files listed in `SHA256SUMS`. Download the film from the URL in `SHA256SUMS` and hash it; it must match `b0afaa47909480f6a4fefc4ffb5708f54b94b472e91108e2721d85f467c71525`. The narration in this folder is the narration in that film.
2. **GitHub recorded it.** Each file here was sent through GitHub's API, and GitHub logged the push on its own servers (its public events feed for this repository shows the time). A commit date alone can be set by anyone, which is why steps 3 and 4 exist.
3. **The date does not depend on GitHub.** `SHA256SUMS.ots` ties the fingerprints to a Bitcoin block. Check it with the OpenTimestamps client (`ots verify SHA256SUMS.ots`) or at [opentimestamps.org](https://opentimestamps.org).
4. **A third copy exists.** This record is saved in the Internet Archive's Wayback Machine.

Nothing here can be edited without changing a fingerprint, and the fingerprints are fixed in time three independent ways.
