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


class ScoreSeriesRole(StrEnum):
    CANONICAL = "canonical"
    AUXILIARY = "auxiliary"


class BoundType(StrEnum):
    ZERO = "zero"
    RANDOM_CHANCE = "random_chance"
    NAIVE = "naive"
    HUMAN = "human"
    BENCHMARK_SPECIFIC = "benchmark_specific"
    THEORETICAL = "theoretical"
    EMPIRICAL = "empirical"


class ResourceScope(StrEnum):
    BENCHMARK = "benchmark"
    MODEL = "model"
    GENERAL = "general"


class ResourceType(StrEnum):
    OFFICIAL_SITE = "official_site"
    PAPER = "paper"
    OFFICIAL_LEADERBOARD = "official_leaderboard"
    GITHUB_REPOSITORY = "github_repository"
    MODEL_CARD = "model_card"
    SYSTEM_CARD = "system_card"
    TECHNICAL_REPORT = "technical_report"
    RELEASE_POST = "release_post"
    DOCUMENTATION = "documentation"
    EVALUATION_LOG = "evaluation_log"
    OTHER = "other"


class ResourceAuthority(StrEnum):
    PRIMARY = "primary"
    TRUSTED_SECONDARY = "trusted_secondary"
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
class ScoreSeriesDefinition:
    id: str
    role: ScoreSeriesRole
    metric_id: str
    protocol_id: str
    task_set_id: str
    lifecycle_eligible: bool
    label: str = ""
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.id or not self.metric_id or not self.protocol_id or not self.task_set_id:
            raise ValueError("score series identity, metric, protocol, and task set are required")
        if self.role is ScoreSeriesRole.AUXILIARY and self.lifecycle_eligible:
            raise ValueError("auxiliary score series cannot be lifecycle eligible")


@dataclass(frozen=True)
class Benchmark:
    id: str
    canonical_name: str
    aliases: tuple[str, ...] = ()
    domains: tuple[str, ...] = ()
    modalities: tuple[str, ...] = ()
    description: str = ""
    maintainer: Optional[str] = None
    resource_ids: tuple[str, ...] = ()


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
    resource_ids: tuple[str, ...] = ()


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
class Resource:
    """A canonical source resource shared by benchmark and model evidence."""

    id: str
    resource_scope: tuple[ResourceScope, ...]
    entity_id: Optional[str]
    resource_type: ResourceType
    title: str
    url: str
    publisher: Optional[str]
    authority: ResourceAuthority
    active: bool = True
    watch: bool = False
    last_checked_at: Optional[date] = None
    notes: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.id or not self.title or not self.url:
            raise ValueError("Resource id, title, and url are required")
        if not self.resource_scope:
            raise ValueError("Resource requires at least one scope")


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
    source_ids: tuple[str, ...] = field(default_factory=tuple)
    model_family_id: Optional[str] = None
    metric_id: Optional[str] = None
    protocol_id: Optional[str] = None
    model_release_date: Optional[date] = None
    result_public_date: Optional[date] = None
    date_precision: Optional[str] = None
    date_notes: Optional[str] = None
    contemporaneous: Optional[bool] = None
    validity_status: ValidityStatus = ValidityStatus.UNVERIFIED
    reported_uncertainty: Optional[tuple[Optional[float], Optional[float], str]] = None
    setting: Optional[str] = None
    notes: Optional[str] = None
    ingested_at: Optional[datetime] = None
    parser_version: str = "manual"
    score_series_id: Optional[str] = None
    score_role: ScoreSeriesRole = ScoreSeriesRole.CANONICAL

    def __post_init__(self) -> None:
        if not self.id or not self.benchmark_version_id or not self.model_id:
            raise ValueError("observation identity fields are required")
        if not self.score_unit or not self.evaluation_protocol:
            raise ValueError("score_unit and evaluation_protocol are required")
        if not self.source_ids:
            raise ValueError("every observation requires at least one source resource")

    @property
    def provenance_ids(self) -> tuple[str, ...]:
        """Backward-compatible name for callers using the pre-Resource schema."""
        return self.source_ids
