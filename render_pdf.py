from argparse import ArgumentParser
from pathlib import Path

from playwright.sync_api import sync_playwright
from pypdf import PdfReader


def render_pdf(html_path: Path, pdf_path: Path) -> None:
    html_path = html_path.resolve()
    pdf_path = pdf_path.resolve()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome")
        page = browser.new_page()
        page.goto(html_path.as_uri())
        page.pdf(
            path=str(pdf_path),
            format="Letter",
            print_background=True,
            prefer_css_page_size=True,
        )
        browser.close()

    page_count = len(PdfReader(str(pdf_path)).pages)
    if page_count != 1:
        raise RuntimeError(f"Expected a one-page PDF, but rendered {page_count} pages.")


def main() -> None:
    parser = ArgumentParser(description="Render an HTML resume to a verified one-page PDF.")
    parser.add_argument("html", nargs="?", default="resume.html", help="Path to the source HTML resume.")
    parser.add_argument("--out", default=None, help="Output PDF path. Defaults to <html-dir>/resume.pdf.")
    args = parser.parse_args()

    html_path = Path(args.html)
    pdf_path = Path(args.out) if args.out else html_path.with_name("resume.pdf")
    render_pdf(html_path, pdf_path)


if __name__ == "__main__":
    main()
