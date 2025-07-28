import os
import json
import datetime
from pdf_utils import extract_sections
from ranker import rank_sections
from analyzer import analyze_subsections

BASE_DIR = r"D:\Projects\adobe_india_hackathon\challenge_1b"

def get_user_inputs(collection_name):
    print(f"\n📝 Provide inputs for '{collection_name}'")
    role = input("Enter Persona Role: ").strip()
    job = input("Enter Job To Be Done: ").strip()
    return role, job

def generate_input_json(collection_path, documents, role, job):
    folder_name = os.path.basename(collection_path)
    challenge_id = folder_name.replace(" ", "_").lower()

    input_json = {
        "challenge_info": {
            "challenge_id": challenge_id,
            "test_case_name": challenge_id,
            "description": folder_name.replace("_", " ").title()
        },
        "documents": [
            {
                "filename": doc,
                "title": os.path.splitext(doc)[0]
            } for doc in documents
        ],
        "persona": {
            "role": role
        },
        "job_to_be_done": {
            "task": job
        }
    }

    input_path = os.path.join(collection_path, 'input.json')
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(input_json, f, indent=2)

    print(f"[{folder_name}] 📥 input.json generated.")

def process_collection(collection_path):
    input_dir = os.path.join(collection_path, 'PDFs')
    output_file = os.path.join(collection_path, 'output.json')

    if not os.path.exists(input_dir):
        print(f"Skipping '{collection_path}': Missing 'PDFs' directory.")
        return

    documents = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]

    if not documents:
        print(f"Skipping '{collection_path}': No PDFs found.")
        return

    role, job = get_user_inputs(os.path.basename(collection_path))

    # Generate input.json using the user-provided values
    generate_input_json(collection_path, documents, role, job)

    metadata = {
        "input_documents": documents,
        "persona": role,
        "job_to_be_done": job,
        "processing_timestamp": datetime.datetime.now().isoformat()
    }

    extracted_sections = []
    refined_subsections = []

    for doc in documents:
        doc_path = os.path.join(input_dir, doc)

        try:
            result = extract_sections(doc_path, translate_always=True)
            sections = result["sections"]
            print(f"[{os.path.basename(collection_path)}] Processing '{doc}' in {result['language']}; sections: {len(sections)}")
        except Exception as e:
            print(f"[{os.path.basename(collection_path)}] ❌ Error processing {doc}: {e}")
            continue

        ranked = rank_sections(sections, {"role": role, "job": job})

        for idx, sec in enumerate(ranked):
            extracted_sections.append({
                "document": doc,
                "section_title": sec["title"],
                "importance_rank": idx + 1,
                "page_number": sec["page"]
            })

            refined = analyze_subsections(doc_path, sec)
            refined_subsections.append({
                "document": doc,
                "refined_text": refined,
                "page_number": sec["page"]
            })

    output = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": refined_subsections
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"[{os.path.basename(collection_path)}] ✅ output.json generated.")

def main():
    if not os.path.exists(BASE_DIR):
        print("❌ Base directory 'Challenge_1b/' not found.")
        return

    collections = [
        os.path.join(BASE_DIR, d)
        for d in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, d))
    ]

    for collection_path in collections:
        process_collection(collection_path)

if __name__ == "__main__":
    main()
