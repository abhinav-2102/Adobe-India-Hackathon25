import fitz  # PyMuPDF
import json
import os
import time
from collections import Counter
import argparse
import logging

def setup_logger():
    """Configure and return a logger."""
    logger = logging.getLogger("pdf_outline_extractor")
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()

def get_font_sizes_by_frequency(doc):
    """
    Analyze all pages to extract rounded font sizes, returning list
    sorted by prevalence (frequency) descending, then by size descending.
    """
    sizes = Counter()
    flags = 4  # TEXTFLAGS_FONT
    for page in doc:
        blocks = page.get_text("dict", flags=flags).get("blocks", [])
        for block in blocks:
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        sizes[round(span["size"])] += 1
    ranked = [size for size, _ in sizes.most_common()]
    return ranked

def extract_outline(pdf_path, heading_levels=3, min_heading_length=3):
    """
    Extract the document title and a hierarchical outline (H1..Hn), based on font size.
    heading_levels: Number of heading levels to detect (default H1-H3).
    min_heading_length: Minimum length for a heading to be considered valid.
    Returns a dict with keys: 'title', 'outline'.
    """
    try:
        with fitz.open(pdf_path) as doc:
            font_sizes = get_font_sizes_by_frequency(doc)
            size_to_level = {}
            for i in range(1, heading_levels+1):
                if len(font_sizes) > i:
                    size_to_level[font_sizes[i]] = f"H{i}"
            title_size = font_sizes[0] if font_sizes else 0
            title = ""
            outline = []
            title_found = False
            flags = 4
            for page_num, page in enumerate(doc):
                blocks = page.get_text("dict", flags=flags).get("blocks", [])
                for block in blocks:
                    if block.get("type") == 0:
                        for line in block.get("lines", []):
                            if not line.get("spans"):
                                continue
                            span = line["spans"][0]
                            text = " ".join(s["text"] for s in line["spans"]).strip()
                            if not text:
                                continue
                            font_size = round(span["size"])
                            # Title detection (only on first 2 pages)
                            if font_size == title_size and not title_found and page_num < 2:
                                title = text
                                title_found = True
                                continue
                            # Heading detection with a minimum character length filter
                            if font_size in size_to_level and len(text) >= min_heading_length:
                                outline.append({
                                    "level": size_to_level[font_size],
                                    "text": text,
                                    "page": page_num + 1
                                })
            # Fallback for title
            if not title and len(doc) > 0:
                blocks = doc[0].get_text("blocks")
                if blocks:
                    title = blocks[0][4].split('\n')[0].strip()
            return {"title": title, "outline": outline}
    except Exception as e:
        logger.error(f"Error processing {pdf_path}: {e}")
        return None

def process_pdfs_in_directory(input_dir, output_dir, heading_levels=3, min_heading_length=3):
    """
    Processes all PDF files in the input directory, saving the results to the output directory as JSON.
    """
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        logger.warning(f"No PDFs found in {input_dir}")
        return
    for filename in pdf_files:
        pdf_path = os.path.join(input_dir, filename)
        logger.info(f"Processing {pdf_path} ...")
        start_time = time.time()
        result = extract_outline(pdf_path, heading_levels=heading_levels, min_heading_length=min_heading_length)
        elapsed = time.time() - start_time
        if result:
            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            logger.info(f"Created {output_path} ({elapsed:.2f} s)")
        else:
            logger.error(f"Failed to process {pdf_path}")

def parse_args():
    parser = argparse.ArgumentParser(description="Extract titles and outlines from PDFs based on font size hierarchy.")
    parser.add_argument("--input", "-i", default="./input", help="Input directory containing PDF files")
    parser.add_argument("--output", "-o", default="./output", help="Output directory for JSON files")
    parser.add_argument("--levels", "-l", type=int, default=3, help="Number of heading levels to detect (default 3: H1-H3)")
    parser.add_argument("--min-length", type=int, default=3, help="Minimum characters for a heading")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    input_dir = args.input
    output_dir = args.output
    levels = max(1, min(args.levels, 6))  # Limit heading levels to 1-6
    min_length = max(1, args.min_length)
    if not os.path.exists(input_dir):
        logger.warning(f"Input directory '{input_dir}' does not exist. Creating it.")
        os.makedirs(input_dir)
    process_pdfs_in_directory(input_dir, output_dir, heading_levels=levels, min_heading_length=min_length)
