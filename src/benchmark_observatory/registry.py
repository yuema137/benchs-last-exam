"""Typed loader for the repository's per-benchmark source records."""

from __future__ import annotations

import json
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


REQUIRED_LOCALIZED_KEYS = frozenset({"en", "zh"})
VALID_EVALUATION_TYPES = frozenset({"Model", "Agent"})
VALID_EVALUATION_TARGETS = frozenset(
    {"final_output", "environment_outcome", "process_and_output"}
)
VALID_INPUT_UNITS = frozenset({"fraction", "percentage_points", "number"})
VALID_SCORE_FORMATS = frozenset({"ratio", "number"})


@dataclass(frozen=True)
class LocalizedText:
    en: str
    zh: str

    @classmethod
    def from_mapping(cls, value: object, *, field_name: str) -> "LocalizedText":
        if not isinstance(value, dict) or set(value) != REQUIRED_LOCALIZED_KEYS:
            raise ValueError(f"{field_name} must contain exactly non-empty en and zh text")
        if not all(isinstance(value[key], str) and value[key].strip() for key in REQUIRED_LOCALIZED_KEYS):
            raise ValueError(f"{field_name} must contain exactly non-empty en and zh text")
        return cls(en=value["en"].strip(), zh=value["zh"].strip())

    def as_dict(self) -> dict[str, str]:
        return {"en": self.en, "zh": self.zh}


@dataclass(frozen=True)
class ScoringDefinition:
    metric_name: str
    explanation: LocalizedText

    @classmethod
    def from_mapping(cls, value: object) -> "ScoringDefinition":
        if not isinstance(value, dict) or set(value) != {"metric_name", "explanation"}:
            raise ValueError("scoring must contain exactly metric_name and explanation")
        metric_name = value["metric_name"]
        if not isinstance(metric_name, str) or not metric_name.strip():
            raise ValueError("scoring.metric_name must be non-empty text")
        return cls(
            metric_name=metric_name.strip(),
            explanation=LocalizedText.from_mapping(
                value["explanation"], field_name="scoring.explanation"
            ),
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "metric_name": self.metric_name,
            "explanation": self.explanation.as_dict(),
        }


@dataclass(frozen=True)
class BenchmarkSpec(Mapping[str, Any]):
    """One complete canonical benchmark/version declaration.

    The mapping interface is intentionally temporary: it lets the existing
    scientific build functions consume typed records without mixing the large
    registry migration with a second computation rewrite.
    """

    id: str
    name: str
    domain: str
    evaluation_type: str
    tags: tuple[str, ...]
    file: str
    score: str
    release: str
    floor: float | None
    ceiling: float | None
    source: str
    summary: LocalizedText
    task_format: LocalizedText
    scoring: ScoringDefinition
    evaluation_target: str
    protocol: str
    metric_id: str
    protocol_id: str
    input_unit: str
    hard_min: float | None
    hard_max: float | None
    progress_baseline: float | None
    progress_target: float | None
    registry_order: int
    score_format: str = "ratio"
    score_multiplier: float | None = None
    score_decimals: int | None = None
    cost_column: str | None = None
    cost_divisor: int | None = None
    frontier_exclude_ids: tuple[str, ...] = ()
    frontier_exclude_models: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, value: object, *, path: Path) -> "BenchmarkSpec":
        if not isinstance(value, dict):
            raise ValueError(f"{path}: benchmark specification must be an object")
        required = {
            "id", "name", "domain", "evaluation_type", "tags", "file", "score",
            "release", "floor", "ceiling", "source", "summary", "task_format",
            "scoring", "evaluation_target", "protocol", "metric_id", "protocol_id",
            "input_unit", "hard_min", "hard_max", "progress_baseline", "progress_target",
            "registry_order",
        }
        optional = {
            "score_format", "score_multiplier", "score_decimals", "cost_column",
            "cost_divisor", "frontier_exclude_ids", "frontier_exclude_models",
        }
        missing = required - set(value)
        unknown = set(value) - required - optional
        if missing or unknown:
            raise ValueError(
                f"{path}: invalid fields; missing={sorted(missing)}, unknown={sorted(unknown)}"
            )

        def text(key: str) -> str:
            item = value[key]
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"{path}: {key} must be non-empty text")
            return item.strip()

        benchmark_id = text("id")
        if path.stem != benchmark_id:
            raise ValueError(f"{path}: filename must match benchmark id {benchmark_id!r}")
        try:
            date.fromisoformat(text("release"))
        except ValueError as error:
            raise ValueError(f"{path}: release must be an ISO calendar date") from error
        source = text("source")
        if urlsplit(source).scheme not in {"http", "https"}:
            raise ValueError(f"{path}: source must be an HTTP(S) URL")
        evaluation_type = text("evaluation_type")
        if evaluation_type not in VALID_EVALUATION_TYPES:
            raise ValueError(f"{path}: unsupported evaluation_type {evaluation_type!r}")
        evaluation_target = text("evaluation_target")
        if evaluation_target not in VALID_EVALUATION_TARGETS:
            raise ValueError(f"{path}: unsupported evaluation_target {evaluation_target!r}")
        input_unit = text("input_unit")
        if input_unit not in VALID_INPUT_UNITS:
            raise ValueError(f"{path}: unsupported input_unit {input_unit!r}")
        score_format = value.get("score_format", "ratio")
        if score_format not in VALID_SCORE_FORMATS:
            raise ValueError(f"{path}: unsupported score_format {score_format!r}")
        tags = value["tags"]
        if not isinstance(tags, list) or not tags or not all(
            isinstance(tag, str) and tag.strip() for tag in tags
        ):
            raise ValueError(f"{path}: tags must be a non-empty text array")

        numeric_fields = (
            "floor", "ceiling", "hard_min", "hard_max", "progress_baseline",
            "progress_target", "score_multiplier",
        )
        for key in numeric_fields:
            item = value.get(key)
            if item is not None and (not isinstance(item, (int, float)) or isinstance(item, bool)):
                raise ValueError(f"{path}: {key} must be numeric or null")
        for key in ("score_decimals", "cost_divisor"):
            item = value.get(key)
            if item is not None and (not isinstance(item, int) or isinstance(item, bool)):
                raise ValueError(f"{path}: {key} must be an integer or null")
        if not isinstance(value["registry_order"], int) or isinstance(value["registry_order"], bool):
            raise ValueError(f"{path}: registry_order must be an integer")
        for key in ("frontier_exclude_ids", "frontier_exclude_models"):
            item = value.get(key, [])
            if not isinstance(item, list) or not all(isinstance(entry, str) for entry in item):
                raise ValueError(f"{path}: {key} must be a text array")

        return cls(
            id=benchmark_id,
            name=text("name"),
            domain=text("domain"),
            evaluation_type=evaluation_type,
            tags=tuple(tag.strip() for tag in tags),
            file=text("file"),
            score=text("score"),
            release=text("release"),
            floor=value["floor"],
            ceiling=value["ceiling"],
            source=source,
            summary=LocalizedText.from_mapping(value["summary"], field_name="summary"),
            task_format=LocalizedText.from_mapping(value["task_format"], field_name="task_format"),
            scoring=ScoringDefinition.from_mapping(value["scoring"]),
            evaluation_target=evaluation_target,
            protocol=text("protocol"),
            metric_id=text("metric_id"),
            protocol_id=text("protocol_id"),
            input_unit=input_unit,
            hard_min=value["hard_min"],
            hard_max=value["hard_max"],
            progress_baseline=value["progress_baseline"],
            progress_target=value["progress_target"],
            registry_order=value["registry_order"],
            score_format=score_format,
            score_multiplier=value.get("score_multiplier"),
            score_decimals=value.get("score_decimals"),
            cost_column=value.get("cost_column"),
            cost_divisor=value.get("cost_divisor"),
            frontier_exclude_ids=tuple(value.get("frontier_exclude_ids", [])),
            frontier_exclude_models=tuple(value.get("frontier_exclude_models", [])),
        )

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "domain": self.domain,
            "evaluation_type": self.evaluation_type,
            "tags": list(self.tags),
            "file": self.file,
            "score": self.score,
            "release": self.release,
            "floor": self.floor,
            "ceiling": self.ceiling,
            "source": self.source,
            "summary": self.summary.as_dict(),
            "task_format": self.task_format.as_dict(),
            "scoring": self.scoring.as_dict(),
            "evaluation_target": self.evaluation_target,
            "protocol": self.protocol,
            "metric_id": self.metric_id,
            "protocol_id": self.protocol_id,
            "input_unit": self.input_unit,
            "hard_min": self.hard_min,
            "hard_max": self.hard_max,
            "progress_baseline": self.progress_baseline,
            "progress_target": self.progress_target,
        }
        optional = {
            "score_format": self.score_format if self.score_format != "ratio" else None,
            "score_multiplier": self.score_multiplier,
            "score_decimals": self.score_decimals,
            "cost_column": self.cost_column,
            "cost_divisor": self.cost_divisor,
            "frontier_exclude_ids": self.frontier_exclude_ids or None,
            "frontier_exclude_models": self.frontier_exclude_models or None,
        }
        result.update({key: value for key, value in optional.items() if value is not None})
        return result

    def __getitem__(self, key: str) -> Any:
        return self.as_dict()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.as_dict())

    def __len__(self) -> int:
        return len(self.as_dict())


def load_benchmark_specs(registry_dir: Path, raw_dir: Path) -> list[BenchmarkSpec]:
    """Load every JSON file as one active benchmark, with no side inclusion list."""

    paths = sorted(registry_dir.glob("*.json"))
    if not paths:
        raise ValueError(f"No benchmark specifications found in {registry_dir}")
    specs: list[BenchmarkSpec] = []
    seen_ids: set[str] = set()
    seen_identity: set[tuple[str, str, str]] = set()
    for path in paths:
        try:
            payload = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"{path}: cannot read benchmark specification: {error}") from error
        spec = BenchmarkSpec.from_mapping(payload, path=path)
        if spec.id in seen_ids:
            raise ValueError(f"Duplicate benchmark id: {spec.id}")
        identity = (spec.name.casefold(), spec.protocol_id, spec.score)
        if identity in seen_identity:
            raise ValueError(f"Duplicate canonical benchmark measurement: {identity}")
        source_file = raw_dir / spec.file
        if not source_file.is_file():
            raise ValueError(f"{path}: raw observation file does not exist: {source_file}")
        seen_ids.add(spec.id)
        seen_identity.add(identity)
        specs.append(spec)
    orders = [spec.registry_order for spec in specs]
    if len(set(orders)) != len(orders):
        raise ValueError("benchmark registry_order values must be unique")
    if sorted(orders) != list(range(len(specs))):
        raise ValueError("benchmark registry_order values must be contiguous from zero")
    return sorted(
        specs,
        key=lambda spec: spec.registry_order,
    )
