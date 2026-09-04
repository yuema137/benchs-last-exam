#!/usr/bin/env python3
"""Build the small static benchmark snapshot used by the local site."""

import csv
import json
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "site" / "data" / "benchmarks.json"
RESOURCE_OUT = ROOT / "data" / "resources.json"
OBSERVATION_OUT = ROOT / "data" / "observations.jsonl"
MODEL_OUT = ROOT / "data" / "models.json"

BENCHMARKS = [
    {"id": "mmlu", "name": "MMLU", "domain": "General knowledge", "file": "mmlu_external.csv", "score": "EM", "release": "2020-09-07", "floor": 0.25, "ceiling": 1.0, "source": "https://arxiv.org/abs/2009.03300", "summary": {"en": "MMLU tests broad knowledge across academic and professional subjects.", "zh": "MMLU 测试模型在多个学术和专业领域里的综合知识。"}, "task_format": {"en": "Each item is a four-choice multiple-choice question. The model selects one answer.", "zh": "每个 task 都是四选一问题，模型需要选出一个答案。"}, "scoring": {"metric_name": "Exact-match accuracy", "explanation": {"en": "A response is correct only when the selected answer matches the answer key. The score is the fraction of questions answered correctly.", "zh": "只有模型选中的答案和标准答案一致，这道题才算答对。分数就是答对题目占全部题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "gsm8k", "name": "GSM8K", "domain": "Mathematics", "file": "gsm8k_external.csv", "score": "EM", "release": "2021-10-27", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2110.14168", "summary": {"en": "GSM8K tests whether a model can solve multi-step grade-school math word problems.", "zh": "GSM8K 测试模型能不能解决需要多步推理的小学数学应用题。"}, "task_format": {"en": "The model receives a natural-language math word problem and produces a solution with a final numerical answer.", "zh": "模型会收到一道自然语言数学应用题，需要给出解题过程和最后的数字答案。"}, "scoring": {"metric_name": "Exact-match accuracy", "explanation": {"en": "The final numerical answer must match the reference answer. The score is the percentage of problems answered correctly.", "zh": "最后的数字答案必须和标准答案一致。分数就是答对题目占全部题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "math-level-5", "name": "MATH Level 5", "domain": "Mathematics", "file": "math_level_5.csv", "score": "Best score (across scorers)", "release": "2021-03-05", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2103.03874", "summary": {"en": "MATH Level 5 is the hardest level of a competition-math dataset, intended to test difficult mathematical problem solving.", "zh": "MATH Level 5 是竞赛数学数据集里最难的一档，用来测试模型解决高难度数学题的能力。"}, "task_format": {"en": "The model receives a competition-style math problem and must produce a solution and final answer.", "zh": "模型会收到一道竞赛数学题，需要给出解答和最后答案。"}, "scoring": {"metric_name": "Answer accuracy", "explanation": {"en": "A problem counts as correct when the reported answer matches the reference answer under the benchmark scorer. The score is the fraction of correct problems.", "zh": "按照 benchmark scorer 的规则，模型答案和标准答案一致时，这道题才算答对。分数就是答对题目占全部题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "gpqa-diamond", "name": "GPQA Diamond", "domain": "Science reasoning", "file": "gpqa_diamond.csv", "score": "Best score (across scorers)", "release": "2023-11-20", "floor": 0.25, "ceiling": 1.0, "source": "https://arxiv.org/abs/2311.12022", "summary": {"en": "GPQA Diamond tests difficult science reasoning questions written and checked by domain experts.", "zh": "GPQA Diamond 测试由领域专家编写和核验的高难度科学推理题。"}, "task_format": {"en": "Each item is a four-choice science question. The model selects one answer, usually without access to external tools in the reported score.", "zh": "每个 task 都是四选一科学问题，模型需要选一个答案；公开分数通常不包含外部工具使用。"}, "scoring": {"metric_name": "Accuracy", "explanation": {"en": "The score is the percentage of questions for which the selected option is correct. Four choices make 25% the random-choice reference point.", "zh": "分数就是选项正确的题目占全部题目的比例。因为每题有四个选项，25% 是随机选择的参考 floor。"}}, "evaluation_target": "final_output"},
    {"id": "swe-bench-verified", "name": "SWE-bench Verified", "domain": "Coding / agents", "file": "swe_bench_verified.csv", "score": "Best score (across scorers)", "release": "2024-08-13", "floor": 0.0, "ceiling": 1.0, "source": "https://openai.com/index/introducing-swe-bench-verified/", "summary": {"en": "SWE-bench Verified tests whether a coding agent can resolve real GitHub issues in a repository.", "zh": "SWE-bench Verified 测试 coding agent 能不能在真实代码仓库里修复 GitHub issue。"}, "task_format": {"en": "The agent receives a repository and issue description, edits files in an environment, and submits a patch. This is not a one-shot answer task.", "zh": "agent 会收到一个代码仓库和 issue 描述，在环境里修改文件并提交 patch。这不是只回答一次文本的问题。"}, "scoring": {"metric_name": "Issue resolution rate", "explanation": {"en": "A task counts as solved when the submitted patch passes the task's required tests. The score is the percentage of issues resolved.", "zh": "如果提交的 patch 通过这个 task 要求的测试，这个 task 才算解决。分数就是解决 issue 占全部 issue 的比例。"}}, "evaluation_target": "environment_outcome"},
]

REFERENCE_ORGANIZATIONS = {"OpenAI", "Anthropic", "Google", "DeepSeek", "Qwen", "Meta", "xAI"}

MODEL_RELEASE_RESOURCES = {
    "fable-5-1": {
        "url": "https://www.anthropic.com/claude/fable",
        "title": "Claude Fable 5.1 official release page",
        "resource_type": "release_post",
        "publisher": "Anthropic",
    },
    "gpt-6-astra": {
        "url": "https://developers.openai.com/api/docs/models/gpt-6-astra",
        "title": "GPT-6 Astra official model page",
        "resource_type": "model_card",
        "publisher": "OpenAI",
    },
    "gemini-3-8-flash": {
        "url": "https://deepmind.google/models/model-cards/gemini-3-8-flash/",
        "title": "Gemini 3.8 Flash official model card",
        "resource_type": "model_card",
        "publisher": "Google DeepMind",
    },
    "deepseek-v4-pro-0813": {
        "url": "https://api-docs.deepseek.com/news/news260813/",
        "title": "DeepSeek-V4-Pro official release announcement",
        "resource_type": "release_post",
        "publisher": "DeepSeek",
    },
    "qwen3-8-max": {
        "url": "https://docs.modelstudio.console.alibabacloud.com/en/model-studio/qwen3-8-max",
        "title": "Qwen3.8-Max official model documentation",
        "resource_type": "documentation",
        "publisher": "Alibaba Cloud",
    },
    "llama-4-maverick": {
        "url": "https://ai.meta.com/llama/get-started/",
        "title": "Llama 4 Maverick official model resources",
        "resource_type": "model_card",
        "publisher": "Meta",
    },
    "grok-4-6": {
        "url": "https://x.ai/news/grok-4-6",
        "title": "Grok 4.6 official release announcement",
        "resource_type": "release_post",
        "publisher": "xAI",
    },
}

REFERENCE_MODEL_RELEASES = [
    {
        "id": "model-claude-fable-5-1",
        "canonical_name": "Claude Fable 5.1",
        "family_id": "anthropic-claude-fable-5-1",
        "release_date": "2026-09-01",
        "organization": "Anthropic",
        "role": "contemporary_frontier",
        "domain": "General knowledge & reasoning",
    },
    {
        "id": "model-gpt-6-astra",
        "canonical_name": "GPT-6 Astra",
        "family_id": "openai-gpt-6-astra",
        "release_date": "2026-09-03",
        "organization": "OpenAI",
        "role": "contemporary_frontier",
        "domain": "General knowledge & reasoning",
    },
    {
        "id": "model-gemini-3-8-flash",
        "canonical_name": "Gemini 3.8 Flash",
        "family_id": "google-gemini-3-8-flash",
        "release_date": "2026-09-02",
        "organization": "Google DeepMind",
        "role": "contemporary_frontier",
        "domain": "General knowledge & reasoning",
    },
    {
        "id": "model-deepseek-v4-pro-0813",
        "canonical_name": "DeepSeek-V4-Pro-0813",
        "family_id": "deepseek-v4-pro",
        "release_date": "2026-08-13",
        "organization": "DeepSeek",
        "role": "open_weight_frontier",
        "domain": "Coding",
    },
    {
        "id": "model-qwen-3-8-max",
        "canonical_name": "Qwen3.8-Max",
        "family_id": "qwen-3-8-max",
        "release_date": "2026-08-03",
        "organization": "Alibaba",
        "role": "open_weight_frontier",
        "domain": "General knowledge & reasoning",
    },
    {
        "id": "model-llama-4-maverick",
        "canonical_name": "Llama 4 Maverick",
        "family_id": "meta-llama-4",
        "release_date": "2025-04-05",
        "organization": "Meta",
        "role": "open_weight_frontier",
        "domain": "Multimodal",
    },
    {
        "id": "model-grok-4-6",
        "canonical_name": "Grok 4.6",
        "family_id": "xai-grok-4-6",
        "release_date": "2026-08-12",
        "organization": "xAI",
        "role": "contemporary_frontier",
        "domain": "General knowledge & reasoning",
    },
]

BENCHMARKS.extend([
    {"id": "mmlu-pro", "name": "MMLU-Pro", "domain": "General knowledge & reasoning", "file": "mmlu_pro_external.csv", "score": "Average Accuracy", "release": "2024-06-03", "floor": 0.1, "ceiling": 1.0, "source": "https://arxiv.org/abs/2406.01574", "summary": {"en": "MMLU-Pro is a harder, reasoning-focused successor to MMLU across academic and professional subjects.", "zh": "MMLU-Pro 是 MMLU 的 harder successor，覆盖多个学术和专业领域，更强调 reasoning。"}, "task_format": {"en": "Each item is a ten-choice multiple-choice question. The model selects one answer, usually after producing a reasoning trace under the chosen prompt.", "zh": "每个 task 都是十选一问题。模型需要选出一个答案，通常会按照指定 prompt 先进行 reasoning。"}, "scoring": {"metric_name": "Overall accuracy", "explanation": {"en": "The score is the fraction of questions for which the selected answer is correct. The benchmark has ten choices per question, so 10% is the random-choice reference point.", "zh": "分数就是选项正确的题目占全部题目的比例。每题有十个选项，所以 10% 是随机选择的参考 floor。"}}, "evaluation_target": "final_output", "protocol": "MMLU-Pro official repository mini-leaderboard overall accuracy; prompt and CoT settings remain source context and are not merged when materially different."},
    {"id": "simpleqa-verified", "name": "SimpleQA Verified", "domain": "General knowledge & reasoning", "file": "simpleqa_verified.csv", "score": "Best score (across scorers)", "release": "2025-09-09", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2509.07968", "summary": {"en": "SimpleQA Verified tests whether a model can answer short, fact-seeking questions with reliable, verifiable answers.", "zh": "SimpleQA Verified 测试模型能不能回答简短、事实导向且可以核验的问题。"}, "task_format": {"en": "Each item is a short fact-seeking question with a single target answer. The model produces a concise answer without browsing.", "zh": "每个 task 都是一道简短的事实问题，有一个目标答案。模型需要在不浏览网页的情况下给出简洁回答。"}, "scoring": {"metric_name": "Graded factuality accuracy", "explanation": {"en": "A grader labels the answer correct, incorrect, or not attempted. The reported score is the benchmark's graded accuracy under the fixed evaluation protocol.", "zh": "grader 会把答案标为正确、错误或未作答。报告分数是在固定评测 protocol 下的 factuality accuracy。"}}, "evaluation_target": "final_output", "protocol": "SimpleQA Verified fixed 1,000-question protocol; scores from the curated standardized evaluation export are kept together and are not merged with the original 4,326-question SimpleQA object."},
    {"id": "frontiermath-tiers-1-3-v2", "name": "FrontierMath Tiers 1–3 (v2)", "domain": "Mathematics", "file": "frontiermath_tiers_1_3_v2.csv", "score": "Best score (across scorers)", "release": "2026-06-12", "floor": 0.0, "ceiling": 1.0, "source": "https://epoch.ai/benchmarks/frontiermath-tiers-1-3", "summary": {"en": "FrontierMath Tiers 1–3 tests advanced mathematics problems written by experts and checked by executable verifiers.", "zh": "FrontierMath Tiers 1–3 测试专家编写、由可执行 verifier 检查的高难度数学题。"}, "task_format": {"en": "The model writes a Python answer function for each mathematics problem and can use an isolated Python tool while solving.", "zh": "模型需要为每道数学题编写 Python answer function，解题时可以使用隔离的 Python 工具。"}, "scoring": {"metric_name": "Verified task accuracy", "explanation": {"en": "A task counts as correct when the submitted answer passes the benchmark's verifier. The score is the fraction of verified tasks solved.", "zh": "提交的答案通过 benchmark verifier，这道题才算正确。分数就是通过验证的 task 占全部 task 的比例。"}}, "evaluation_target": "final_output"},
    {"id": "arc-agi-2", "name": "ARC-AGI-2", "domain": "Abstract / novel reasoning", "file": "arc_agi_2_external.csv", "score": "Score", "release": "2025-03-24", "floor": 0.0, "ceiling": 1.0, "source": "https://arcprize.org/blog/announcing-arc-agi-2-and-arc-prize-2025", "summary": {"en": "ARC-AGI-2 tests whether a system can infer abstract transformations from a few visual examples and generalize them to new grids.", "zh": "ARC-AGI-2 测试系统能否从少量视觉示例中推断抽象变换，并把规则泛化到新的网格。"}, "task_format": {"en": "Each task shows example input-output grids. The system must produce exactly two candidate outputs for the test input.", "zh": "每个 task 会给出输入和输出网格示例，系统需要为测试输入生成恰好两个候选输出。"}, "scoring": {"metric_name": "Pass@2 task accuracy", "explanation": {"en": "A task is correct when either of the two submitted outputs exactly matches the ground truth. The final score is the fraction of tasks solved this way.", "zh": "如果提交的两个输出中有一个和标准答案完全一致，这道题就算答对。最终分数是答对 task 的比例。"}}, "evaluation_target": "final_output"},
    {"id": "aider-polyglot", "name": "Aider Polyglot", "domain": "Coding / software engineering", "file": "aider_polyglot_external.csv", "score": "Percent correct", "score_multiplier": 0.01, "release": "2024-12-21", "floor": 0.0, "ceiling": 1.0, "source": "https://aider.chat/2024/12/21/polyglot.html", "summary": {"en": "Aider Polyglot tests whether a model can edit code correctly across six programming languages.", "zh": "Aider Polyglot 测试模型能不能在六种编程语言中正确修改代码。"}, "task_format": {"en": "The model receives an Exercism coding exercise and must make the requested repository edit using Aider's editing format.", "zh": "模型会收到一个 Exercism 编程题，需要用 Aider 要求的编辑格式修改代码仓库。"}, "scoring": {"metric_name": "Correct edit rate", "explanation": {"en": "A task counts as correct when the resulting code passes the benchmark checks. The score is the percentage of exercises completed correctly.", "zh": "修改后的代码通过 benchmark 检查，这道题才算正确。分数就是正确完成 exercise 的比例。"}}, "evaluation_target": "environment_outcome"},
    {"id": "osworld-2", "name": "OSWorld 2.0", "domain": "Agents / computer use", "file": "osworld_2_external.csv", "score": "Partial score", "release": "2026-06-26", "floor": 0.0, "ceiling": 1.0, "source": "https://os-world.github.io/", "summary": {"en": "OSWorld 2.0 tests whether a computer-use agent can complete tasks in real desktop and web applications.", "zh": "OSWorld 2.0 测试 computer-use agent 能不能在真实桌面和网页应用中完成任务。"}, "task_format": {"en": "The agent operates a computer through tools under a task and step budget, then receives credit for completing the requested outcome.", "zh": "agent 通过工具操作电脑，在规定的 task 和步数预算内完成目标，最后根据结果计分。"}, "scoring": {"metric_name": "Partial task score", "explanation": {"en": "The benchmark assigns partial credit for progress toward the requested computer-use outcome. The score is the average partial credit across tasks; it is distinct from binary task success.", "zh": "benchmark 会根据 computer-use task 的完成进度给部分分数。最终分数是所有 task 的平均 partial credit，和 binary task success 不是同一个指标。"}}, "evaluation_target": "environment_outcome", "protocol": "OSWorld 2.0 partial-score series. The source export's Partial score is used; binary accuracy is preserved in the raw CSV but is not mixed into this headline frontier."},
    {"id": "terminal-bench-2", "name": "Terminal-Bench 2.0", "domain": "Agents / computer use", "file": "terminalbench_external.csv", "score": "Accuracy mean", "release": "2025-11-07", "floor": 0.0, "ceiling": 1.0, "source": "https://www.tbench.ai/news/announcement-2-0", "summary": {"en": "Terminal-Bench 2.0 tests whether agents can solve realistic tasks inside terminal environments.", "zh": "Terminal-Bench 2.0 测试 agent 能不能在 terminal 环境中完成真实的软件和系统任务。"}, "task_format": {"en": "The agent receives a task in a containerized terminal environment and can use shell tools before submitting the final environment state.", "zh": "agent 会在容器化 terminal 环境中收到 task，可以使用 shell 工具，最后提交环境状态。"}, "scoring": {"metric_name": "Task success rate", "explanation": {"en": "A task counts as solved when its evaluator accepts the resulting environment or artifact. The score is the fraction of tasks solved.", "zh": "如果 evaluator 接受最终环境状态或产物，这个 task 就算解决。分数是解决 task 的比例。"}}, "evaluation_target": "environment_outcome"},
])

# ARC-AGI-1 has strong source support but only a year-level origin date in the
# current audit; keep it queued until a defensible release date is curated.
BENCHMARKS = [spec for spec in BENCHMARKS if spec["id"] != "arc-agi-1"]
for spec in BENCHMARKS:
    if spec["id"] == "aider-polyglot":
        spec["cost_column"] = "Cost"
        spec["cost_divisor"] = 225

BENCHMARKS.extend([
    {"id": "frontiercode-1-1", "name": "FrontierCode 1.1", "domain": "Coding / software engineering", "file": "frontiercode_external.csv", "score": "Main score", "release": "2026-02-05", "floor": 0.0, "ceiling": 1.0, "source": "https://cognition.com/blog/frontier-code-1.1", "summary": {"en": "FrontierCode 1.1 evaluates whether coding systems produce maintainable, regression-safe solutions under a maintainer-defined rubric.", "zh": "FrontierCode 1.1 评估 coding systems 能不能按照 maintainer 定义的标准，产出可维护且不会引入回归问题的解决方案。"}, "task_format": {"en": "The system works on software-engineering tasks and submits code changes evaluated with tests and rubric-based checks.", "zh": "系统需要完成 software-engineering task 并提交代码修改，结果会通过测试和 rubric 检查。"}, "scoring": {"metric_name": "Main score", "explanation": {"en": "The reported main score aggregates the benchmark's task-level quality and correctness criteria. It is not simply a raw unit-test pass rate.", "zh": "报告中的 main score 汇总了 benchmark 对 task 质量和正确性的多项判断，不只是原始的测试通过率。"}}, "evaluation_target": "process_and_output"},
    {"id": "arc-agi-1", "name": "ARC-AGI-1", "domain": "Abstract / novel reasoning", "file": "arc_agi_external.csv", "score": "Score", "release": "2019-11-01", "floor": 0.0, "ceiling": 1.0, "source": "https://arcprize.org/", "summary": {"en": "ARC-AGI-1 tests abstract visual reasoning: infer a transformation from a few example grids and apply it to a new grid.", "zh": "ARC-AGI-1 测试抽象视觉推理：模型需要从少量网格示例中推断变换规则，再应用到新网格。"}, "task_format": {"en": "Each task contains a few input-output grid examples. The system must generate the exact output grid for a new input.", "zh": "每个 task 包含几组输入输出网格示例，系统需要为新的输入生成完全一致的输出网格。"}, "scoring": {"metric_name": "Exact task accuracy", "explanation": {"en": "A task is correct only when the predicted grid exactly matches the target grid. The score is the fraction of tasks solved.", "zh": "只有预测网格和目标网格完全一致，这个 task 才算答对。分数是解决 task 的比例。"}}, "evaluation_target": "final_output", "cost_column": "Cost per task"},
])

# ARC-AGI-1 remains queued until its year-level origin date is curated as a
# precise benchmark release date.
BENCHMARKS = [spec for spec in BENCHMARKS if spec["id"] != "arc-agi-1"]

BENCHMARKS.extend([
    {"id": "frontiermath-tier-4-v2", "name": "FrontierMath Tier 4 (v2)", "domain": "Mathematics", "file": "frontiermath_tier_4_v2.csv", "score": "Best score (across scorers)", "release": "2026-06-12", "floor": 0.0, "ceiling": 1.0, "source": "https://epoch.ai/benchmarks/frontiermath-tier-4-v2", "summary": {"en": "FrontierMath Tier 4 tests research-level mathematics problems written and vetted by expert mathematicians.", "zh": "FrontierMath Tier 4 测试由数学专家编写和核验的 research-level 数学题。"}, "task_format": {"en": "The model reasons about a difficult mathematics problem and submits a Python answer function that is checked by an executable verifier.", "zh": "模型需要解决高难度数学题，并提交由可执行 verifier 检查的 Python answer function。"}, "scoring": {"metric_name": "Verified task accuracy", "explanation": {"en": "A task earns one point when the submitted answer passes the verifier. The score is the fraction of Tier 4 problems solved.", "zh": "提交的答案通过 verifier 才得一分。分数是解决的 Tier 4 题目占全部题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "arc-agi-3", "name": "ARC-AGI-3", "domain": "Abstract reasoning", "file": "arc_agi_3_gpt6.csv", "score": "Score", "release": "2026-03-25", "floor": 0.0, "ceiling": 1.0, "source": "https://arcprize.org/blog/arc-agi-3-launch", "summary": {"en": "ARC-AGI-3 tests whether an agent can explore unfamiliar interactive environments, infer goals, and adapt its actions.", "zh": "ARC-AGI-3 测试 agent 能不能探索陌生的 interactive environment，自己理解目标并调整行动。"}, "task_format": {"en": "The agent interacts with turn-based game-like environments without explicit instructions or stated goals, learning from feedback across levels.", "zh": "agent 会在没有明确说明和目标的回合制游戏式环境中行动，并根据反馈在不同 level 中学习。"}, "scoring": {"metric_name": "Human-normalized action-efficiency score", "explanation": {"en": "The score measures task success and action efficiency relative to a human action baseline; the official release reports humans at 100%.", "zh": "分数根据 task 是否成功以及行动效率相对 human action baseline 的表现计算；官方发布中 human score 是 100%。"}}, "evaluation_target": "environment_outcome"},
    {"id": "agents-last-exam", "name": "Agents' Last Exam (ALE-V1)", "domain": "General agent tasks", "file": "agents_last_exam_external.csv", "score": "Pass Rate", "release": "2026-06-03", "floor": 0.0, "ceiling": 1.0, "source": "https://agents-last-exam.org/leaderboard", "summary": {"en": "Agents' Last Exam evaluates agents on long-horizon, economically valuable professional workflows with verifiable outcomes.", "zh": "Agents' Last Exam 评估 agent 能不能完成有明确验证结果、耗时较长且贴近真实工作的专业任务。"}, "task_format": {"en": "An agent works through a real digital-work task using the required tools and environment, then submits an outcome that can be checked.", "zh": "agent 会在指定工具和环境中完成真实的数字工作任务，最后提交一个可以被验证的结果。"}, "scoring": {"metric_name": "Pass rate", "explanation": {"en": "Pass rate is the share of task runs that earn a perfect score. The leaderboard also reports an average partial-credit score separately.", "zh": "Pass rate 是拿到满分的 task run 占比。leaderboard 还会单独报告包含部分得分的平均 score。"}}, "evaluation_target": "environment_outcome"},
    {"id": "terminal-bench-science-0-1", "name": "Terminal-Bench-Science 0.1", "domain": "Science / research", "file": "terminal_bench_science_external.csv", "score": "Resolution rate", "release": "2026-05-20", "floor": 0.0, "ceiling": 1.0, "source": "https://www.terminal-bench-science.ai/announcement", "summary": {"en": "Terminal-Bench-Science evaluates agents on expert-curated research workflows across five scientific domains.", "zh": "Terminal-Bench-Science 评估 agent 能不能在五个科学领域完成专家挑选的真实研究工作流。"}, "task_format": {"en": "The agent works in a terminal environment on a scientific workflow and produces an analysis, simulation, proof, code, or data artifact.", "zh": "agent 会在 terminal 环境中完成科学工作流，产出分析、simulation、证明、代码或数据结果。"}, "scoring": {"metric_name": "Resolution rate", "explanation": {"en": "A task is resolved when its task-specific evaluator accepts the required scientific artifact or outcome. The reported rate averages three independent trials per task.", "zh": "当 task 专用 evaluator 接受所需的科学产物或最终结果时，task 才算解决。报告的 resolution rate 基于每个 task 的三次独立尝试。"}}, "evaluation_target": "environment_outcome"},
    {"id": "terminalworld-verified", "name": "TerminalWorld Verified", "domain": "Terminal / OS", "file": "terminalworld_verified_external.csv", "score": "Score", "release": "2026-05-21", "floor": 0.0, "ceiling": 1.0, "source": "https://terminalworld.ai/leaderboard/", "summary": {"en": "TerminalWorld Verified evaluates agents on real-world terminal workflows derived from developer recordings and manually verified.", "zh": "TerminalWorld Verified 评估 agent 能不能完成来自真实开发者操作记录、并经过人工核验的 terminal 工作流。"}, "task_format": {"en": "The agent operates inside an isolated Docker terminal environment and must reach the task's required final system state.", "zh": "agent 会在隔离的 Docker terminal 环境中操作，必须让系统达到 task 要求的最终状态。"}, "scoring": {"metric_name": "Verified task pass rate", "explanation": {"en": "The score is the fraction of the 200 human-verified tasks completed successfully. Results use the standardized Terminus-2 agent framework and Harbor harness.", "zh": "分数是 200 个经过人工核验的 task 中成功完成的比例。结果使用统一的 Terminus-2 agent framework 和 Harbor harness。"}}, "evaluation_target": "environment_outcome"},
    {"id": "terminal-bench-2-1", "name": "Terminal-Bench 2.1", "domain": "Terminal / OS", "file": "terminal_bench_2_1_external.csv", "score": "Accuracy mean", "release": "2026-05-06", "floor": 0.0, "ceiling": 1.0, "source": "https://www.tbench.ai/news/terminal-bench-2-1", "summary": {"en": "Terminal-Bench 2.1 measures agents on difficult, reproducible terminal tasks after fixing issues in 28 tasks from version 2.0.", "zh": "Terminal-Bench 2.1 评估 agent 完成高难度、可复现 terminal task 的能力，并修复了 2.0 版本中 28 个 task 的问题。"}, "task_format": {"en": "The agent receives an instruction and a containerized terminal task with tests, then must leave the environment in a passing state.", "zh": "agent 会收到指令和带测试的容器化 terminal task，最后必须让环境通过检查。"}, "scoring": {"metric_name": "Mean task accuracy", "explanation": {"en": "The reported accuracy is the mean task success rate under the listed agent-model setup. Different harnesses are kept as separate observations.", "zh": "报告的 accuracy 是指定 agent-model setup 下的平均 task 成功率。不同 harness 会作为不同 observation 保留。"}}, "evaluation_target": "environment_outcome"},
])

BENCHMARKS.extend([
    {"id": "terminal-bench-4-0", "name": "Terminal-Bench 4.0", "domain": "Terminal / OS", "file": "terminal_bench_4_0_external.csv", "score": "Resolution rate", "release": "2026-08-26", "floor": 0.0, "ceiling": 1.0, "source": "https://github.com/harbor-framework/terminal-bench/releases/tag/v4.0.0", "summary": {"en": "Terminal-Bench 4.0 measures agents on hard command-line tasks in reproducible container environments.", "zh": "Terminal-Bench 4.0 评估 agent 能不能在可复现的容器 terminal 环境中完成高难度命令行任务。"}, "task_format": {"en": "The agent works inside a container, runs commands, and must leave the environment in a state accepted by task-specific verification tests.", "zh": "agent 会在容器里运行命令，最后必须让环境达到 task 专用 verification tests 接受的状态。"}, "scoring": {"metric_name": "Resolution rate", "explanation": {"en": "The score is the fraction of benchmark trials whose final environment passes the task verifier. Version 4.0 has a separate task set and is not comparable with earlier versions by default.", "zh": "分数是最终环境通过 task verifier 的 benchmark trial 占比。4.0 使用独立的 task set，默认不能和早期版本直接比较。"}}, "evaluation_target": "environment_outcome"},
    {"id": "humanitys-last-exam", "name": "Humanity's Last Exam", "domain": "General knowledge & reasoning", "file": "humanitys_last_exam_external.csv", "score": "Accuracy", "release": "2025-04-03", "floor": 0.0, "ceiling": 1.0, "source": "https://labs.scale.com/leaderboard/humanitys_last_exam", "summary": {"en": "Humanity's Last Exam is a difficult, multi-domain academic question set designed to probe the frontier of model knowledge and reasoning.", "zh": "Humanity's Last Exam 是一个覆盖多个学科的高难度 academic question set，用来测试模型知识和推理能力的 frontier。"}, "task_format": {"en": "Each item is a text or multimodal academic question. The model returns an answer, and some items require a short explanation or structured response.", "zh": "每个 task 是文字或多模态 academic question。模型需要给出答案，有些题目还要求简短解释或结构化回答。"}, "scoring": {"metric_name": "Accuracy", "explanation": {"en": "The score is the percentage of questions answered correctly under the benchmark's answer and grading protocol.", "zh": "分数是在 benchmark 的答案和评分 protocol 下答对题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "cursorbench-3-2", "name": "CursorBench 3.2", "domain": "Software engineering", "file": "cursorbench_3_2_external.csv", "score": "Score", "release": "2026-07-08", "floor": 0.0, "ceiling": 1.0, "source": "https://cursor.com/cn/cursorbench", "cost_column": "Cost", "summary": {"en": "CursorBench 3.2 evaluates agents on ambiguous, multi-file software tasks drawn from real Cursor sessions.", "zh": "CursorBench 3.2 评估 agent 能不能完成来自真实 Cursor session、含糊且涉及多个文件的软件任务。"}, "task_format": {"en": "The agent receives a multi-file coding task and uses an editing environment and tools to modify the codebase.", "zh": "agent 会收到一个涉及多个文件的 coding task，并使用编辑环境和工具修改 codebase。"}, "scoring": {"metric_name": "Task score", "explanation": {"en": "The score is the percentage of tasks completed successfully under Cursor's task grader. Reported cost is estimated from token usage and published model pricing.", "zh": "分数是按照 Cursor task grader 成功完成的 task 比例。报告的 cost 根据 token 用量和公开 model 定价估算。"}}, "evaluation_target": "environment_outcome"},
    {"id": "gdpval-aa-v2", "name": "GDPval-AA v2", "domain": "General agent tasks", "file": "gdpval_aa_v2_external.csv", "score": "Elo", "release": "2026-04-18", "floor": None, "ceiling": None, "score_format": "number", "source": "https://artificialanalysis.ai/evaluations/gdpval-aa", "summary": {"en": "GDPval-AA v2 evaluates agentic systems on real-world professional deliverables across occupations and industries.", "zh": "GDPval-AA v2 评估 agent 能不能完成覆盖多个职业和行业的真实 professional deliverables。"}, "task_format": {"en": "The system uses shell and web access in an agentic loop to produce documents, slides, diagrams, spreadsheets, or other work products.", "zh": "系统会在 agentic loop 中使用 shell 和 web 工具，产出文档、slides、图表、表格或其他工作成果。"}, "scoring": {"metric_name": "Elo rating", "explanation": {"en": "Two anonymized submissions are compared by a judge; pairwise results are aggregated into an Elo rating anchored to a human baseline of 1,000. Elo is not a percentage accuracy measure.", "zh": "两个匿名 submission 会由 judge 进行比较，pairwise 结果汇总成以 human baseline 1,000 为锚点的 Elo rating。Elo 不是百分比 accuracy。"}}, "evaluation_target": "process_and_output"},
    {"id": "automationbench", "name": "AutomationBench", "domain": "General agent tasks", "file": "automationbench_external.csv", "score": "Pass Rate", "release": "2026-04-20", "floor": 0.0, "ceiling": 1.0, "source": "https://github.com/zapier/AutomationBench", "summary": {"en": "AutomationBench tests whether agents can complete realistic business workflows across simulated SaaS tools.", "zh": "AutomationBench 测试 agent 能不能在模拟的 SaaS 工具之间完成真实的 business workflow。"}, "task_format": {"en": "The agent uses APIs or tool calls across simulated CRM, inbox, calendar, and other business applications, then must leave the correct final state.", "zh": "agent 会通过 API 或 tool calls 操作模拟的 CRM、收件箱、日历和其他 business application，最后必须留下正确的最终状态。"}, "scoring": {"metric_name": "Strict task pass rate", "explanation": {"en": "A task passes only when every required assertion about the final environment state is satisfied. Partial credit is reported separately and is not the headline score.", "zh": "只有最终环境状态的所有 required assertion 都满足，task 才算通过。partial credit 会单独报告，不是 headline score。"}}, "evaluation_target": "environment_outcome"},
    {"id": "screenspot-pro", "name": "ScreenSpot-Pro", "domain": "Multimodal", "file": "screenspot_pro_external.csv", "score": "Accuracy", "release": "2025-01-04", "floor": 0.0, "ceiling": 1.0, "source": "https://github.com/likaixin2000/ScreenSpot-Pro-GUI-Grounding", "summary": {"en": "ScreenSpot-Pro tests whether a multimodal system can locate the precise UI element described in a natural-language instruction on a high-resolution professional screenshot.", "zh": "ScreenSpot-Pro 测试 multimodal system 能不能根据自然语言指令，在高分辨率的专业软件截图中准确找到目标 UI 元素。"}, "task_format": {"en": "Each item provides a screenshot and an instruction. The system predicts a point or bounding-box location for the requested icon or text element; the benchmark uses static screenshots rather than a full interactive desktop environment.", "zh": "每个 task 会提供一张截图和一条指令。系统需要预测指定 icon 或文字元素的位置；这个 benchmark 使用静态截图，不是完整的可交互桌面环境。"}, "scoring": {"metric_name": "Grounding accuracy", "explanation": {"en": "A prediction is correct when the predicted point falls inside the target element's ground-truth bounding box. The reported score is the micro-average accuracy over the benchmark instructions.", "zh": "如果预测点落在目标元素的标准 bounding box 内，就算答对。报告分数是所有 benchmark instruction 的 micro-average accuracy。"}}, "evaluation_target": "final_output", "protocol": "Comparable direct-grounding results only: greedy decoding with a single predicted location. Agentic multi-step or zoom-assisted results are not mixed into this capability frontier."},
])

# Keep the taxonomy intentionally small and stable. Evaluation type describes
# the benchmark's task setup; domain describes what the task is about.
TAXONOMY = {
    "mmlu": ("Model", "General knowledge & reasoning", ["multiple-choice", "academic"]),
    "gsm8k": ("Model", "Mathematics", ["multi-step", "word problems"]),
    "math-level-5": ("Model", "Mathematics", ["competition math"]),
    "gpqa-diamond": ("Model", "Science", ["expert", "multiple-choice", "reasoning"]),
    "swe-bench-verified": ("Agent", "Software engineering", ["repository", "test-based"]),
    "mmlu-pro": ("Model", "General knowledge & reasoning", ["multiple-choice", "reasoning", "ten-choice"]),
    "simpleqa-verified": ("Model", "General knowledge & reasoning", ["factuality", "short-answer", "grader"]),
    "frontiermath-tiers-1-3-v2": ("Model", "Mathematics", ["expert", "verifiable"]),
    "frontiermath-tier-4-v2": ("Model", "Mathematics", ["research-level", "expert", "verifiable"]),
    "arc-agi-2": ("Model", "Abstract reasoning", ["visual", "novel reasoning"]),
    "arc-agi-3": ("Agent", "Abstract reasoning", ["interactive", "novel reasoning", "adaptation"]),
    "aider-polyglot": ("Model", "Coding", ["code editing", "multi-language"]),
    "osworld-2": ("Agent", "Computer use", ["desktop", "web", "environment"]),
    "terminal-bench-2": ("Agent", "Terminal / OS", ["terminal", "container"]),
    "frontiercode-1-1": ("Agent", "Software engineering", ["code quality", "regression safety"]),
    "agents-last-exam": ("Agent", "General agent tasks", ["long-horizon", "professional work", "verifiable"]),
    "terminal-bench-science-0-1": ("Agent", "Science / research", ["scientific workflows", "terminal", "continuous benchmark"]),
    "terminalworld-verified": ("Agent", "Terminal / OS", ["real-world workflows", "verified subset", "terminal"]),
    "terminal-bench-2-1": ("Agent", "Terminal / OS", ["container", "reproducible", "revision"]),
    "terminal-bench-4-0": ("Agent", "Terminal / OS", ["container", "command line", "versioned"]),
    "humanitys-last-exam": ("Model", "General knowledge & reasoning", ["academic", "multimodal", "expert"]),
    "cursorbench-3-2": ("Agent", "Software engineering", ["multi-file", "coding", "tool use"]),
    "gdpval-aa-v2": ("Agent", "General agent tasks", ["professional work", "Elo", "agentic"]),
    "automationbench": ("Agent", "General agent tasks", ["business workflows", "API", "end-state grading"]),
    "screenspot-pro": ("Model", "Multimodal", ["GUI grounding", "high resolution", "static screenshot"]),
}

for _spec in BENCHMARKS:
    try:
        _spec["evaluation_type"], _spec["domain"], _spec["tags"] = TAXONOMY[_spec["id"]]
    except KeyError as error:
        raise ValueError(f"No curated taxonomy entry for benchmark {_spec['id']}") from error
    _spec.setdefault("metric_id", f"{_spec['id']}-metric-v1")
    _spec.setdefault("protocol_id", f"{_spec['id']}-source-export-v1")
    _spec.setdefault("protocol", "Source export protocol; row-level protocol details are preserved when available.")


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def register_resource(resources, url, title, *, resource_type="other", publisher=None,
                      authority="trusted_secondary", scope=("benchmark", "model"),
                      notes=None):
    resource_id = f"resource-{slug(url)}"
    resources.setdefault(resource_id, {
        "id": resource_id,
        "resource_scope": list(scope),
        "entity_id": None,
        "resource_type": resource_type,
        "title": title,
        "url": url,
        "publisher": publisher,
        "authority": authority,
        "active": True,
        "watch": False,
        "last_checked_at": None,
        "notes": notes,
    })
    return resource_id


def model_family(model, organization):
    return slug(f"{organization}-{re.sub(r'\\s*\\([^)]*\\)', '', model)}")


def model_release_resource(resources, model):
    normalized = slug(model)
    for key, spec in MODEL_RELEASE_RESOURCES.items():
        if key in normalized:
            return register_resource(
                resources,
                spec["url"],
                spec["title"],
                resource_type=spec["resource_type"],
                publisher=spec["publisher"],
                authority="primary",
                scope=("model",),
                notes="Official release/model resource for the current frontier model panel.",
            )
    return None


def parse_dates(row):
    evaluation_date = (row.get("Started at") or "")[:10] or None
    model_release_date = row.get("Release date") or None
    return evaluation_date, model_release_date


def build_frontier(rows, date_field, date_meaning):
    """Build a deterministic, step-function frontier from canonical observations.

    Observations sharing a date are evaluated as one cohort. The winning
    observation retains the lineage of the score that established the event;
    the cohort IDs document the other observations considered at that date.
    """
    cohorts = {}
    for row in rows:
        event_date = row.get(date_field)
        if event_date:
            cohorts.setdefault(event_date, []).append(row)
    frontier = []
    best_score = None
    for event_date in sorted(cohorts):
        cohort = sorted(cohorts[event_date], key=lambda item: (item["score"], item["observation_id"]))
        winner = cohort[-1]
        if best_score is None or winner["score"] > best_score:
            event = {**winner}
            event["plot_date"] = event_date
            event["date"] = event_date
            event["date_kind"] = date_meaning
            event["frontier_observation_ids"] = [item["observation_id"] for item in cohort]
            frontier.append(event)
            best_score = winner["score"]
    return frontier


def threshold_metrics(frontier, release, floor, ceiling, as_of=None):
    result = {}
    if floor is None or ceiling is None or ceiling == floor:
        for label in ("T50", "T80", "T90"):
            result[label] = {"status": "not_applicable", "reason": "No defensible fixed floor and ceiling."}
        return result
    censor_date = as_of or (date.fromisoformat(frontier[-1]["plot_date"]) if frontier else release)
    for label, target in (("T50", 0.5), ("T80", 0.8), ("T90", 0.9)):
        crossing = next((point for point in frontier if (point["score"] - floor) / (ceiling - floor) >= target), None)
        if crossing:
            days = (date.fromisoformat(crossing["plot_date"]) - release).days
            result[label] = {"status": "at_release", "days": 0, "qualifying_model_release_date": crossing["plot_date"]} if days <= 0 else {"status": "reached", "days": days}
        elif frontier:
            result[label] = {"status": "right_censored", "days": max(0, (censor_date - release).days)}
        else:
            result[label] = {"status": "unknown", "reason": "No dated observations are available on this timeline."}
    finite = {label: item["days"] for label, item in result.items()
              if item.get("status") in {"at_release", "reached"}}
    for lower, higher in (("T50", "T80"), ("T80", "T90"), ("T50", "T90")):
        if lower in finite and higher in finite and finite[higher] < finite[lower]:
            raise ValueError(f"Threshold ordering violated: {higher}={finite[higher]} < {lower}={finite[lower]}")
    return result


def frontier_velocity(frontier, window_days=180):
    if len(frontier) < 2:
        return None
    latest = frontier[-1]
    latest_date = date.fromisoformat(latest["plot_date"])
    prior = next((point for point in reversed(frontier[:-1])
                  if (latest_date - date.fromisoformat(point["plot_date"])).days >= window_days), None)
    if not prior:
        return None
    elapsed = (latest_date - date.fromisoformat(prior["plot_date"])).days
    return (latest["score"] - prior["score"]) / elapsed * 30.44


def build_benchmark(spec, resources, models):
    benchmark_resource_id = register_resource(
        resources, spec["source"], f"{spec['name']} primary source", resource_type="paper",
        publisher="Benchmark authors", authority="primary", scope=("benchmark",),
    )
    rows = []
    with (RAW / spec["file"]).open(newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                score = float(row[spec["score"]]) * spec.get("score_multiplier", 1.0)
            except (KeyError, TypeError, ValueError):
                continue
            evaluation_date, model_release_date = parse_dates(row)
            model = row.get("Name") or row.get("Model version") or "Unknown model"
            source_url = row.get("Source link") or row.get("Source Link") or row.get("Source URL") or row.get("Logs") or row.get("Source") or spec["source"]
            source_is_benchmark_primary = source_url == spec["source"]
            source_id = register_resource(
                resources, source_url,
                row.get("Source") or ("Epoch evaluation log" if row.get("Logs") else f"{spec['name']} source"),
                resource_type="evaluation_log" if row.get("Logs") else "official_leaderboard",
                publisher="Epoch AI" if row.get("Logs") else row.get("Source"),
                authority="primary" if source_is_benchmark_primary else "trusted_secondary",
                scope=("benchmark", "model"),
                notes="Shared evidence resource; the export does not provide a model-specific source record."
                if not row.get("Source link") and not row.get("Logs") else None,
            )
            model_id = f"model-{slug(model)}"
            family_id = model_family(model, row.get("Organization") or "unknown")
            release_resource_id = model_release_resource(resources, model)
            is_math_retro = spec["id"] == "math-level-5"
            retrospective = is_math_retro or bool(
                evaluation_date and model_release_date and evaluation_date > model_release_date
            )
            models.setdefault(model_id, {
                "id": model_id,
                "canonical_name": model,
                "family_id": family_id,
                "release_date": model_release_date,
                "organization": row.get("Organization") or "Unknown",
                "resource_ids": [source_id] + ([release_resource_id] if release_resource_id else []),
                "roles": ["contemporary_frontier"],
                "domains": [spec["domain"]],
                "evaluation_types": [spec["evaluation_type"]],
                "inclusion_reason": "Included as a representative observation in the curated pilot dataset.",
                "provenance_note": "The current export provides evaluation evidence but not a model-specific official resource.",
            })
            rows.append({
                "observation_id": f"obs-{spec['id']}-{row.get('id') or slug(model)}",
                "benchmark_id": spec["id"],
                "benchmark_version_id": f"{spec['id']}-canonical",
                "model_id": model_id,
                "model_family_id": family_id,
                "model": model,
                "organization": row.get("Organization") or "Unknown",
                "score": score,
                "reported_cost_per_task": row.get(spec.get("cost_column", "")) if spec.get("cost_column") else None,
                "metric_id": spec["metric_id"],
                "protocol_id": spec["protocol_id"],
                "metric": spec["score"],
                "evaluation_protocol": spec["protocol"],
                "model_release_date": model_release_date,
                "evaluation_date": evaluation_date,
                "result_public_date": None,
                "source_publication_date": None,
                "ingested_at": datetime.now().date().isoformat(),
                "date_precision": "day" if evaluation_date or model_release_date else None,
                "date_notes": "Result-public date is not present in the source export.",
                "date": evaluation_date or model_release_date,
                "date_kind": "evaluation_date" if evaluation_date else "unknown",
                "capability_date": model_release_date,
                "capability_date_meaning": "model_release_date",
                "reported_date_meaning": "result_public_date",
                "historical_frontier_date": None,
                "temporal_class": "retrospective_evaluation" if retrospective else "historical_or_unknown",
                "retrospective": retrospective,
                "capability_frontier_eligible": bool(model_release_date),
                "historical_frontier_eligible": False,
                "eligibility_reason": "Capability eligibility uses the model release date and the curated protocol; reported-result eligibility requires result_public_date.",
                "contemporaneous": not retrospective,
                "source_ids": ([source_id, benchmark_resource_id] if source_id != benchmark_resource_id else [source_id]) + ([release_resource_id] if release_resource_id else []),
                "source": source_url,
                "notes": "Operational evaluation timeline only; not a historical public-result date.",
            })
    capability_frontier = build_frontier(rows, "capability_date", "model release date")
    reported_frontier = build_frontier(
        [row for row in rows if row.get("result_public_date")],
        "result_public_date",
        "result first-public date",
    )
    current = capability_frontier[-1] if capability_frontier else None
    reported_current = reported_frontier[-1] if reported_frontier else None
    progress = None
    if current and spec["ceiling"] != spec["floor"]:
        progress = (current["score"] - spec["floor"]) / (spec["ceiling"] - spec["floor"])
        progress = max(0.0, min(1.0, progress))
    release = date.fromisoformat(spec["release"])
    snapshot_date = date.today()
    threshold_days = threshold_metrics(capability_frontier, release, spec["floor"], spec["ceiling"], snapshot_date)
    reported_threshold_days = threshold_metrics(reported_frontier, release, spec["floor"], spec["ceiling"], snapshot_date)
    velocity_180d = frontier_velocity(capability_frontier)
    reported_velocity_180d = frontier_velocity(reported_frontier)
    cost_values = []
    if spec.get("cost_column"):
        for row in rows:
            try:
                cost = float(row.get("reported_cost_per_task", ""))
            except (TypeError, ValueError):
                continue
            if cost >= 0:
                cost_values.append(cost)
    cost = None
    if cost_values:
        divisor = spec.get("cost_divisor", 1)
        method = "median of reported per-task values in the curated export"
        if divisor != 1:
            method = f"median of reported full-run costs divided by the documented {divisor}-task benchmark size"
        cost = {"value": sorted(cost_values)[len(cost_values) // 2] / divisor, "currency": "USD", "per_task": True, "method": method, "source_ids": sorted({source_id for row in rows for source_id in row["source_ids"]}), "notes": "Cost varies by model, harness, and inference settings."}
    organizations = {row["organization"] for row in rows}
    coverage_orgs = sorted(organizations & REFERENCE_ORGANIZATIONS)
    coverage = len(coverage_orgs) / len(REFERENCE_ORGANIZATIONS)
    return {
        **{key: spec[key] for key in ("id", "name", "domain", "release", "floor", "ceiling", "source")},
        "evaluation_type": spec["evaluation_type"],
        "tags": spec["tags"],
        "metric": spec["score"],
        "score_format": spec.get("score_format", "ratio"),
        "metric_id": spec["metric_id"],
        "protocol_id": spec["protocol_id"],
        "benchmark_version_id": f"{spec['id']}-canonical",
        "summary": spec["summary"],
        "task_format": spec["task_format"],
        "scoring": spec["scoring"],
        "evaluation_target": spec["evaluation_target"],
        "observation_count": len(rows),
        "observations": rows,
        "frontier": [{**point, "source_ids": point["source_ids"]} for point in capability_frontier],
        "frontier_events": [{**point, "source_ids": point["source_ids"]} for point in capability_frontier],
        "capability_frontier": [{**point, "source_ids": point["source_ids"]} for point in capability_frontier],
        "reported_frontier": [{**point, "source_ids": point["source_ids"]} for point in reported_frontier],
        "historical_frontier": [{**point, "source_ids": point["source_ids"]} for point in reported_frontier],
        "retrospective_observations": [row for row in rows if row["retrospective"]],
        "observed_frontier": current["score"] if current else None,
        "capability_frontier_value": current["score"] if current else None,
        "reported_frontier_value": reported_current["score"] if reported_current else None,
        "current_frontier": current["score"] if current else None,
        "normalized_progress": progress,
        "normalized_headroom": None if progress is None else 1 - progress,
        "threshold_days": threshold_days,
        "capability_threshold_days": threshold_days,
        "reported_threshold_days": reported_threshold_days,
        "velocity_180d": velocity_180d,
        "capability_velocity_180d": velocity_180d,
        "reported_velocity_180d": reported_velocity_180d,
        "cost_per_task": cost,
        "coverage": {"value": coverage, "represented_organizations": coverage_orgs, "panel_size": len(REFERENCE_ORGANIZATIONS), "status": "high" if coverage >= 0.7 else "medium" if coverage >= 0.4 else "low"},
        "unavailable": ["T80: not included in the first vertical slice"],
        "resource_ids": [benchmark_resource_id],
        "date_policy": "Primary capability lifecycle metrics use model_release_date on protocol-compatible curated observations. Evaluation and result-public dates are preserved for provenance; they are not silently substituted into the capability timeline.",
        "historical_frontier_status": "unknown_public_dates" if not reported_frontier else "available",
        "timeline_default": "capability",
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    resources, models = {}, {}
    benchmarks = [build_benchmark(spec, resources, models) for spec in BENCHMARKS]
    for panel_model in REFERENCE_MODEL_RELEASES:
        release_resource_id = model_release_resource(resources, panel_model["canonical_name"])
        models.setdefault(panel_model["id"], {
            "id": panel_model["id"],
            "canonical_name": panel_model["canonical_name"],
            "family_id": panel_model["family_id"],
            "release_date": panel_model["release_date"],
            "organization": panel_model["organization"],
            "resource_ids": [release_resource_id] if release_resource_id else [],
            "roles": [panel_model["role"]],
            "domains": [panel_model["domain"]],
            "evaluation_types": ["Model"],
            "inclusion_reason": "Included as a current frontier reference-panel release anchor; benchmark scores are added only when authoritative results are available.",
            "provenance_note": "Official release/model resource is preserved even when no score is yet available in the curated benchmark set.",
        })
    payload = {
        "snapshot_id": datetime.now().strftime("%Y-%m-%d"),
        "source": "Curated benchmark exports; see resource registry for source lineage",
        "resources": sorted(resources.values(), key=lambda item: item["id"]),
        "models": sorted(models.values(), key=lambda item: item["id"]),
        "benchmarks": benchmarks,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    RESOURCE_OUT.write_text(json.dumps(payload["resources"], indent=2) + "\n")
    MODEL_OUT.write_text(json.dumps(payload["models"], indent=2) + "\n")
    observations = [observation for benchmark in benchmarks for observation in benchmark["observations"]]
    OBSERVATION_OUT.write_text("".join(json.dumps(observation, sort_keys=True) + "\n" for observation in observations))
    print(f"Wrote {OUT} ({len(payload['benchmarks'])} benchmarks)")


if __name__ == "__main__":
    main()
