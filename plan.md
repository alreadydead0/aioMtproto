# aioMtproto Performance Plan — v2 (Reality-Checked)

This replaces `aioMtproto-full-plan-final.md`. It's based on actually reading your
repo (`aioMtproto-main.zip`), not just theory. Follow it top to bottom, one
checkbox at a time — each phase is independently mergeable and benchmarkable.

---

## 0. What the original plan got right vs already-done vs overclaimed

**Already implemented in your repo (skip these, don't re-do them):**
- `Phase 0.1` (auth export/import per media session) — **already correct** in
  `dc_manager.py` (`ExportAuthorization` on main DC → `ImportAuthorization` on
  media DC). This is the "#1 trap" the plan warns about; you already avoided it.
- `Phase 0.2` (per-session msg_id/time offset) — **already correct**. Every
  `RPCEngine` owns its own `IdGenerator` instance (`protocol/ids.py`), so this
  is naturally per-session once you add more sessions.
- Partial-failure-tolerant init pattern — your `get_dc_client()` already has
  proper try/except/cleanup/state-machine hygiene. Extending it to N sessions
  per DC is a mechanical change, not new design.

**Real, confirmed bottleneck (highest leverage — do this first):**
- `crypto/aes_ige.py` does IGE in a **pure-Python loop calling a C AES-ECB
  primitive once per 16-byte block**. For a 512 KB chunk that's ~32,768
  Python-level function calls + generator-based XORs. The AES itself is
  C-backed, but the *loop and glue* is what's slow — that's exactly why
  `tgcrypto`/`cryptg` (single C call for the whole buffer, IGE implemented in
  C) wins by a large margin. This part of the plan is legitimate.

**Real, confirmed bug (do this early, it's cheap):**
- `media/downloader.py` uses blocking `open()` / `.seek()` / `.write()` inside
  the async download path, even though `aiofiles` is already a dependency in
  `pyproject.toml` and unused here. Every chunk write briefly stalls your
  event loop (and therefore the RPC reader task) while it's happening. Fix
  this before you touch anything else — it's mechanical and safe.

**Real gap the plan correctly flags:**
- There is **no real connection pool**. `DCManager._sessions` is `dict[dc_id]
  -> ONE session`. Your "parallel chunk workers" in `downloader.py` are all
  multiplexed over that single TCP socket via `asyncio.gather` + a semaphore.
  This *works* (MTProto is designed for in-flight multiplexing via msg_id),
  but it means you're capped by one socket's TCP window instead of N. Adding
  a real per-DC pool (2-4 sessions) is worth doing — see Phase 3 below.

**Missing from the original plan (found by checking how Pyrogram actually
does it, not by memory):**
- Pyrogram/pyrotgfork run crypto for large payloads **in a thread pool
  executor**, not inline in the event loop — even with `tgcrypto`. A single
  C call over a big buffer is fast, but it's still synchronous and blocks the
  loop for its duration; for big files under load this matters. Your plan
  doesn't mention this. Add it (Phase 1.2 below).

**Overclaimed part of the original plan — the "50-200x" total, "20-40+ MB/s"
target:**
- Each phase's multiplier (20-50x crypto × 4-8x pool × 4-8x media rewrite ×
  2-3x disk I/O × 1.5x TCP tuning) was **multiplied together as if
  independent**. They aren't — they all compete for the same wall-clock
  budget and the same network ceiling. Real throughput is capped by (a) your
  VPS's actual bandwidth to that Telegram DC, and (b) Telegram's own
  per-connection/per-authkey throttling, neither of which any of these
  changes touch. Don't plan against the "20-40 MB/s" number — **measure your
  own baseline and re-measure after each phase** (harness in section 5). If
  your VPS caps out at 10 MB/s on the wire, no amount of IGE optimization
  gets you to 40.

---

## 1. Will this be faster or slower than pyrotgfork, honestly?

**Ceiling:** roughly comparable, potentially faster for parallel same-DC
media, *if* Phases 1-3 below are implemented correctly and validated. Reason:
pyrotgfork/pyrogram normally run **one** media session per DC (occasionally
more for CDN redirects); a correctly built 2-4 session pool per DC gives you
more concurrent in-flight requests than stock Pyrogram does out of the box.

**Real risk of being slower than pyrotgfork, not faster:**
- If you add `tgcrypto`/`cryptg` but **don't** thread-pool it for large
  chunks (see 1.2), you can end up *worse* than Pyrogram under concurrent
  load, since Pyrogram already avoids blocking its loop this way.
- Telegram caps concurrent connections per DC per auth key (commonly cited
  informally around 4-8, undocumented officially). Going past that gets you
  disconnects or `FLOOD_WAIT`, not more speed. `pool_size=4` (as in the
  original plan) is a sane, conservative default — don't be tempted to push
  it to 16 "for more speed."
- Hand-rolled MTProto (msg_id sequencing, salt rotation, bad_msg handling,
  CDN redirects, file-reference refresh) has had years of edge-case
  hardening in Pyrogram/Telethon. Bugs here cost you far more than any crypto
  win — correctness first, speed second.

**Bottom line:** don't trust either plan's numbers. Build the benchmark
harness in section 5 *first*, get your real baseline, then apply phases in
order and re-measure. That number is the only one that matters for your repo.

---

## 2. Phase order (revised priority — do in this sequence)

### Phase 1 — Crypto backend swap (do first, highest leverage, lowest risk)
- [ ] Add `tgcrypto` (recommended: proven at Pyrogram's scale) as a dependency.
      Since you'd earlier settled on `cryptg` — either is fine, both wrap a C
      IGE implementation; don't block on re-deciding this, pick one and move.
- [ ] Rewrite `aes_ige_encrypt`/`aes_ige_decrypt` to call the native
      whole-buffer IGE function directly (no Python per-block loop). Keep
      your existing `cryptography`-per-block path and `PureAES` as fallback
      tiers, exactly like your current multi-backend detection pattern
      already does — just add the fast tier above them.
- [ ] **1.2 (not in original plan): thread-pool offload.** Wrap
      `aes_ige_encrypt`/`decrypt` calls for payloads above ~64 KB in
      `loop.run_in_executor(None, ...)`. Keep small payloads (handshake,
      small RPCs) inline — executor dispatch overhead isn't worth it there.
- [ ] Benchmark against your OLD implementation on your own machine (section 5.1)
      before touching anything else. Confirm the win is real before proceeding.

### Phase 2 — Fix blocking disk I/O (cheap, do alongside Phase 1)
- [ ] Replace `open()`/`.write()`/`.seek()` in `media/downloader.py` and
      `media/uploader.py` with `aiofiles.open()` + `await f.seek()` / `await
      f.write()`. It's already a dependency — this is a small diff.
- [ ] Keep the existing offset-based chunk writing logic as-is; only swap the
      I/O calls to their async equivalents.

### Phase 3 — Real per-DC session pool (do after 1 & 2 are validated)
- [ ] Build `DCSessionPool` wrapping what `dc_manager.py` already does for a
      single media session — reuse its exact auth export/import and
      handshake logic per pool member, don't rewrite it.
- [ ] `pool_size` default 4, configurable, hard warn (don't silently allow) if
      someone sets it above ~8.
- [ ] `asyncio.gather(..., return_exceptions=True)` for pool init, same
      partial-failure pattern you already use in `get_dc_client()`.
- [ ] **Enforce one-session-per-worker ownership explicitly** — this is the
      one part of the original plan that's a correctness issue, not just a
      speed one. Sharing one pooled session across concurrent workers will
      corrupt the TCP stream. Assign sessions to workers by index, not by a
      shared round-robin call mid-flight.
- [ ] Update `DCManager.get_media_client()` to return from the pool instead
      of the single cached session.

### Phase 4 — Rate limiting + CDN redirect handling (do before going wide)
- [ ] Add a simple token-bucket limiter shared across all pooled sessions for
      the same DC. Without it, 4 parallel sessions hitting Telegram
      simultaneously is a fast way to get `FLOOD_WAIT`.
- [ ] Confirm your CDN-redirect and `FILE_REFERENCE_EXPIRED`/`FILE_MIGRATE_X`
      handling (you already have some of this per `errors/mtproto.py`) works
      correctly per-pooled-session, not just for a single session.

### Phase 5 — TCP/uvloop tuning (last, smallest gain, do once the above is stable)
- [ ] `TCP_NODELAY` + bigger `SO_SNDBUF`/`SO_RCVBUF` on the socket.
- [ ] Confirm `uvloop.install()` runs before any asyncio setup (dependency's
      already there — check it's actually wired in at startup).

### Phase 6 — Persistent pool session state (optional, do last)
- [ ] Only worth it once 1-5 are stable and you're tired of re-handshaking 4
      sessions per DC on every restart. Not a speed win, a restart-latency
      and Telegram-login-attempt-count win.

---

## 3. What to explicitly NOT do

- Don't implement Phase 0.1/0.2 from the original plan — already done, and
  re-doing it risks breaking a working auth flow for no gain.
- Don't chase `pool_size` above ~8 "for more parallelism" — you'll hit
  Telegram-side limits before you hit any real speed ceiling.
- Don't trust the "20-40 MB/s" / "50-200x" numbers as a target. Trust your
  own measured baseline instead.
- Don't skip Phase 1.2 (thread-pool offload) — it's the one thing missing
  from the original plan that Pyrogram does for a real reason.

---

## 4. Per-phase acceptance criteria (so "dheere dheere" stays safe)

For every phase above, before merging:
1. Existing `tests/test_mtproto/*` still pass.
2. Run `run_full_check.py` (already in your repo) clean.
3. Re-run the benchmark harness below and record the number in the PR/commit
   message — old vs new, same file, same DC, same network.
4. Don't start the next phase until the current one's benchmark shows a real,
   reproducible improvement (not a one-off lucky run — run it 3x).

---

## 5. Benchmark harness (build this before Phase 1, not after)

### 5.1 Crypto-only benchmark
```python
import time, os
from aiogram.mtproto.crypto.aes_ige import aes_ige_encrypt

key, iv = os.urandom(32), os.urandom(32)
data = os.urandom(10 * 1024 * 1024)

start = time.perf_counter()
for _ in range(10):
    aes_ige_encrypt(data, key, iv)
elapsed = time.perf_counter() - start
print(f"Throughput: {100 / elapsed:.1f} MB/s")
```
Run this BEFORE and AFTER Phase 1. That ratio is your real crypto speedup —
compare it to what you expected before moving on.

### 5.2 End-to-end download benchmark
```python
import time

start = time.perf_counter()
await bot.download_file_mtproto(
    location=file_location,
    file_size=100 * 1024 * 1024,
    destination="/dev/null",
    workers=4,
)
elapsed = time.perf_counter() - start
print(f"Download: {100 / elapsed:.1f} MB/s")
```
Run this after EVERY phase (1 through 5), same file, same time of day if
possible (Telegram DC load varies). Keep a running log — this log is your
actual comparison data against pyrotgfork, not the plan's paper numbers.

### 5.3 Comparison run
Once Phase 1-3 are done, run the *same* 5.2 benchmark against a pyrotgfork
client downloading the same file from the same DC, same VPS, same time. That
head-to-head number is the only honest answer to "faster or slower than
pyrotgfork" — everything above this is informed prediction, not proof.

---

## 6. Quick-start checklist (copy this into your issue tracker)

- [ ] Phase 1: swap crypto backend + thread-pool offload for large buffers
- [ ] Phase 1: benchmark 5.1, record before/after
- [ ] Phase 2: fix blocking disk I/O in downloader.py / uploader.py
- [ ] Phase 3: build real DCSessionPool (size=4), reuse existing auth logic
- [ ] Phase 3: benchmark 5.2, record before/after
- [ ] Phase 4: token-bucket rate limiter + verify CDN/file-ref handling under pool
- [ ] Phase 5: TCP tuning + confirm uvloop wired at startup
- [ ] Phase 5: benchmark 5.2 again
- [ ] Section 5.3: head-to-head vs pyrotgfork on same file/DC/VPS
- [ ] Phase 6 (optional): persistent pool session storage
