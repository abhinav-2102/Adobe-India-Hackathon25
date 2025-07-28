###Challenge 1b: Multi-Collection PDF Analysis
##Overview
This project is an advanced PDF analysis solution designed to process multiple collections of documents. It intelligently extracts and ranks relevant content based on user-defined personas and specific tasks, making it a powerful tool for quickly finding the most important information within a large set of PDFs.

The system can handle documents in various languages by automatically translating them to English before analysis. It outputs structured JSON files containing ranked sections and further analysis, which can be easily integrated into other workflows.

Project Structure
The project is organized to handle multiple "collections," where each collection represents a distinct use case with its own set of PDFs and analysis configuration.

```
├── Collection1/
│   ├── PDFs/
│   │   └── ... (your PDF files)
│   ├── input.json
│   └── output.json
├── Collection2/
│   └── ...
├── Collection3/
│   └── ...
├── Dockerfile
├── README.md
├── analyzer.py
├── main.py
├── pdf_utils.py
├── ranker.py
└── requirements.txt
```
## File Descriptions

* **`main.py`**: The main entry point for the application. It orchestrates the entire workflow, from handling user input for persona and task definitions to processing each collection and generating the final output.
  
* **`pdf_utils.py`**: A utility module for all PDF-related operations. It uses `PyPDF2` to extract text, `langdetect` to identify the language of the content, and the `Helsinki-NLP` models via the `transformers` library to translate text to English.
  
* **`ranker.py`**: This script is responsible for the core intelligence of the application. It uses the `sentence-transformers` library to encode the user's task and the extracted PDF section titles into vector embeddings, then ranks them by cosine similarity to find the most relevant content.
  
* **`analyzer.py`**: A module designed for deeper, more granular analysis of the top-ranked sections. It can be extended to perform summarization, entity extraction, or other NLP tasks.
  
* **`Dockerfile`**: A script to create a Docker image containing the Python environment and all necessary dependencies. This allows the application to run in an isolated, portable container.

* **`requirements.txt`**: Lists all the Python packages required for the project, such as `torch`, `transformers`, and `PyPDF2`.

* **`input.json`**: A configuration file automatically generated for each collection. It stores the persona, the job to be done, and the list of documents to be analyzed.

* **`output.json`**: The final, structured output of the analysis for a collection. It includes metadata, a ranked list of the most important sections, and any refined analysis.

## How to Run

You can run this project either locally with a Python environment or using Docker.

## Local Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Prepare Collections**:
    Create a directory for each collection (e.g., `Collection1`). Inside each collection directory, create a `PDFs` subdirectory and place your PDF files in it.

4.  **Run the Application**:
    ```bash
    python main.py
    ```
    The script will prompt you to enter a `Persona Role` and a `Job To Be Done` for each collection it finds.
    
## Docker Setup

1.  **Build the Docker Image**:
    From the project's root directory, run the following command:
    ```bash
    docker build -t pdf-analysis-engine .
    ```

2.  **Run the Docker Container**:
    You need to mount the project directory into the container to allow it to read your PDFs and write the output files.

    * On macOS or Linux:
        ```bash
        docker run -it --rm -v "$(pwd)":/app pdf-analysis-engine
        ```
    * On Windows (Command Prompt):
        ```bash
        docker run -it --rm -v "%cd%":/app pdf-analysis-engine
        ```
    * On Windows (PowerShell):
        ```bash
        docker run -it --rm -v "${PWD}:/app" pdf-analysis-engine
        ```
## Input and Output Format

### `input.json`

This file defines the parameters for an analysis job.

```json
{
  "challenge_info": {
    "challenge_id": "collection1",
    "test_case_name": "collection1",
    "description": "Collection 1"
  },
  "documents": [
    {
      "filename": "some_document.pdf",
      "title": "some_document"
    }
  ],
  "persona": {
    "role": "A specific user role (e.g., Financial Analyst)"
  },
  "job_to_be_done": {
    "task": "A specific task (e.g., Find revenue growth over the last 5 years)"
  }
}
```

output.json
This file contains the results of the analysis.
```json
{
  "metadata": {
    "input_documents": ["some_document.pdf"],
    "persona": "A specific user role",
    "job_to_be_done": "A specific task",
    "processing_timestamp": "2025-07-28T14:30:00.123456"
  },
  "extracted_sections": [
    {
      "document": "some_document.pdf",
      "section_title": "Most Relevant Section Title",
      "importance_rank": 1,
      "page_number": 15
    },
    {
      "document": "some_document.pdf",
      "section_title": "Second Most Relevant Section",
      "importance_rank": 2,
      "page_number": 4
    }
  ],
  "subsection_analysis": [
    {
      "document": "some_document.pdf",
      "refined_text": "Refined summary of section 'Most Relevant Section Title' on page 15.",
      "page_number": 15
    }
  ]
}
```
