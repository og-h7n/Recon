#!/usr/bin/env python3
"""
The Final scanner which does all the work.
Run it and do some other work.

    python3 main.py target.com

-h7n
"""

import sys
import os

from get_urls import GetAllUrls
from DirBrtfrcing import dir_brtfrce
from Fingerprinting import fingerprinting
from jsScan import Js_scanner
from param import para_finder

from ui import ReconUI

TOOLS = [
    "gau", "katana", "gospider", "uro", "httpx",
    "dirsearch", "feroxbuster",
    "whatweb", "nmap", "wafw00f", "wappalyzer", "curl",
    "mantra", "jsecret",
    "arjun",
    "gowitness",
]


def main(target: str):
    ui = ReconUI(target=target, tools=TOOLS)
    ui.banner()

    base_dir = os.getcwd()

    # ------------------------------------------------------------------
    # 1. URL collection: gau + katana + gospider -> dedup/liveness -> screenshots
    # ------------------------------------------------------------------
    ui.section("URL Collection")
    urls = GetAllUrls(target)

    with ui.step("gau") as s:
        try:
            urls.run_gau()
            s.result(count=ui.count_lines("_gau_.txt"))
        except Exception as e:
            s.fail(str(e))

    with ui.step("katana") as s:
        try:
            urls.run_katana()
            s.result(count=ui.count_lines("_katana_.txt"))
        except Exception as e:
            s.fail(str(e))

    with ui.step("gospider") as s:
        try:
            urls.run_gospider()
            s.result(count=ui.count_lines("_gospider_.txt"))
        except Exception as e:
            s.fail(str(e))

    with ui.step("dedup + liveness (uro + httpx)") as s:
        try:
            urls.rm_junk()
            s.result(count=ui.count_lines("_LiveUrls_.txt"))
        except Exception as e:
            s.fail(str(e))

    with ui.step("screenshots (gowitness)") as s:
        try:
            urls.screen_shot()
            s.result(count=ui.count_lines("_screenshot_targets_.txt"))
        except Exception as e:
            s.fail(str(e))

    # get-urls.py's run_all() chdir's into "Urls_collected" - urls live there now
    live_urls_path = os.path.join(base_dir, "Urls_collected", "_LiveUrls_.txt")

    # ------------------------------------------------------------------
    # 2. Fingerprinting: whatweb, httpx, nmap, wafw00f, wappalyzer, curl
    # ------------------------------------------------------------------
    ui.section("Fingerprinting")
    os.chdir(base_dir)
    fp = fingerprinting(target)

    with ui.step("fingerprint sweep (whatweb/httpx/nmap/wafw00f/wappalyzer/curl)") as s:
        try:
            fp.run_all()
            s.result(note="see Fingerprint/ folder for individual tool outputs")
        except Exception as e:
            s.fail(str(e))

    # ------------------------------------------------------------------
    # 3. JS secret scanning: filter .js -> mantra + jsecret
    # ------------------------------------------------------------------
    ui.section("JavaScript Analysis")
    os.chdir(base_dir)
    js = Js_scanner(live_urls_path)

    with ui.step("js secret scan (mantra + jsecret)") as s:
        try:
            js.run_js()
            s.result(count=ui.count_lines("js_files.txt"), note="secrets printed above, if any")
        except Exception as e:
            s.fail(str(e))

    # ------------------------------------------------------------------
    # 4. Parameter discovery: grep '=' + arjun
    # ------------------------------------------------------------------
    ui.section("Parameter Discovery")
    os.chdir(base_dir)
    params = para_finder(live_urls_path, target)

    with ui.step("parameter discovery (arjun + grep)") as s:
        try:
            params.run_js()  # note: method name in param.py, kept as-is
            s.result(count=ui.count_lines("param.txt"))
        except Exception as e:
            s.fail(str(e))

    # ------------------------------------------------------------------
    # 5. Directory bruteforce: feroxbuster + dirsearch
    # ------------------------------------------------------------------
    ui.section("Directory Bruteforce")
    os.chdir(base_dir)
    dirs = dir_brtfrce(f"https://{target}")

    with ui.step("directory bruteforce (ferox + dirsearch)") as s:
        try:
            dirs.run_all()
            s.result(
                count=ui.count_lines("ferox_results.txt") + ui.count_lines("Dirseach_results.txt")
            )
        except Exception as e:
            s.fail(str(e))

    os.chdir(base_dir)
    ui.summary()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target.com>")
        sys.exit(1)

    main(sys.argv[1])
