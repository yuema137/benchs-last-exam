# Capability labels

BLE separates three kinds of metadata:

- `evaluation_type` describes how the evaluated system acts: `Model` or `Agent`.
- `domain` is one mutually exclusive primary task or subject domain.
- `labels` is a many-to-many list of capabilities centrally demanded by the task.

Free-form `tags` remain available for protocol, format, population, implementation, and search metadata. A tag is not automatically a capability label.

The controlled bilingual vocabulary lives in `data/capability_labels.json`. Each record contains a short name, a taxonomy definition, and a one-sentence `coverage_statement` explaining how that capability appears in a task. Every active benchmark must reference at least one valid label ID. The typed registry loader and integration validator reject missing, duplicate, or unknown labels.

Detail pages render the coverage statement under every assigned label. The frontend resolves this copy from the controlled registry; it must not maintain separate label explanations in HTML or JavaScript. Keep the statement concrete, short, and focused on what the evaluated system must actually do.

## Curation rule

Assign a label only when success on the canonical benchmark meaningfully requires that capability. Do not add labels merely because:

- the domain name contains a similar word;
- the evaluator uses code or tests behind the scenes;
- a task says a tool is unavailable;
- the capability is incidental to a small subset;
- a free-form tag resembles a label.

Labels describe task demands; they do not claim that a benchmark causally isolates an internal model mechanism. A broad benchmark may have several labels. A narrow benchmark may truthfully have one.

Reasoning labels are deliberately mechanism-specific. Difficulty, multi-step work, planning, or the word "reasoning" in benchmark prose does not by itself justify a reasoning label:

- `formal-deductive-reasoning` requires explicit premises, rules, constraints, or a formal system;
- `rule-induction-abstraction` requires discovering latent rules or representations from examples;
- `commonsense-inference` requires unstated everyday or physical-world knowledge to judge plausible outcomes;
- `mechanistic-reasoning` requires a causal, scientific, or operational model of how a system behaves.

For example, an agent that browses, calls tools, and plans is not automatically deductive. A physics benchmark may carry both `mechanistic-reasoning` and `quantitative-reasoning`, because those labels describe different demands.

`scripts/suggest_capability_labels.py` is an audit helper. Its output is a starting suggestion, never runtime truth. Accepted labels are written explicitly into the per-benchmark source record and reviewed in diff.

## Filter semantics

The homepage label control is multi-select. Multiple selected labels use AND semantics. For example:

```text
Planning + Tool use
```

returns benchmarks carrying both labels. Domain, evaluation type, year, coverage, search, and labels compose as additional filters. Applying filters restores Capability frontier ascending order unless the user subsequently chooses another sortable column.
