#Challenge 1a: PDF Processing Solution

## Overview

This repository contains a sample solution for **Challenge 1a** of the Adobe India Hackathon 2025. The goal is to extract a hierarchical outline from a collection of PDF documents based on typographic structure (font sizes), and save the structured output as JSON files.

The solution is implemented using **PyMuPDF (fitz)** for PDF parsing and includes a command-line interface. It is fully containerized using Docker for reproducibility and compatibility with the challenge constraints.

## Official Challenge Guidelines

### ✅ Submission Requirements

- `GitHub Project`: Complete code repository with working solution
- `Dockerfile`: Must be functional and located in the root directory
- `README.md`: Clear documentation of the solution, models, and technologies used

---## 🛠 Build & Run

### 🐳 Build Command

```bash
docker build --platform linux/amd64 -t pdf-outline-extractor .
```
🚀 Run the Docker Container

```bash
docker run --rm \
  -v $(pwd)/Sample\ Dataset/PDFs:/app/input:ro \
  -v $(pwd)/Sample\ Dataset/Output:/app/output \
  --network none \
  pdf-outline-extractor
```
📁 Ensure:

PDFs/ folder contains input .pdf files.
Output/ folder exists and is writable.

✅ Key Features

Title Extraction: Automatically identifies the document title.
Outline Generation: Extracts heading hierarchy (H1–H3) based on font sizes.
Structured Output: Produces a clean JSON format for each PDF.
Fully Containerized: Compatible with AMD64 CPUs using Docker.

📤 Output Format Example

Each output JSON file follows this schema:

```
{
  "title": "Sample Document Title",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "Background", "page": 2 }
  ]
}
```
⚙️ Script Usage (main.py)
```
python main.py --input "./Sample Dataset/PDFs" --output "./Sample Dataset/Output"
```

🧪 Validation Checklist

 All PDFs in input directory are processed
 Corresponding .json output created
 Output includes title + outline
 Structure matches expected JSON format
 No internet required at runtime
 Compatible with AMD64 architecture
 Container runs within 10 seconds for 50-page PDFs
 Memory usage within 16GB limit

📚 Dependencies

Only one external library is required:
PyMuPDF==1.24.1
```
Install via:
pip install -r requirements.txt
```

📌 Notes

Output JSONs are saved to the Sample Dataset/Output/ directory.
Only .pdf files are processed.
Headings are determined by most frequent font sizes (largest → H1).
