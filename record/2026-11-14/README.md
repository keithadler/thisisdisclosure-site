# The record, November 14, 2026

This folder is a dated public record of what I, Keith Adler, say in the film *This Is Disclosure*, released free at [thisisdisclosure.com](https://thisisdisclosure.com) on November 9, 2026.

| File | What it is |
|---|---|
| `CLAIMS.md` | My central claims, each quoted word for word from the film with the time it is spoken. |
| `narration.en.srt` | The complete narration of the film, timed to the second. |
| `narration.en.txt` | The same narration as plain text. |
| `predictions/` | My dated predictions, as published on the predictions page. |
| `SHA256SUMS` | SHA-256 fingerprints of every file here, of the film itself, and of the live site text. |
| `SHA256SUMS.ots` | An OpenTimestamps proof that `SHA256SUMS` existed on this date, anchored in the Bitcoin blockchain. |

## How anyone can check it

1. **The words are mine and unchanged.** Run `shasum -a 256 -c` on the folder files listed in `SHA256SUMS`. Download the film from the URL in `SHA256SUMS` and hash it; it must match `cb6509f7843a01093f262272f0d933d3ac16658fda472e7f5cd39ebc66557954`. The narration in this folder is the narration in that film.
2. **The date is real.** Each file here was committed through GitHub's own interface, so GitHub signed the commit and recorded the time on its servers. The commit shows as Verified, and its date is not one I can set.
3. **The date does not depend on GitHub.** `SHA256SUMS.ots` ties the fingerprints to a Bitcoin block. Check it with the OpenTimestamps client (`ots verify SHA256SUMS.ots`) or at [opentimestamps.org](https://opentimestamps.org).
4. **A third copy exists.** This record is saved in the Internet Archive's Wayback Machine.

Nothing here can be edited without changing a fingerprint, and the fingerprints are fixed in time three independent ways.
