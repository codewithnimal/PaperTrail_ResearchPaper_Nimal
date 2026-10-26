"""
Utility functions for text processing, pattern matching, and secure path validation.
"""
import re
from pathlib import Path
from typing import List, Tuple, Optional


def resolve_safe_path(base_dir: Path, relative_or_absolute_path: str) -> Path:
    """
    Resolve and validate that a file path is strictly inside base_dir
    to prevent path traversal vulnerabilities.
    """
    target = Path(relative_or_absolute_path)
    if not target.is_absolute():
        target = (base_dir / target).resolve()
    else:
        target = target.resolve()

    base_resolved = base_dir.resolve()
    if not str(target).startswith(str(base_resolved)):
        raise ValueError(f"Path traversal detected or access outside base directory: {relative_or_absolute_path}")

    return target


def find_paper_file(base_dir: Path, relative_or_absolute_path: str) -> Optional[Path]:
    """
    Safely find an uploaded paper PDF file across configured storage and common sibling directories
    (such as backend-java/data/papers or data/papers) regardless of current working directory.
    """
    if not relative_or_absolute_path:
        return None

    # 1. Try standard resolve_safe_path within base_dir
    try:
        candidate = resolve_safe_path(base_dir, relative_or_absolute_path)
        if candidate.is_file():
            return candidate
    except Exception:
        pass

    # 2. Search by filename across known sibling storage locations
    filename = Path(relative_or_absolute_path).name
    # Prevent traversal in the filename itself
    if ".." in filename or "/" in filename or "\\" in filename:
        return None

    candidate_dirs = [
        base_dir.resolve(),
        (base_dir.parent / "backend-java" / "data" / "papers").resolve(),
        (base_dir.parent.parent / "backend-java" / "data" / "papers").resolve(),
        (base_dir.parent.parent / "data" / "papers").resolve(),
        (Path.cwd() / "backend-java" / "data" / "papers").resolve(),
        (Path.cwd() / "data" / "papers").resolve(),
        (Path.cwd().parent / "backend-java" / "data" / "papers").resolve(),
    ]

    for cdir in candidate_dirs:
        try:
            target = cdir / filename
            if target.is_file():
                return target
        except Exception:
            continue

    return None


def clean_text(text: str) -> str:
    """Normalize whitespace and strip unprintable characters."""
    if not text:
        return ""
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()


def extract_numbers_and_units(text: str) -> List[Tuple[float, str]]:
    """
    Find numbers and optional units/metrics (e.g., 94.5%, 0.85 F1, 10k, 1000 samples).
    """
    pattern = r'\b(\d+(?:\.\d+)?)\s*(%|percent|f1|accuracy|bleu|rouge|samples|epochs|parameters|params|m|b)?(?!\w)'
    matches = []
    for match in re.finditer(pattern, text, re.IGNORECASE):
        try:
            val = float(match.group(1))
            unit = (match.group(2) or "").strip().lower()
            if unit == "percent":
                unit = "%"
            matches.append((val, unit))
        except ValueError:
            continue
    return matches


def extract_title_from_text(first_page_text: str) -> Optional[str]:
    """
    Extract probable paper title from the top of the first page.
    Heuristic: Look for non-empty lines before authors/abstract.
    """
    if not first_page_text:
        return None
    lines = [line.strip() for line in first_page_text.split('\n') if line.strip()]
    if not lines:
        return None

    # Skip generic headers like "arXiv:...", "Conference...", "IEEE..."
    for line in lines[:5]:
        if len(line) > 10 and not any(line.lower().startswith(x) for x in ["arxiv:", "issn", "doi", "vol.", "http", "www."]):
            return line[:200]
    return lines[0][:200]
