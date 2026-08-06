# Recon + Analysis Automation

An automated recon script built for bug bounty hunting - it chains together
URL collection, fingerprinting, JS secret scanning, parameter discovery, and
directory bruteforcing into a single pipeline, so you can point it at a
target and go do something else while it runs.

Every stage prints live status to the terminal and finishes with a summary
table showing what ran, how many results each tool found, and how long it
took.

---

## Pipeline stages

Running `main.py` walks through the following, in order:

1. **URL Collection** — `gau`, `katana`, and `gospider` run in parallel to
   pull every URL they can find for the target. Results are merged,
   deduplicated (`uro`), and checked for liveness (`httpx`). Live,
   non-static-asset endpoints are then screenshotted with `gowitness`.
2. **Fingerprinting** — `whatweb`, `httpx`, `nmap`, `wafw00f`, `wappalyzer`,
   and `curl` run in parallel against the target to identify tech stack,
   open ports/services, WAF presence, and raw response headers.
3. **JavaScript Analysis** — `.js` files are filtered out of the collected
   URLs and scanned with `mantra` and `jsecret` for exposed API keys and
   leaked credentials.
4. **Parameter Discovery** — `arjun` actively probes for hidden parameters
   while a `grep` pass pulls out URLs that already contain query strings,
   both saved to `param.txt` for later fuzzing/IDOR testing.
5. **Directory Bruteforce** — `feroxbuster` and `dirsearch` run in parallel
   to find hidden paths not surfaced by the earlier crawling stages.

---

## Tools used

| Tool | Purpose |
|---|---|
| [gau](https://github.com/lc/gau) | Pulls URLs from Wayback/CommonCrawl/OTX/urlscan |
| [katana](https://github.com/projectdiscovery/katana) | Live web crawler |
| [gospider](https://github.com/jaeles-project/gospider) | Fast web spider |
| [uro](https://github.com/s0md3v/uro) | Removes structurally duplicate URLs |
| [httpx](https://github.com/projectdiscovery/httpx) | Liveness checks + tech fingerprinting |
| [dirsearch](https://github.com/maurosoria/dirsearch) | Directory/content bruteforce |
| [feroxbuster](https://github.com/epi052/feroxbuster) | Directory/content bruteforce |
| [whatweb](https://github.com/urbanadventurer/WhatWeb) | Tech stack fingerprinting |
| [nmap](https://nmap.org/) | Port/service/version scanning |
| [wafw00f](https://github.com/EnableSecurity/wafw00f) | WAF detection |
| [Wappalyzer CLI](https://github.com/wappalyzer/wappalyzer) | Tech stack fingerprinting |
| [mantra](https://github.com/MrEmpy/mantra) | Secret scanning in JS files |
| [jsecret](https://github.com/m4ll0k/SecretFinder) | Secret scanning in JS files |
| [arjun](https://github.com/s0md3v/Arjun) | Hidden parameter discovery |
| [gowitness](https://github.com/sensepost/gowitness) | Screenshotting live web pages |

Each of these is a separate CLI tool and needs to be installed on your
system independently — `pip`/`requirements.txt` only covers the Python side
(`rich`, for the terminal UI). See each tool's repo for install instructions
(most are `go install ...` or available via `apt`/`pip`).

`gowitness` additionally needs a Chrome-based browser installed
(Chrome, Chromium, or Brave) — Firefox is not supported since gowitness
uses the Chrome DevTools Protocol.

---

## Setup

```bash
git clone https://github.com/og-h7n/Recon.git
cd Recon/Analysis

pip install -r requirements.txt --break-system-packages
```

Then install the external CLI tools listed above. Most Go-based tools can
be installed like this (requires Go):

```bash
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/jaeles-project/gospider@latest
go install github.com/sensepost/gowitness@latest
# ... etc, check each tool's repo for the current install command
```

`nmap`, `whatweb`, and `wafw00f` are usually available via your distro's
package manager:

```bash
sudo apt install nmap whatweb wafw00f -y
```

---

## Usage

```bash
python3 main.py target.com
```

This will create two subfolders in your working directory as it runs:

- `Urls_collected/` — all URL-collection output (`_gau_.txt`, `_katana_.txt`,
  `_gospider_.txt`, `_LiveUrls_.txt`, screenshot targets)
- `Fingerprint/` — all fingerprinting tool output (`httpx.txt`, `nmap.txt`,
  `whatweb.txt`, `firewall.txt`, `wappalyzer.txt`, `headers.txt`)

JS secrets, discovered parameters, and directory bruteforce results are
saved in the working directory as `js_files.txt`, `param.txt`,
`ferox_results.txt`, and `Dirseach_results.txt`.

---

## ⚠️ Authorized use only

This tool is intended for use against targets you own or have explicit
written authorization to test (e.g. an active bug bounty program's
in-scope assets). Running these tools against systems without permission
may be illegal in your jurisdiction. Always check program scope before
scanning.

---

## Contributing / feedback

Suggestions are welcome — open an issue or a PR.

Discord: https://discord.gg/d9wFhhnwFe

Miro board: https://miro.com/app/board/uXjVHAlbwYw=/?share_link_id=227022886951

Created by [@h7n](https://github.com/og-h7n)
