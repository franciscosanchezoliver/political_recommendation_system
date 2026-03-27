import argparse
import json
from pathlib import Path

from src.ingest import ingest_pdfs
from src.cli import run_interview
from src.scoring import score_parties

import logging
logging.basicConfig(level=logging.INFO)

PARTIES = ["PP", "PSOE", "Vox", "Sumar", "Podemos"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ingest", nargs="*", help="PDF files to ingest")
    parser.add_argument("--persist-dir", default="./data/chroma")
    parser.add_argument(
        "--recommend",
        action="store_true",
        help="Run recommend flow",
    )
    args = parser.parse_args()

    if args.ingest is not None:
        pdfs = args.ingest
        print(f"Ingesting PDFs: {pdfs}")
        Path(args.persist_dir).mkdir(parents=True, exist_ok=True)
        ingest_pdfs(pdfs, persist_directory=args.persist_dir)
        print("Ingestion complete.")

    if args.recommend:
        profile = run_interview()
        results = score_parties(profile, PARTIES)
        print("\nRecommendation results:")
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
