"""Canonical schema models.

These models intentionally use only the Python standard library in the first
milestone. Serialization and JSON Schema generation can be added later without
coupling the scientific core to an ingestion source.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import StrEnum
from typing import Optional


class Direction(StrEnum):
    HIGHER_IS_BETTER = "higher_is_better"
    LOWER_IS_BETTER = "lower_is_better"


class BoundType(StrEnum):
    ZERO = "zero"
    RANDOM_CHANCE = "random_chance"
    NAIVE = "naive"
    HUMAN = "human"
    BENCHMARK_SPECIFIC = "benchmark_specific"
    THEORETICAL = "theoretical"
    EMPIRICAL = "empirical"


class SourceType(StrEnum):
    PRIMARY = "primary"
    TRUSTED_AGGREGATOR = "trusted_aggregator"
    SECONDARY = "secondary"


class ValidityStatus(StrEnum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    DISPUTED = "disputed"
    RETRACTED = "retracted"


class PanelRole(StrEnum):
    HISTORICAL_ANCHOR = "historical_anchor"
    CONTEMPORARY_FRONTIER = "contemporary_frontier"
    DOMAIN_SPECIALIST = "domain_specialist"
    OPEN_WEIGHT_FRONTIER = "open_weight_frontier"


@dataclass(frozen=True)
class Bound:
    value: float
    type: BoundType
    provenance_id: Optional[str] = None


@dataclass(frozen=True)
class MetricDefinition:
    id: str
    name: str
    direction: Direction
    unit: str
    bounded: bool
    floor: Optional[Bound] = None
    ceiling: Optional[Bound] = None
    normalization_policy_version: str = "v1"

    def __post_init__(self) -> None:
        if not self.id or not self.name or not self.unit:
            raise ValueError("MetricDefinition id, name, and unit are required")
        if self.bounded and (self.floor is None or self.ceiling is None):
            raise ValueError("bounded metrics require both floor and ceiling")
        if self.floor and self.ceiling and self.floor.value == self.ceiling.value:
            raise ValueError("floor and ceiling must differ")


@dataclass(frozen=True)
class Benchmark:
    id: str
    canonical_name: str
    aliases: tuple[str, ...] = ()
    domains: tuple[str, ...] = ()
    modalities: tuple[str, ...] = ()
    description: str = ""
    maintainer: Optional[str] = None


@dataclass(frozen=True)
class BenchmarkVersion:
    id: str
    benchmark_id: str
    version_label: str
    release_date: Optional[date]
    metric_definition_id: str
    scoring_protocol: str
    validity_status: str = "active"
    comparability_notes: Optional[str] = None


@dataclass(frozen=True)
class Model:
    id: str
    canonical_name: str
    family_id: Optional[str] = None
    release_date: Optional[date] = None
    provider: Optional[str] = None
    model_card_uri: Optional[str] = None
    organization: Optional[str] = None
    roles: tuple[PanelRole, ...] = ()
    domains: tuple[str, ...] = ()
    panel_start: Optional[date] = None
    panel_end: Optional[date] = None
    inclusion_reason: str = ""
    predecessor_id: Optional[str] = None


@dataclass(frozen=True)
class ReferenceModelPanel:
    id: str
    label: str
    valid_from: date
    valid_until: Optional[date]
    scope: str
    domain: Optional[str]
    member_ids: tuple[str, ...]
    methodology_version: str


@dataclass(frozen=True)
class PanelMembership:
    panel_id: str
    model_id: str
    role: PanelRole
    organization: Optional[str]
    weight: float
    valid_from: date
    valid_until: Optional[date]
    inclusion_reason: str

    def __post_init__(self) -> None:
        if self.weight < 0:
            raise ValueError("panel membership weight cannot be negative")
        if not self.inclusion_reason:
            raise ValueError("panel membership requires an inclusion reason")


@dataclass(frozen=True)
class SourceProvenance:
    id: str
    source_type: SourceType
    url: str
    title: Optional[str]
    publisher: Optional[str]
    publication_date: Optional[date]
    retrieved_at: datetime
    source_revision: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.id or not self.url:
            raise ValueError("SourceProvenance id and url are required")


@dataclass(frozen=True)
class ScoreObservation:
    id: str
    benchmark_version_id: str
    model_id: str
    score: float
    score_unit: str
    evaluation_date: Optional[date]
    reported_date: Optional[date]
    public_available_date: Optional[date]
    evaluation_protocol: str
    provenance_ids: tuple[str, ...] = field(default_factory=tuple)
    validity_status: ValidityStatus = ValidityStatus.UNVERIFIED
    reported_uncertainty: Optional[tuple[Optional[float], Optional[float], str]] = None
    setting: Optional[str] = None
    notes: Optional[str] = None
    ingested_at: Optional[datetime] = None
    parser_version: str = "manual"

    def __post_init__(self) -> None:
        if not self.id or not self.benchmark_version_id or not self.model_id:
            raise ValueError("observation identity fields are required")
        if not self.score_unit or not self.evaluation_protocol:
            raise ValueError("score_unit and evaluation_protocol are required")
        if not self.provenance_ids:
            raise ValueError("every observation requires provenance")
