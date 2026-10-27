# N8 E-SEAL: sealed forecasts for Validation Track A

**Status (2026-10-27): built and dry-run tested; not yet sealed.** The seal waits for a public key from a custodian (below). It also refuses to run if the plan has changed since it was committed. Nothing in this folder holds forecast content. The only model replies so far came from the dry run on a non-conservation problem, and they were discarded unread.

Plan and pre-stated scoring: `docs/plans/n8-e-seal.md`. Rules: `REORIENTATION.md` §18.1 (E-SEAL), §20 item 5, §22 (N8). Secondary and non-gating: nothing here can change what K0, K1, K2, Stage B arm matching or the 2–3-week delay decides (`research/experiment-ai-assisted-cta-physics.md`).

## What is sealed, and what is not

- **The operation-list half.** For each of the four Stage A think-aloud problems, at most 12 mental operations per arm, forecast closed-book from the problem statement and the unit definition only. Arms: `anthropic/claude-opus-5.5` (top-tier, primary), `openai/gpt-6.1-sol` (other family), and `anthropic/claude-haiku-4.5` (cheap). Evidence label: synthetic extrapolation. It is a predictor, never a criterion.
- **The early-K0 half is not built.** §18.1 allows it only after the early-K0 items are frozen in their registration. `instrument/k0/items.md` and `instrument/k0/prereg-early-k0.md` are still drafts.

## How

- `reconstruct/src/reconstruct/eseal.py` keeps replies in memory and encrypts them in one piece. Plaintext reaches openssl only on stdin. The data is AES-256-CBC with PBKDF2 at 600,000 iterations of SHA-256, under a fresh 256-bit random passphrase. That passphrase is wrapped with RSA-OAEP-SHA256 under the custodian's public key of at least 3072 bits.
- The run prints only hashes, cost and per-call outcomes. Model-call errors are recorded by exception class only, and refusals print fixed messages that carry no content.
- A canary test (`reconstruct/tests/test_eseal.py`) shows that a fake model's content reaches no output, log or file, in five encodings, and that it is recovered on decryption.
- The seal refuses to start in any of these cases: no public key; a key under 3072 bits; `OPENAI_LOG` set; OpenRouter logging not confirmed off; key or account headroom under $10 (measured by `scripts/key_headroom.py`); the plan not committed; no passing dry run made with the same prompt and schema; or a seal already in place.
- **Unsealing** needs the custodian's private key and a committed K1 lock file carrying `k1_decision`. It writes the plaintext only outside the repo, and appends a record to `research/n8_eseal/unseal_record.json`.

## Hashes (SHA-256)

| Object | Hash |
|---|---|
| `instrument/problems/problems.json` (the problems to be forecast) | `9021e28e3f8225e1b88c60ea292b3a13f57f52b00fa90f6c403df47d753462ba` |
| System prompt `reconstruct/src/reconstruct/prompts/eseal_system.md` | `5882b04a7a3ce1c3b3c5b5b49ab168873b2d65323f9ea9180ced9f416e83c6c0` |
| User template `eseal_user.md` | `17a25ae358b94c7a9e060b2bd508914569e97eaa1d612e171ce97ea9b8637e91` |
| Output schema | `77865fed3a613c0bde8d042aa2474e882d76e6d5fcf10dcd29a47f33112e895a` |
| Dry-run manifest `dry_run/manifest.json` | `5db3cb68abcbca74bb012f22b0fa45a11bb888cd959f1ad3c81b78accba9751a` |
| `forecast.enc`, `key.enc`, plaintext, public key | written to `sealed/manifest.json` at sealing |

## Cost

| Run | Cap | Spent |
|---|---|---|
| Dry run, 2026-10-27, 3 calls (Opus $0.0215, Sol $0.0061, Haiku $0.0037) | $0.25 | **$0.0313** |
| Seal, 12 calls | $0.75 | not run; about $0.13 expected from the dry run's token counts |

Ledgers: `dry_run/calls.jsonl` and, later, `sealed/calls.jsonl`. These store prompt hashes only.

## To seal (owner and custodian)

1. A custodian who holds no Track A role, and will take none, generates the key pair: `openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out e_seal.pem`, then `openssl pkey -in e_seal.pem -pubout -out e_seal.pub`. They keep `e_seal.pem` offline with a second copy, and give the operator only `e_seal.pub`. Record the custodian's name and role here, with the output of `shasum -a 256 e_seal.pub`.
2. Turn off input/output logging on the OpenRouter account.
3. Run `export E_SEAL_PUBLIC_KEY=/path/to/e_seal.pub`, then `uv run --directory reconstruct python -m reconstruct.eseal seal --live --max-usd 0.75 --provider-logging-off`. Then commit `sealed/`.
4. Name the plan's SHA-256 (in `sealed/manifest.json`) in Track A's pre-registration before M4.

Do not open the OpenRouter activity entries for the seal's calls. Anyone who sees the forecast becomes ineligible for every Track A human role (§18.1).
