# Explanation Style Guide

## Goal

Explain evaluation concepts so that a technically curious reader can understand what changed, why it matters, how a number is produced, and where the conclusion stops.

For Observatory specifically, always separate “what the benchmark score says” from “whether we had strong enough probes to know.” Explain coverage before making a lifecycle claim.

## Required structure

For a dense concept, use this order when useful:

1. State the practical question.
2. Name the actor, object, and changed step.
3. Show the before/after mechanism or data flow.
4. Give one small worked example with real schema fields, a formula, or a short trace.
5. State the boundary, caveat, and what the result does not establish.

Prefer causal sentences over abstract noun piles. Explain unfamiliar terms at first meaningful use and then use the stable project label consistently.

## DongbeiGPT principles

DongbeiGPT is a clarity discipline, not a dialect costume. In direct Chinese explanations:

- use plain, concrete wording;
- keep a relaxed conversational rhythm when the context allows it;
- say what a field or metric actually does before naming it;
- use a compact example when a relationship is easy to misunderstand;
- preserve technical terms, formulas, and distinctions exactly;
- remove colloquial markers whenever they reduce precision or accessibility;
- avoid regional vocabulary, performance of accent, jokes, and empty friendliness.

For formal documentation, methodology, schemas, tests, and code, keep the requested professional style. The style guide governs explanatory organization and clarity; it does not authorize changing technical claims.

## Bilingual rule

The English page is canonical. The Chinese page must preserve the same information and evidence while reading as natural Chinese. Translate meaning, not word order. Do not translate identifiers, benchmark names, paper titles, formulas, URLs, or code literals.
