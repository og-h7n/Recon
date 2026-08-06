<div align="center">

# 🕸️ RECON-Analysis

### *the whole attack surface, mapped out, automated where it counts*

`recon` → `analysis` → `results`

</div>

---

## what even is this 👀

this repo is split into two phases because that's just how recon actually
works — first you go **wide** (find everything that exists), then you go
**deep** (figure out what's actually worth attacking).

```
┌───────────────┐        ┌──────────────────┐
│    /recon       │  ──▶   │    /Analysis        │
│  find the        │        │  automate the      │
│  attack surface   │        │  boring parts       │
└───────────────┘        └──────────────────┘
```

- **[`/recon`](./recon)** — the methodology. how to actually enumerate a
  target's full scope (subdomains, root domains, out-of-scope filtering,
  passive + active discovery) before you touch a single tool from the
  automation side.
- **[`/Analysis`](./Analysis)** — the automation. once you've got your
  scope, this is the script that chains url collection, fingerprinting,
  js secret hunting, param discovery, and dir bruteforce into one run.

tl;dr: `/recon` tells you **what** to scan, `/Analysis` tells your
computer **how** to scan it (without you babysitting 10 terminal tabs).

---

## 🗺️ the recon methodology (`/recon`)

the whole point of scoping properly before scanning is finding **maximum
attack surface** without wasting time on things that aren't in scope or
aren't worth it. the flow looks like:

```
                          RECON
                            │
                        Scopes
                    ┌───────┼────────┐
              In scope            Out of scope
                    │
        ┌───────────┼───────────┐
   Root domains   Subdomains   (given by program /
   (given)        (found from   found via root domains,
                    root domains)  used to filter OUT)
```

**always recon one domain at a time.** root domains are given, subdomains
are what you find *from* those root domains — and anything matching the
out-of-scope list gets filtered before it ever reaches your target list.

### automated enumeration

a mix of passive and active sources, run against root domains to pull the
maximum number of subdomains:

- **passive** — `amass enum -passive`, weyback machine URL scraping,
  cert transparency (`crt.sh`), Chaos (ProjectDiscovery's public dataset),
  GitHub subdomain scanning, VirusTotal, AlienVault OTX
- **active** — `amass enum -active`, Shodan (`ssl.cert.subject.CN`
  searches), ASN lookups (non-cloud targets), permutation/alteration
  scanning (`alterx`) on discovered subdomains
- **other signals** — CSP headers, favicons, archived pages — all can leak
  domains a straightforward subdomain scan would miss

### manual enumeration

for the stuff automation doesn't catch on its own:

- WHOIS + reverse WHOIS (registered domains under the same org/email)
- manually pulling emails via mxtoolbox and pivoting from there

### narrowing it down

```
subdomains + domains
        │
   clean + dedupe (regex strip protocol/paths)
        │
   filter by live status codes
        │
   ┌────┴────┐
 200.txt   403.txt / 401.txt
(mandatory)  (recommended — often reveal
             tech stack / auth type)
        │
  screenshot everything (gowitness)
        │
  manually review → find real targets
```

**what you're actually hunting for** once you've got live targets:
login forms, `.txt`/config files, input fields, 403/401 bypass
candidates, and anything else that stands out.

### priority targets

not everything found is equally worth digging into — some pages carry
way more risk than others:

**priority 1** — login pages, admin panels, dashboards, API endpoints,
single-page apps, payment pages *(high value, complex logic, more likely
to have real bugs)*

**priority 2** — registration pages, profile pages, search pages, mail/
webmail, dev/staging environments *(lower priority — usually less secured
but also lower impact)*

---

## ⚙️ the automation (`/Analysis`)

once you've actually got your scope narrowed down, this is where the
manual grind stops and the script takes over.

full breakdown, setup instructions, and usage are in
**[`Analysis/readme.md`](./Analysis/readme.md)** — short version:

```bash
cd Analysis
pip install -r requirements.txt --break-system-packages
./install.sh          # optional - makes `recon` runnable from anywhere

recon target.com
```

it runs url collection → fingerprinting → js secret scanning → param
discovery → directory bruteforce, all chained and parallelized, and spits
out a clean summary when it's done.

---

## ⚠️ use it responsibly

everything in this repo — the methodology and the automation — is for
targets you own or have explicit written authorization to test. bug
bounty in-scope assets, your own infra, CTFs, whatever. always confirm
scope before you scan anything.

---

## 💬 got thoughts?

suggestions, bug reports, methodology improvements — all welcome.

discord → https://discord.gg/d9wFhhnwFe

miro board → https://miro.com/app/board/uXjVHAlbwYw=/?share_link_id=227022886951

<div align="center">

---

made with way too much caffeine by

# **H7N**

</div>
