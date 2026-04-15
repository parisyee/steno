#!/usr/bin/env python3
"""Generate a styled PDF from a transcript string or .txt file."""

import argparse
from datetime import date
from pathlib import Path

from fpdf import FPDF

LINE_HEIGHT_MM = 6
MARGIN_MM = 25


def write_pdf(
    transcript: str,
    output_path: Path,
    source_name: str,
    transcribed_date: str | None = None,
) -> None:
    """Write a transcript to a PDF file with a metadata header.

    Args:
        transcript: The transcript text, with blank lines for cadence/pauses.
        output_path: Destination .pdf file path.
        source_name: Source filename shown in the header (e.g. "interview.mp4").
        transcribed_date: Date string for the header. Defaults to today.
    """
    if transcribed_date is None:
        transcribed_date = date.today().strftime("%B %-d, %Y")

    pdf = FPDF()
    pdf.set_margins(MARGIN_MM, MARGIN_MM, MARGIN_MM)
    pdf.set_auto_page_break(auto=True, margin=MARGIN_MM)
    pdf.add_page()

    # Header: source filename
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.cell(0, LINE_HEIGHT_MM, source_name, ln=True)

    # Header: transcription date
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, LINE_HEIGHT_MM, f"Transcribed: {transcribed_date}", ln=True)

    # Horizontal rule
    pdf.ln(2)
    x1 = pdf.get_x()
    y = pdf.get_y()
    pdf.line(x1, y, pdf.w - MARGIN_MM, y)
    pdf.ln(6)

    # Transcript body
    pdf.set_font("Helvetica", size=11)
    usable_width = pdf.w - 2 * MARGIN_MM

    for line in transcript.splitlines():
        if line.strip():
            pdf.multi_cell(usable_width, LINE_HEIGHT_MM, line)
        else:
            pdf.ln(LINE_HEIGHT_MM)

    pdf.output(str(output_path))


def main():
    parser = argparse.ArgumentParser(description="Convert a transcript .txt file to PDF")
    parser.add_argument("input_file", type=Path, help="Path to a transcript .txt file")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output .pdf path (default: <input_name>.pdf)",
    )
    args = parser.parse_args()

    if not args.input_file.exists():
        import sys
        sys.exit(f"Error: File not found: {args.input_file}")

    output_path = args.output or args.input_file.with_suffix(".pdf")
    transcript = args.input_file.read_text(encoding="utf-8")
    write_pdf(transcript, output_path, source_name=args.input_file.name)
    print(f"PDF written to {output_path}")


if __name__ == "__main__":
    main()
