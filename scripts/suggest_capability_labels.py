#!/usr/bin/env python3
"""Suggest controlled capability-demand labels from source metadata.

The suggestions bootstrap the initial migration and help curators inspect new
cards. They are not runtime derivation: accepted labels remain explicit in each
canonical benchmark record and must be reviewed by a human.
"""

import argparse
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "benchmarks"
LABELS = json.loads((ROOT / "data" / "capability_labels.json").read_text())["labels"]
LABEL_ORDER = {item["id"]: index for index, item in enumerate(LABELS)}


def normalized(value):
    value = unicodedata.normalize("NFKD", value).casefold()
    return re.sub(r"[^\w]+", " ", value).strip()


def has(text, *needles):
    return any(re.search(rf"(?<!\w){re.escape(normalized(needle))}(?!\w)", text) for needle in needles)


def suggest(record):
    metadata = normalized(" ".join([
        record["id"], record["name"],
        *record["tags"], record["summary"]["en"],
    ]))
    task = normalized(record["task_format"]["en"])
    text = f"{metadata} {task}"
    labels = set()

    if record["domain"] == "Multimodal":
        labels.add("multimodal-perception")
    if record["domain"] == "Long context":
        labels.add("long-context-integration")
    if record["domain"] == "Mathematics":
        labels.add("quantitative-reasoning")

    knowledge_domains = {"General knowledge & reasoning", "Science", "Health", "Life Science", "Chemistry",
                         "Materials Science", "Earth Science", "Nuclear Engineering", "Biomedical Engineering"}
    if record["evaluation_type"] == "Model" and (record["domain"] in knowledge_domains or has(metadata, "multiple-choice", "ten-choice", "knowledge", "academic", "factuality",
           "open-domain qa", "reading comprehension", "closed book", "exam", "olympiad",
           "nomenclature", "trivia", "language understanding", "protocolqa")):
        labels.add("knowledge-recall")
    retrieval_needles = ["browsing", "browser", "rag", "citation", "evidence", "pdf", "documentation",
                         "literature", "database", "open-domain qa", "web"]
    if record["evaluation_type"] == "Agent":
        retrieval_needles.append("research")
    retrieval_text = text if record["evaluation_type"] == "Agent" else metadata
    if has(retrieval_text, *retrieval_needles):
        labels.add("information-retrieval")
    if has(text, "formal proof", "formally checked", "lean 4", "logical deduction", "symbolic reasoning",
           "explicit rules", "stated rules", "formal system", "decision-theoretic"):
        labels.add("formal-deductive-reasoning")
    if has(text, "abstract transformation", "latent rule", "hidden rule", "rule induction",
           "infer goals", "unfamiliar interactive environments"):
        labels.add("rule-induction-abstraction")
    if has(text, "commonsense", "plausible continuation", "everyday situation", "likely to work",
           "more plausible"):
        labels.add("commonsense-inference")
    if has(text, "mechanistic", "physical principles", "scientific principles", "causal structure",
           "physical system", "circuit", "control engineering", "thermodynamics", "climate",
           "astrodynamics", "power flow", "finite element", "physics", "chemical reasoning",
           "experimental failure", "diagnosis", "troubleshooting"):
        labels.add("mechanistic-reasoning")
    if record["domain"] in {
        "Mathematics", "Physics", "Electrical Engineering", "Nuclear Engineering",
        "Computational Engineering", "Mechanical & Aerospace Engineering", "Energy & Infrastructure",
    } or has(text, "numerical", "numeric", "quantitative", "calculation", "thermodynamics",
             "formula", "mathemat", "physics", "power cycles", "finite element", "cfd", "pde"):
        labels.add("quantitative-reasoning")
    if has(text, "spatial", "geometry", "3d", "cad", "crystal", "structure", "layout", "manipulation",
           "embodied", "robot", "circuit", "breadboard", "gui grounding"):
        labels.add("spatial-reasoning")
    if has(text, "multimodal", "vision", "visual", "video", "image", "diagram", "chart", "plot",
           "screenshot", "handwriting", "vqa", "egocentric", "xrd"):
        labels.add("multimodal-perception")
    if has(text, "long context", "long-context", "long document", "repository", "multi-file", "codebase",
           "research replication", "pdf", "notebook"):
        labels.add("long-context-integration")
    if record["domain"] == "Instruction following" or has(metadata, "instruction", "constraints", "format",
           "function calling", "function calls", "tool calls", "api", "policy", "contract"):
        labels.add("instruction-following")

    if record["evaluation_type"] == "Agent" or has(metadata, "planning"):
        labels.add("planning")
    tool_text = text if record["evaluation_type"] == "Agent" else metadata
    if record["evaluation_type"] == "Agent" and (has(tool_text, "tool", "tools", "tool use", "api", "browser", "browsing", "terminal", "command line", "mcp", "software",
           "computer", "desktop", "notebook", "kaggle", "code execution", "fhir", "ehr") or record["domain"] in {
        "Tool use", "Terminal / OS", "Computer use", "Software engineering", "Science / research",
    }):
        labels.add("tool-use")
    if record["evaluation_type"] == "Agent":
        labels.add("environment-interaction")
    if has(text, "multi-turn", "multi-round", "long-horizon", "cross-application", "workflow", "games",
           "interactive", "state", "memory", "temporal", "trajectory"):
        labels.add("state-tracking")
    if record["evaluation_type"] == "Agent" and has(text, "debugging", "troubleshooting", "adaptation", "closed loop", "diagnosis", "repair",
           "regression safety", "failed", "error recovery"):
        labels.add("error-recovery")

    code_text = text if record["evaluation_type"] == "Agent" else metadata
    if record["domain"] in {"Coding", "Software engineering"} or has(code_text, "code generation", "coding",
           "python", "verilog", "systemverilog", "rtl", "solver generation", "vision-to-code",
           "scientific coding", "programmatic cad", "patch"):
        labels.add("code-generation")
    if has(code_text, "debugging", "code execution", "test-based", "unit tests", "repository", "terminal",
           "command line", "notebook", "execution", "regression safety", "kaggle"):
        labels.add("code-execution-debugging")
    if has(text, "experimental design", "experiments", "scientific discovery", "research replication",
           "designs experiments", "discover unknown", "hypothesis"):
        labels.add("experimental-design")
    if has(text, "design", "optimization", "generation", "editing", "engineering design", "molecule generation",
           "cad", "control systems", "artifact", "functional performance"):
        labels.add("design-optimization")

    return sorted(labels, key=LABEL_ORDER.__getitem__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-missing", action="store_true")
    args = parser.parse_args()
    counts = {item["id"]: 0 for item in LABELS}
    for path in sorted(REGISTRY.glob("*.json")):
        record = json.loads(path.read_text())
        proposed = suggest(record)
        for label in proposed:
            counts[label] += 1
        print(f"{record['id']}: {', '.join(proposed)}")
        if args.write_missing and "labels" not in record and proposed:
            record["labels"] = proposed
            path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    print("\nDistribution")
    for label in LABELS:
        print(f"{label['id']}: {counts[label['id']]}")


if __name__ == "__main__":
    main()
