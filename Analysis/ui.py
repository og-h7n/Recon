"""
Terminal UI for the recon pipeline.
Wraps the existing tool classes (GetAllUrls, JsScanner, para_finder,
dir_brtfrce, fingerprinting) with a styled banner + step-by-step status
+ final results table. Doesn't change how the tools run (still plain
os.system / threading under the hood) - this just renders around them.

Usage:
    from ui import ReconUI

    ui = ReconUI(target="example.com", tools=[...])
    ui.banner()

    with ui.step("gau") as s:
        tool.run_gau()
        s.result(count=ui.count_lines("_gau_.txt"))

    ui.summary()
"""

import time
from contextlib import contextmanager
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()

AUTHOR_TAG = "-h7n"


class StepResult:
    """Handed to the caller inside a `with ui.step(...)` block so it can
    attach a count / note once the underlying tool call finishes."""

    def __init__(self):
        self.count = None
        self.note = ""
        self.failed = False

    def result(self, count=None, note=""):
        self.count = count
        self.note = note

    def fail(self, note=""):
        self.failed = True
        self.note = note


class ReconUI:
    def __init__(self, target: str, tools=None):
        self.target = target
        self.tools = tools or []
        self.steps = []
        self.start_time = time.time()

    # ------------------------------------------------------------------
    def banner(self):
        title = Text("R E C O N   S C A N N E R", style="bold cyan", justify="center")
        sub = Text(f"target: {self.target}", style="bold white", justify="center")

        body = Text()
        if self.tools:
            body.append("tools loaded  ", style="dim")
            body.append(" • ".join(self.tools), style="green")

        panel_content = Text()
        panel_content.append_text(title)
        panel_content.append("\n")
        panel_content.append_text(sub)
        if self.tools:
            panel_content.append("\n\n")
            panel_content.append_text(body)

        console.print()
        console.print(
            Panel(
                Align.center(panel_content),
                box=box.DOUBLE,
                border_style="cyan",
                padding=(1, 4),
            )
        )
        console.print(Align.center(Text(AUTHOR_TAG, style="dim italic")))
        console.print()

    # ------------------------------------------------------------------
    def section(self, name: str):
        """Prints a section divider for grouping steps (e.g. 'URL Collection', 'Fingerprinting')."""
        console.print()
        console.rule(f"[bold magenta]{name}[/bold magenta]", style="magenta")

    # ------------------------------------------------------------------
    @contextmanager
    def step(self, name: str):
        console.print(f"[bold yellow][*][/bold yellow] running [bold]{name}[/bold] ...")
        started = time.time()
        result = StepResult()
        try:
            yield result
        except Exception as e:
            result.failed = True
            result.note = str(e)
            elapsed = time.time() - started
            self.steps.append((name, result, elapsed))
            console.print(
                f"[bold red][!][/bold red] {name} raised an exception "
                f"[dim]({elapsed:.1f}s)[/dim] — {result.note}"
            )
            return  # swallow so the pipeline can continue to the next step
        else:
            elapsed = time.time() - started
            self.steps.append((name, result, elapsed))

            if result.failed:
                console.print(
                    f"[bold red][!][/bold red] {name} failed "
                    f"[dim]({elapsed:.1f}s)[/dim] — {result.note}"
                )
            else:
                count_str = f", {result.count} results" if result.count is not None else ""
                note_str = f" — {result.note}" if result.note else ""
                console.print(
                    f"[bold green][+][/bold green] {name} done "
                    f"[dim]({elapsed:.1f}s{count_str})[/dim]{note_str}"
                )

    # ------------------------------------------------------------------
    def summary(self):
        total_elapsed = time.time() - self.start_time

        table = Table(
            title=f"Scan Summary — {self.target}",
            box=box.SIMPLE_HEAVY,
            title_style="bold cyan",
            header_style="bold white",
        )
        table.add_column("Step", style="bold")
        table.add_column("Status", justify="center")
        table.add_column("Results", justify="right")
        table.add_column("Time", justify="right", style="dim")

        for name, result, elapsed in self.steps:
            status = "[bold red]FAILED[/bold red]" if result.failed else "[bold green]OK[/bold green]"
            results_str = str(result.count) if result.count is not None else "-"
            table.add_row(name, status, results_str, f"{elapsed:.1f}s")

        console.print()
        console.print(table)

        ok = sum(1 for _, r, _ in self.steps if not r.failed)
        failed = sum(1 for _, r, _ in self.steps if r.failed)

        footer = Text()
        footer.append(f"{ok} succeeded", style="green")
        if failed:
            footer.append("  •  ", style="dim")
            footer.append(f"{failed} failed", style="red")
        footer.append("  •  ", style="dim")
        footer.append(f"total {total_elapsed:.1f}s", style="dim")

        console.print()
        console.print(Align.center(footer))
        console.print(Align.center(Text(AUTHOR_TAG, style="dim italic")))
        console.print()

    # ------------------------------------------------------------------
    @staticmethod
    def count_lines(filepath: str) -> int:
        p = Path(filepath)
        if not p.exists():
            return 0
        return sum(1 for _ in p.open(errors="ignore"))
