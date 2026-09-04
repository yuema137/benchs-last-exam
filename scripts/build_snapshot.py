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
    {"id": "ifeval", "name": "IFEval", "domain": "Instruction following", "file": "ifeval_external.csv", "score": "Score", "release": "2023-11-14", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2311.07911", "summary": {"en": "IFEval tests whether a language model follows concrete, automatically checkable instructions in a prompt.", "zh": "IFEval 测试语言模型能不能遵守 prompt 里具体、可以自动检查的指令。"}, "task_format": {"en": "Each prompt includes one or more constraints, such as an exact format, word limit, or required phrase. The model writes a response that must satisfy those constraints.", "zh": "每个 prompt 都带有一个或多个约束，比如固定格式、字数限制或必须出现某个短语。模型需要写出满足这些约束的回答。"}, "scoring": {"metric_name": "Prompt-level accuracy", "explanation": {"en": "A prompt is counted as correct only when the response satisfies all of its verifiable instructions. The score is the fraction of prompts fully satisfied.", "zh": "只有当回答满足一道 prompt 的全部可验证指令时，这道题才算正确。分数就是完整满足的 prompt 占全部 prompt 的比例。"}}, "evaluation_target": "final_output", "protocol": "IFEval English prompt-level accuracy; the stricter prompt-level metric is kept separate from instruction-level accuracy and from multilingual variants."},
    {"id": "healthbench", "name": "HealthBench", "domain": "Health", "file": "healthbench_external.csv", "score": "Score", "release": "2025-05-12", "floor": 0.0, "ceiling": 1.0, "source": "https://openai.com/index/healthbench/", "summary": {"en": "HealthBench tests whether models give useful and safe answers in realistic health conversations judged against physician-written criteria.", "zh": "HealthBench 测试模型能不能在真实健康对话中给出有用、安全的回答，并按照医生写的标准进行评分。"}, "task_format": {"en": "The model receives a multi-turn conversation between a person and a health assistant, then writes the best response to the user's last message.", "zh": "模型会收到一段用户和 health assistant 的多轮对话，然后回答用户最后一条消息。"}, "scoring": {"metric_name": "Physician-rubric score", "explanation": {"en": "A model-based grader checks physician-written criteria for each conversation. The score is the weighted proportion of criteria the response satisfies.", "zh": "model-based grader 会检查每段对话对应的医生标准。分数是回答满足这些标准的加权比例。"}}, "evaluation_target": "process_and_output", "protocol": "HealthBench overall score; HealthBench Consensus and HealthBench Hard are separate variants and are not merged."},
    {"id": "browsecomp", "name": "BrowseComp", "domain": "General agent tasks", "file": "browsecomp_external.csv", "score": "Score", "release": "2025-04-10", "floor": 0.0, "ceiling": 1.0, "source": "https://openai.com/index/browsecomp/", "summary": {"en": "BrowseComp tests whether a browsing agent can find hard-to-locate facts that require persistent, multi-step web research.", "zh": "BrowseComp 测试 browsing agent 能不能通过持续、多步的网页研究找到很难定位的事实。"}, "task_format": {"en": "The agent receives a short fact-seeking question and must search the web, combine evidence, and submit a concise answer.", "zh": "agent 会收到一个简短的事实问题，需要搜索网页、组合证据，再提交简短答案。"}, "scoring": {"metric_name": "Answer accuracy", "explanation": {"en": "A response is correct when it matches the reference answer under the benchmark grader. The score is the fraction of the 1,266 questions answered correctly.", "zh": "按照 benchmark grader 的规则，答案和标准答案匹配才算正确。分数就是答对 1,266 道题的比例。"}}, "evaluation_target": "environment_outcome", "protocol": "BrowseComp official 1,266-task benchmark; browsing availability and agent scaffold remain part of each observation's setup."},
    {"id": "longbench-v2", "name": "LongBench v2", "domain": "Long context", "file": "longbench_v2_external.csv", "score": "Score", "release": "2024-12-26", "floor": 0.0, "ceiling": 1.0, "source": "https://github.com/EnvCommons/LongBench-v2/blob/main/README.md", "summary": {"en": "LongBench v2 tests deep reasoning over long documents, from roughly 8K to 2M words, across several task domains.", "zh": "LongBench v2 测试模型对超长文档的理解和推理能力，文档长度大约从 8K 到 2M words，覆盖多个 task domain。"}, "task_format": {"en": "The model receives a long document and a multiple-choice question, then submits one of four answer choices. The fixed test split has 503 tasks.", "zh": "模型会收到一篇长文档和一道选择题，然后提交四个选项中的一个。固定 test split 有 503 个 task。"}, "scoring": {"metric_name": "Exact-match accuracy", "explanation": {"en": "A task is correct when the submitted A/B/C/D choice exactly matches the reference answer. The score is the fraction of the 503 tasks solved.", "zh": "提交的 A/B/C/D 选项和标准答案完全一致时，这个 task 才算答对。分数就是答对 503 个 task 的比例。"}}, "evaluation_target": "final_output", "protocol": "LongBench-v2 fixed 503-task test split; zero-shot multiple-choice accuracy. It is kept separate from the original LongBench object."},
    {"id": "video-mme", "name": "Video-MME", "domain": "Multimodal", "file": "video_mme_external.csv", "score": "Overall (no subtitles)", "release": "2024-06-03", "floor": 0.0, "ceiling": 1.0, "source": "https://video-mme.github.io/home_page.html", "summary": {"en": "Video-MME tests multimodal models on questions about short, medium, and long videos across diverse visual domains.", "zh": "Video-MME 测试 multimodal model 理解短、中、长视频的能力，覆盖多个视觉领域。"}, "task_format": {"en": "Each item provides a video and a multiple-choice question. The model answers questions that may require visual, audio, subtitle, and temporal understanding; this card uses the no-subtitles overall score.", "zh": "每个 task 会提供一段视频和一道选择题。模型需要结合视觉、音频、字幕和时间信息回答问题；本卡使用 no-subtitles overall score。"}, "scoring": {"metric_name": "Overall accuracy without subtitles", "explanation": {"en": "The score is the fraction of video questions answered correctly under the official no-subtitles setting. Subtitle and duration-specific scores are separate metrics.", "zh": "分数是在官方 no-subtitles 设置下答对视频问题的比例。带字幕和不同视频时长的分数属于其他独立 metric。"}}, "evaluation_target": "final_output", "protocol": "Video-MME original benchmark, overall no-subtitles score; Video-MME-v2 is a separate benchmark object."},
    {"id": "mathvista", "name": "MathVista", "domain": "Multimodal", "file": "mathvista_external.csv", "score": "Score", "release": "2023-10-03", "floor": 0.0, "ceiling": 1.0, "source": "https://mathvista.github.io/", "summary": {"en": "MathVista tests mathematical reasoning in visual contexts, combining charts, diagrams, geometry, and other visual materials with math questions.", "zh": "MathVista 测试模型在视觉材料中进行数学推理的能力，题目包含图表、示意图、几何图形等内容。"}, "task_format": {"en": "The model receives an image or visual context and a mathematics question, then produces an answer under the benchmark's answer protocol.", "zh": "模型会收到图片或其他视觉材料以及一道数学问题，然后按照 benchmark 的 answer protocol 给出答案。"}, "scoring": {"metric_name": "Answer accuracy", "explanation": {"en": "A response counts as correct when it matches the reference answer under the MathVista evaluator. The score is the fraction of visual-math questions answered correctly.", "zh": "按照 MathVista evaluator 的规则，答案和标准答案匹配时算正确。分数就是答对视觉数学题的比例。"}}, "evaluation_target": "final_output", "protocol": "MathVista official project-page score series; test/testmini and materially different subsets are not silently merged."},
    {"id": "mmlu-pro", "name": "MMLU-Pro", "domain": "General knowledge & reasoning", "file": "mmlu_pro_external.csv", "score": "Average Accuracy", "release": "2024-06-03", "floor": 0.1, "ceiling": 1.0, "source": "https://arxiv.org/abs/2406.01574", "summary": {"en": "MMLU-Pro is a harder, reasoning-focused successor to MMLU across academic and professional subjects.", "zh": "MMLU-Pro 是 MMLU 的 harder successor，覆盖多个学术和专业领域，更强调 reasoning。"}, "task_format": {"en": "Each item is a ten-choice multiple-choice question. The model selects one answer, usually after producing a reasoning trace under the chosen prompt.", "zh": "每个 task 都是十选一问题。模型需要选出一个答案，通常会按照指定 prompt 先进行 reasoning。"}, "scoring": {"metric_name": "Overall accuracy", "explanation": {"en": "The score is the fraction of questions for which the selected answer is correct. The benchmark has ten choices per question, so 10% is the random-choice reference point.", "zh": "分数就是选项正确的题目占全部题目的比例。每题有十个选项，所以 10% 是随机选择的参考 floor。"}}, "evaluation_target": "final_output", "protocol": "MMLU-Pro official repository mini-leaderboard overall accuracy; prompt and CoT settings remain source context and are not merged when materially different."},
    {"id": "simpleqa-verified", "name": "SimpleQA Verified", "domain": "General knowledge & reasoning", "file": "simpleqa_verified.csv", "score": "Best score (across scorers)", "release": "2025-09-09", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2509.07968", "summary": {"en": "SimpleQA Verified tests whether a model can answer short, fact-seeking questions with reliable, verifiable answers.", "zh": "SimpleQA Verified 测试模型能不能回答简短、事实导向且可以核验的问题。"}, "task_format": {"en": "Each item is a short fact-seeking question with a single target answer. The model produces a concise answer without browsing.", "zh": "每个 task 都是一道简短的事实问题，有一个目标答案。模型需要在不浏览网页的情况下给出简洁回答。"}, "scoring": {"metric_name": "Graded factuality accuracy", "explanation": {"en": "A grader labels the answer correct, incorrect, or not attempted. The reported score is the benchmark's graded accuracy under the fixed evaluation protocol.", "zh": "grader 会把答案标为正确、错误或未作答。报告分数是在固定评测 protocol 下的 factuality accuracy。"}}, "evaluation_target": "final_output", "protocol": "SimpleQA Verified fixed 1,000-question protocol; scores from the curated standardized evaluation export are kept together and are not merged with the original 4,326-question SimpleQA object."},
    {"id": "frontiermath-tiers-1-3-v2", "name": "FrontierMath Tiers 1–3 (v2)", "domain": "Mathematics", "file": "frontiermath_tiers_1_3_v2.csv", "score": "Best score (across scorers)", "release": "2026-06-12", "floor": 0.0, "ceiling": 1.0, "source": "https://epoch.ai/benchmarks/frontiermath-tiers-1-3", "summary": {"en": "FrontierMath Tiers 1–3 tests advanced mathematics problems written by experts and checked by executable verifiers.", "zh": "FrontierMath Tiers 1–3 测试专家编写、由可执行 verifier 检查的高难度数学题。"}, "task_format": {"en": "The model writes a Python answer function for each mathematics problem and can use an isolated Python tool while solving.", "zh": "模型需要为每道数学题编写 Python answer function，解题时可以使用隔离的 Python 工具。"}, "scoring": {"metric_name": "Verified task accuracy", "explanation": {"en": "A task counts as correct when the submitted answer passes the benchmark's verifier. The score is the fraction of verified tasks solved.", "zh": "提交的答案通过 benchmark verifier，这道题才算正确。分数就是通过验证的 task 占全部 task 的比例。"}}, "evaluation_target": "final_output"},
    {"id": "arc-agi-2", "name": "ARC-AGI-2", "domain": "Abstract / novel reasoning", "file": "arc_agi_2_external.csv", "score": "Score", "release": "2025-03-24", "floor": 0.0, "ceiling": 1.0, "source": "https://arcprize.org/blog/announcing-arc-agi-2-and-arc-prize-2025", "summary": {"en": "ARC-AGI-2 tests whether a system can infer abstract transformations from a few visual examples and generalize them to new grids.", "zh": "ARC-AGI-2 测试系统能否从少量视觉示例中推断抽象变换，并把规则泛化到新的网格。"}, "task_format": {"en": "Each task shows example input-output grids. The system must produce exactly two candidate outputs for the test input.", "zh": "每个 task 会给出输入和输出网格示例，系统需要为测试输入生成恰好两个候选输出。"}, "scoring": {"metric_name": "Pass@2 task accuracy", "explanation": {"en": "A task is correct when either of the two submitted outputs exactly matches the ground truth. The final score is the fraction of tasks solved this way.", "zh": "如果提交的两个输出中有一个和标准答案完全一致，这道题就算答对。最终分数是答对 task 的比例。"}}, "evaluation_target": "final_output"},
    {"id": "aider-polyglot", "name": "Aider Polyglot", "domain": "Coding / software engineering", "file": "aider_polyglot_external.csv", "score": "Percent correct", "score_multiplier": 0.01, "release": "2024-12-21", "floor": 0.0, "ceiling": 1.0, "source": "https://aider.chat/2024/12/21/polyglot.html", "summary": {"en": "Aider Polyglot tests whether a model can edit code correctly across six programming languages.", "zh": "Aider Polyglot 测试模型能不能在六种编程语言中正确修改代码。"}, "task_format": {"en": "The model receives an Exercism coding exercise and must make the requested repository edit using Aider's editing format.", "zh": "模型会收到一个 Exercism 编程题，需要用 Aider 要求的编辑格式修改代码仓库。"}, "scoring": {"metric_name": "Correct edit rate", "explanation": {"en": "A task counts as correct when the resulting code passes the benchmark checks. The score is the percentage of exercises completed correctly.", "zh": "修改后的代码通过 benchmark 检查，这道题才算正确。分数就是正确完成 exercise 的比例。"}}, "evaluation_target": "environment_outcome"},
    {"id": "osworld-2", "name": "OSWorld 2.0", "domain": "Agents / computer use", "file": "osworld_2_external.csv", "score": "Partial score", "release": "2026-06-26", "floor": 0.0, "ceiling": 1.0, "source": "https://os-world.github.io/", "summary": {"en": "OSWorld 2.0 tests whether a computer-use agent can complete tasks in real desktop and web applications.", "zh": "OSWorld 2.0 测试 computer-use agent 能不能在真实桌面和网页应用中完成任务。"}, "task_format": {"en": "The agent operates a computer through tools under a task and step budget, then receives credit for completing the requested outcome.", "zh": "agent 通过工具操作电脑，在规定的 task 和步数预算内完成目标，最后根据结果计分。"}, "scoring": {"metric_name": "Partial task score", "explanation": {"en": "The benchmark assigns partial credit for progress toward the requested computer-use outcome. The score is the average partial credit across tasks; it is distinct from binary task success.", "zh": "benchmark 会根据 computer-use task 的完成进度给部分分数。最终分数是所有 task 的平均 partial credit，和 binary task success 不是同一个指标。"}}, "evaluation_target": "environment_outcome", "protocol": "OSWorld 2.0 partial-score series. The source export's Partial score is used; binary accuracy is preserved in the raw CSV but is not mixed into this headline frontier."},
    {"id": "terminal-bench-2", "name": "Terminal-Bench 2.0", "domain": "Agents / computer use", "file": "terminalbench_external.csv", "score": "Accuracy mean", "release": "2025-11-07", "floor": 0.0, "ceiling": 1.0, "source": "https://www.tbench.ai/news/announcement-2-0", "summary": {"en": "Terminal-Bench 2.0 tests whether agents can solve realistic tasks inside terminal environments.", "zh": "Terminal-Bench 2.0 测试 agent 能不能在 terminal 环境中完成真实的软件和系统任务。"}, "task_format": {"en": "The agent receives a task in a containerized terminal environment and can use shell tools before submitting the final environment state.", "zh": "agent 会在容器化 terminal 环境中收到 task，可以使用 shell 工具，最后提交环境状态。"}, "scoring": {"metric_name": "Task success rate", "explanation": {"en": "A task counts as solved when its evaluator accepts the resulting environment or artifact. The score is the fraction of tasks solved.", "zh": "如果 evaluator 接受最终环境状态或产物，这个 task 就算解决。分数是解决 task 的比例。"}}, "evaluation_target": "environment_outcome"},
])

# High-signal additions backed by curated raw exports.  These are deliberately
# partial-core records: missing lifecycle thresholds or cost remain explicit in
# the generated snapshot instead of blocking an important benchmark entirely.
BENCHMARKS.extend([
    {"id": "big-bench-hard", "name": "BIG-Bench Hard", "domain": "General knowledge & reasoning", "file": "bbh_external.csv", "score": "Average", "release": "2022-10-17", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2210.09261", "summary": {"en": "BIG-Bench Hard tests difficult reasoning patterns across 23 tasks that are challenging for language models.", "zh": "BIG-Bench Hard 测试 23 类对语言模型更难的推理任务，覆盖多种需要组合思考的题型。"}, "task_format": {"en": "The model receives a short text prompt and produces an answer for one of 23 task types, such as logical reasoning, tracking, or classification.", "zh": "模型会收到简短的文字 prompt，并完成 23 类 task 中的一类，例如逻辑推理、状态跟踪或分类。"}, "scoring": {"metric_name": "Task accuracy", "explanation": {"en": "Each task is scored against its reference answer. The headline score averages accuracy across the 23 tasks.", "zh": "每道 task 都和标准答案比较。headline score 是 23 类 task accuracy 的平均值。"}}, "evaluation_target": "final_output"},
    {"id": "scienceqa", "name": "ScienceQA", "domain": "Science", "file": "science_qa_external.csv", "score": "Score", "release": "2022-09-19", "floor": 0.0, "ceiling": 1.0, "source": "https://scienceqa.github.io/", "summary": {"en": "ScienceQA tests multimodal science question answering with text, diagrams, and explanations.", "zh": "ScienceQA 测试模型结合文字、图表等材料回答科学问题的能力。"}, "task_format": {"en": "Each item is a multiple-choice science question with a short context that may include an image or diagram. The model selects an answer.", "zh": "每道题都是科学选择题，题目可能附带图片或示意图。模型需要选出答案。"}, "scoring": {"metric_name": "Multiple-choice accuracy", "explanation": {"en": "The score is the fraction of questions for which the selected option matches the reference answer.", "zh": "分数就是模型选项和标准答案一致的题目占全部题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "hellaswag", "name": "HellaSwag", "domain": "General knowledge & reasoning", "file": "hella_swag_external.csv", "score": "Overall accuracy", "release": "2019-05-20", "floor": 0.25, "ceiling": 1.0, "source": "https://arxiv.org/abs/1905.07830", "summary": {"en": "HellaSwag tests whether a model can choose the most plausible continuation of an everyday situation.", "zh": "HellaSwag 测试模型能不能从日常场景的多个选项中选出最合理的后续情节。"}, "task_format": {"en": "The model reads a short situation and chooses one continuation from several candidates.", "zh": "模型会读到一段简短场景，并从多个候选后续中选出一个。"}, "scoring": {"metric_name": "Accuracy", "explanation": {"en": "A question is correct when the selected continuation matches the human-written reference. The score is the percentage correct.", "zh": "选择的后续和人工标准答案一致时算答对。分数就是答对题目的百分比。"}}, "evaluation_target": "final_output"},
    {"id": "piqa", "name": "PIQA", "domain": "General knowledge & reasoning", "file": "piqa_external.csv", "score": "Score", "release": "2019-11-26", "floor": 0.5, "ceiling": 1.0, "source": "https://arxiv.org/abs/1911.11641", "summary": {"en": "PIQA tests physical commonsense: choosing which of two solutions is more likely to work in the real world.", "zh": "PIQA 测试物理常识：模型需要判断两个解决办法中哪个更可能在现实世界有效。"}, "task_format": {"en": "Each item describes a goal and offers two possible solutions. The model chooses the more plausible one.", "zh": "每道题会描述一个目标，并给出两个解决办法。模型需要选择更合理的一个。"}, "scoring": {"metric_name": "Binary accuracy", "explanation": {"en": "The score is the fraction of physical commonsense questions answered correctly.", "zh": "分数就是物理常识题答对的比例。"}}, "evaluation_target": "final_output"},
    {"id": "triviaqa", "name": "TriviaQA", "domain": "General knowledge & reasoning", "file": "trivia_qa_external.csv", "score": "EM", "release": "2017-05-09", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/1705.03551", "summary": {"en": "TriviaQA tests open-domain question answering against noisy evidence from the web and documents.", "zh": "TriviaQA 测试模型根据开放领域问题和网页、文档证据回答事实问题的能力。"}, "task_format": {"en": "The model receives a question and may use an associated evidence document to produce a short answer.", "zh": "模型会收到问题以及相关证据文档，并需要给出简短答案。"}, "scoring": {"metric_name": "Exact match", "explanation": {"en": "Exact match counts an answer when its normalized text matches an accepted reference answer.", "zh": "经过规范化后，答案文字和可接受的标准答案一致时算 exact match。"}}, "evaluation_target": "final_output"},
    {"id": "superglue", "name": "SuperGLUE", "domain": "General knowledge & reasoning", "file": "superglue_external.csv", "score": "Score", "release": "2019-05-01", "floor": 0.0, "ceiling": 1.0, "source": "https://super.gluebenchmark.com/", "summary": {"en": "SuperGLUE tests language understanding across several difficult reading, reasoning, and linguistic tasks.", "zh": "SuperGLUE 测试模型在阅读理解、推理和语言学等多类任务上的语言理解能力。"}, "task_format": {"en": "The suite contains several task formats, including classification, entailment, and question answering. The model produces the required answer for each task.", "zh": "这个 suite 包含分类、蕴含判断和问答等多种 task format，模型需要按每类 task 的要求作答。"}, "scoring": {"metric_name": "Aggregate task score", "explanation": {"en": "Each task uses its official metric, and the headline score aggregates the task scores according to the benchmark protocol.", "zh": "每类 task 使用自己的官方 metric，headline score 按 benchmark protocol 汇总各项 task score。"}}, "evaluation_target": "final_output"},
    {"id": "cybench", "name": "CyBench", "domain": "Cybersecurity", "file": "cybench_external.csv", "score": "Unguided % Solved", "score_multiplier": 0.01, "release": "2024-08-01", "floor": 0.0, "ceiling": 1.0, "source": "https://cybench.github.io/", "summary": {"en": "CyBench tests agents on realistic cybersecurity tasks that require investigation and technical action.", "zh": "CyBench 测试 agent 完成真实网络安全任务时的调查和技术操作能力。"}, "task_format": {"en": "The agent works in a cybersecurity environment, using available tools to investigate a challenge and produce a successful solution.", "zh": "agent 会在网络安全环境中使用工具调查 challenge，并完成可验证的解决方案。"}, "scoring": {"metric_name": "Unguided task success rate", "explanation": {"en": "A task is solved when the agent completes the challenge without task-specific guidance. The score is the fraction solved.", "zh": "agent 在没有 task-specific guidance 的情况下完成 challenge 才算解决。分数是解决 task 的比例。"}}, "evaluation_target": "environment_outcome"},
    {"id": "deepresearch-bench", "name": "DeepResearch Bench", "domain": "General agent tasks", "file": "deepresearchbench_external.csv", "score": "Average score", "release": "2025-06-13", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2506.11763", "summary": {"en": "DeepResearch Bench tests research agents on expert-written questions that require web research, synthesis, and grounded reporting.", "zh": "DeepResearch Bench 测试 research agent 完成专家问题、网页检索、信息综合和有依据写作的能力。"}, "task_format": {"en": "The agent receives a research question, searches for evidence, and produces a long-form report with supporting citations.", "zh": "agent 会收到研究问题，检索证据，并提交带有引用的长篇报告。"}, "scoring": {"metric_name": "RACE/FACT aggregate score", "explanation": {"en": "The reported score combines report quality and citation-grounding evaluation under the benchmark's documented framework.", "zh": "报告分数按照 benchmark 的 framework 综合报告质量和引用 grounding 结果。"}}, "evaluation_target": "process_and_output"},
    {"id": "scicode", "name": "SciCode", "domain": "Science", "file": "scicode_external.csv", "score": "Score", "release": "2024-07-18", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2407.13168", "summary": {"en": "SciCode tests whether models can write executable code for research problems curated by scientists.", "zh": "SciCode 测试模型能不能为科学家挑选的研究问题编写可执行代码。"}, "task_format": {"en": "The model solves scientific programming subproblems and submits code that is checked against scientist-authored solutions and tests.", "zh": "模型需要解决科学编程 subproblem，提交的代码会和科学家编写的 solution 及测试进行核验。"}, "scoring": {"metric_name": "Execution-verified success rate", "explanation": {"en": "A problem is solved when the generated code produces the expected result under the benchmark tests. The score is the fraction solved.", "zh": "生成的代码通过 benchmark tests 并得到预期结果时，这道题才算解决。分数是解决题目的比例。"}}, "evaluation_target": "environment_outcome"},
    {"id": "spatialviz-bench", "name": "SpatialViz-Bench", "domain": "Multimodal", "file": "spatialviz_bench_external.csv", "score": "Overall score", "release": "2024-09-19", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2409.13253", "summary": {"en": "SpatialViz-Bench tests visual-spatial reasoning, including mental rotation, folding, penetration, and animation.", "zh": "SpatialViz-Bench 测试视觉空间推理，包括心理旋转、折叠、穿透和运动想象。"}, "task_format": {"en": "The model receives visual-spatial questions and selects or predicts the answer under the benchmark's visual reasoning protocol.", "zh": "模型会收到视觉空间问题，并按照 benchmark 的视觉推理 protocol 选择或预测答案。"}, "scoring": {"metric_name": "Overall accuracy", "explanation": {"en": "The overall score aggregates accuracy across the benchmark's four spatial reasoning subskills.", "zh": "overall score 汇总 benchmark 四类空间推理能力上的 accuracy。"}}, "evaluation_target": "final_output"},
    {"id": "vending-bench-2", "name": "Vending-Bench 2", "domain": "General agent tasks", "file": "vending_bench_2_external.csv", "score": "Score", "release": "2025-05-01", "floor": 0.0, "ceiling": 1.0, "source": "https://andonlabs.com/evals/vending-bench-2", "summary": {"en": "Vending-Bench 2 evaluates whether an agent can operate a simulated business over an extended period.", "zh": "Vending-Bench 2 评估 agent 能不能在较长时间内经营一个模拟 business。"}, "task_format": {"en": "The agent makes repeated decisions in a simulated vending-business environment and is evaluated on the resulting business outcome.", "zh": "agent 会在模拟 vending business 环境中持续做决策，最后根据 business outcome 评分。"}, "scoring": {"metric_name": "Final business outcome", "explanation": {"en": "The score reflects the final simulated business outcome under the benchmark run, rather than answer accuracy on individual questions.", "zh": "分数反映一次 benchmark run 最终的模拟 business outcome，而不是单道题的 answer accuracy。"}}, "evaluation_target": "environment_outcome"},
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
    {"id": "benchcad-vision2code", "name": "BenchCAD · Vision2Code", "domain": "Multimodal", "file": "benchcad_vision2code_external.csv", "score": "IoU-score", "release": "2026-05-11", "floor": 0.0, "ceiling": 1.0, "source": "https://benchcad.com/leaderboard", "summary": {"en": "BenchCAD Vision2Code tests whether a multimodal model can turn orthographic views of an industrial part into executable parametric CAD code.", "zh": "BenchCAD Vision2Code 测试 multimodal model 能不能把工业零件的多视图转换成可执行的参数化 CAD 代码。"}, "task_format": {"en": "The model receives four rendered views of a part and must produce a CadQuery program. The program is executed to create a solid and compared with the reference geometry.", "zh": "模型会收到一个零件的四张渲染视图，需要生成 CadQuery 程序。程序会被执行生成实体，再和标准几何结果比较。"}, "scoring": {"metric_name": "Execution-grounded IoU-score", "explanation": {"en": "The generated program is executed and scored by voxel intersection-over-union, with non-executing outputs receiving zero. The score is the average IoU-score across tasks; it is not an LLM-judge rating.", "zh": "生成的程序会被执行，并按 voxel intersection-over-union 评分；无法执行的输出得分为零。最终分数是所有 task 的平均 IoU-score，不是 LLM judge 评分。"}}, "evaluation_target": "environment_outcome", "protocol": "BenchCAD Vision2Code public leaderboard task; execution-grounded IoU-score. The curated series uses comparable non-tool IoU-score rows only; IoU · tools and other BenchCAD tasks remain separate measurements."},
    {"id": "gaia", "name": "GAIA", "domain": "General agent tasks", "file": "gaia_external.csv", "score": "Average score", "release": "2023-11-21", "floor": 0.0, "ceiling": 1.0, "source": "https://huggingface.co/spaces/gaia-benchmark/leaderboard", "summary": {"en": "GAIA tests general-purpose assistants on real-world questions that require reasoning, multimodal understanding, web browsing, and tool use.", "zh": "GAIA 测试通用 assistant 解决真实世界问题的能力，这些问题可能需要推理、多模态理解、网页浏览和工具使用。"}, "task_format": {"en": "The agent receives a real-world question, sometimes with an attached file, and must research, reason, use tools, and submit one final answer. The benchmark has three difficulty levels and separate public validation and private test sets.", "zh": "agent 会收到一个真实世界问题，有时还会附带文件，需要检索、推理、使用工具，并提交一个最终答案。benchmark 分为三个难度等级，并有公开 validation set 和答案保密的 test set。"}, "scoring": {"metric_name": "Exact-answer task success rate", "explanation": {"en": "A task is correct when the final answer matches the reference answer under the official scorer. The overall score is the fraction of tasks solved, with level-specific scores reported separately.", "zh": "按照官方 scorer，最终答案和标准答案匹配时 task 才算正确。overall score 是解决 task 占全部 task 的比例，各难度等级还会分别报告分数。"}}, "evaluation_target": "environment_outcome", "protocol": "GAIA 2023 fixed benchmark release; official leaderboard average score across levels. Public leaderboard submission dates are preserved only as evidence metadata and are not substituted for a defensible agent/system release date, so lifecycle metrics remain Unknown until such dates are curated."},
    {"id": "mcp-atlas", "name": "MCP-Atlas", "domain": "Tool use", "file": "mcp_atlas_external.csv", "score": "Pass rate", "release": "2025-10-01", "floor": 0.0, "ceiling": 1.0, "source": "https://labs.scale.com/leaderboard/mcp_atlas", "summary": {"en": "MCP-Atlas tests whether agents can discover and use real Model Context Protocol tools across multi-step workflows.", "zh": "MCP-Atlas 测试 agent 能不能在多步 workflow 中发现并正确使用真实的 Model Context Protocol 工具。"}, "task_format": {"en": "Each task exposes a controlled set of real MCP servers and distractor tools. The agent must call tools, recover from errors, and synthesize a correct final answer.", "zh": "每个 task 会提供一组受控的真实 MCP server 和干扰工具。agent 需要调用工具、处理错误，并综合出正确的最终答案。"}, "scoring": {"metric_name": "Task pass rate", "explanation": {"en": "Claims in the final answer receive 0, 0.5, or 1 credit. A task passes when mean claim coverage is at least 75%; the headline score is the percentage of passed tasks.", "zh": "最终答案中的 claims 得分为 0、0.5 或 1。当一个 task 的平均 claim coverage 至少达到 75% 时才算通过；headline score 是通过 task 的比例。"}}, "evaluation_target": "process_and_output", "protocol": "MCP-Atlas updated evaluation methodology: 1,000 tasks, 36 MCP servers, 220 tools, up to 100 tool calls per task, Gemini-2.5-Pro claim judge. Earlier MCP-Atlas series is not merged."},
    {"id": "toolathlon-verified", "name": "Toolathlon-Verified", "domain": "Tool use", "file": "toolathlon_verified_external.csv", "score": "Pass@1", "release": "2026-06-30", "floor": 0.0, "ceiling": 1.0, "source": "https://toolathlon.xyz/docs/leaderboard", "summary": {"en": "Toolathlon-Verified tests models and agents on diverse tool-use tasks that require multi-step planning and execution.", "zh": "Toolathlon-Verified 测试模型和 agent 在多种 tool-use task 中进行多步规划和执行的能力。"}, "task_format": {"en": "The system receives a task and access to a fixed set of MCP servers or local toolkits, then must complete the requested workflow through tool calls.", "zh": "系统会收到一个 task，并获得固定 MCP server 或 local toolkit 的访问权限，然后需要通过 tool calls 完成指定 workflow。"}, "scoring": {"metric_name": "Pass@1", "explanation": {"en": "Pass@1 is the share of tasks solved by the single submitted trajectory. The verified release also reports Pass@3 and Pass^3, but they are kept separate from the headline metric.", "zh": "Pass@1 是只提交一次 trajectory 时成功解决的 task 比例。verified 版本还报告 Pass@3 和 Pass^3，但这些 metric 不和 headline metric 混合。"}}, "evaluation_target": "environment_outcome", "protocol": "Toolathlon-Verified fixed release; the official page identifies it as a new score series with revised task specifications, evaluators, initial states, and infrastructure. Earlier Toolathlon results are not merged."},
])

BENCHMARKS.extend([
    {"id": "the-agent-company", "name": "TheAgentCompany", "domain": "General agent tasks", "file": "the_agent_company_external.csv", "score": "% Resolved", "release": "2024-10-01", "floor": 0.0, "ceiling": 1.0, "source": "https://the-agent-company.com/", "summary": {"en": "TheAgentCompany evaluates agents on multi-step knowledge-work tasks inside a simulated software company.", "zh": "TheAgentCompany 在模拟的软件公司环境中评估 agent 完成多步知识工作的能力。"}, "task_format": {"en": "An agent works across browser, office, communication, and coding tools to complete a workplace task; success is checked against the resulting state and deliverable.", "zh": "agent 需要跨浏览器、办公、沟通和 coding 工具完成 workplace task，结果通过最终状态和交付物检查。"}, "scoring": {"metric_name": "Task resolution rate", "explanation": {"en": "The score is the share of tasks resolved under the benchmark's task-specific checks. Partial progress is reported separately from the resolved-task rate.", "zh": "分数是按照 task 专用检查成功完成的 task 占比。部分完成进度和 resolved-task rate 分开报告。"}}, "evaluation_target": "environment_outcome", "protocol": "TheAgentCompany v1 evaluation export; OpenHands scaffold and model identity are retained in each observation. The benchmark release date is the public v1 launch month; model release dates drive the capability timeline."},
    {"id": "deepswe-v1-1", "name": "DeepSWE v1.1", "domain": "Software engineering", "file": "deepswe_external.csv", "score": "Pass@1", "release": "2026-04-01", "floor": 0.0, "ceiling": 1.0, "source": "https://deepswe.datacurve.ai/", "cost_column": "Mean cost (USD)", "summary": {"en": "DeepSWE v1.1 measures long-horizon software-engineering agents on repository-level tasks under a fixed mini-SWE-agent setup.", "zh": "DeepSWE v1.1 在固定的 mini-SWE-agent 设置下，评估 agent 完成 repository-level、长链 software-engineering task 的能力。"}, "task_format": {"en": "The agent inspects a repository, plans and edits multiple files, runs tests, and submits a patch for an issue-level task.", "zh": "agent 需要检查代码仓库、规划并修改多个文件、运行测试，然后为 issue-level task 提交 patch。"}, "scoring": {"metric_name": "Pass@1", "explanation": {"en": "Pass@1 is the fraction of repository tasks whose submitted patch is accepted by the benchmark grader in one run. Pass@4 is retained as a separate field and is not mixed into the headline metric.", "zh": "Pass@1 是一次运行中提交的 patch 被 benchmark grader 接受的 repository task 占比。Pass@4 作为独立字段保留，不和 headline metric 混合。"}}, "evaluation_target": "environment_outcome", "protocol": "DeepSWE leaderboard export; only Pass@1 rows are used for the capability frontier. Harness and reasoning effort remain part of observation provenance."},
    {"id": "frontierswe-v2", "name": "FrontierSWE V2", "domain": "Software engineering", "file": "frontierswe_v2_curated.csv", "score": "Score", "release": "2026-07-01", "floor": 0.0, "ceiling": 1.0, "source": "https://www.frontierswe.com/", "cost_column": "Average cost (USD)", "summary": {"en": "FrontierSWE V2 evaluates coding agents on difficult software tasks using separate implementation, performance, and research-quality dimensions.", "zh": "FrontierSWE V2 从 implementation、performance 和 research quality 等维度评估 agent 完成高难度软件任务的能力。"}, "task_format": {"en": "The agent works on repository-level engineering tasks and submits changes evaluated across implementation correctness, performance, and research-oriented quality criteria.", "zh": "agent 需要完成 repository-level engineering task 并提交修改，结果会从实现正确性、性能和 research quality 等维度评估。"}, "scoring": {"metric_name": "Mean@5 composite score", "explanation": {"en": "The headline score is the mean across five runs of the benchmark's composite score; the implementation, performance, and research components are preserved as supporting evidence.", "zh": "headline score 是五次运行中 composite score 的均值；implementation、performance 和 research 分项作为 supporting evidence 保留。"}}, "evaluation_target": "environment_outcome", "protocol": "FrontierSWE V2 public leaderboard export; Mean@5 rows using the proximus harness are kept together, while Best@5 and Worst@5 are not substituted for the headline metric."},
    {"id": "scienceagentbench", "name": "ScienceAgentBench", "domain": "Science / research", "file": "scienceagentbench_external.csv", "score": "Accuracy", "release": "2024-10-07", "floor": 0.0, "ceiling": 1.0, "source": "https://hal.cs.princeton.edu/scienceagentbench", "summary": {"en": "ScienceAgentBench evaluates language agents on reproducible, data-driven scientific discovery tasks sourced from peer-reviewed publications.", "zh": "ScienceAgentBench 评估 language agent 在可复现、来自同行评审论文的 data-driven scientific discovery task 上的表现。"}, "task_format": {"en": "The agent must produce a self-contained Python program that analyzes scientific data and generates the required result in a reproducible environment.", "zh": "agent 需要生成一个 self-contained Python program，在可复现环境中分析科学数据并产出要求的结果。"}, "scoring": {"metric_name": "Scientific task accuracy", "explanation": {"en": "Accuracy is the fraction of benchmark tasks for which the generated program and its executed result satisfy the task evaluator. The leaderboard also reports total API cost separately.", "zh": "Accuracy 是生成的程序及其执行结果满足 task evaluator 的 benchmark task 占比。leaderboard 还会单独报告总 API cost。"}}, "evaluation_target": "environment_outcome", "protocol": "ScienceAgentBench 102-task release with the HAL leaderboard's verified accuracy results. SAB Self-Debug and HAL Generalist Agent are retained as distinct scaffolds; no cost total is treated as per-task cost."},
    {"id": "mle-bench", "name": "MLE-bench", "domain": "Science / research", "file": "mle_bench_external.csv", "score": "All (%)", "release": "2024-10-10", "floor": 0.0, "ceiling": 1.0, "source": "https://openai.com/index/mle-bench/", "summary": {"en": "MLE-bench evaluates agents on real machine-learning engineering competitions derived from Kaggle tasks.", "zh": "MLE-bench 使用来自 Kaggle 的真实机器学习竞赛任务，评估 agent 的 machine-learning engineering 能力。"}, "task_format": {"en": "The agent prepares data, trains models, runs experiments, and submits a solution for one of 75 curated ML competitions.", "zh": "agent 需要准备数据、训练模型、运行实验，并为 75 个精选 ML 竞赛之一提交解决方案。"}, "scoring": {"metric_name": "Any-medal rate", "explanation": {"en": "The score is the share of competitions where the agent reaches at least a Kaggle bronze-medal threshold. Low, medium, high, and all-complexity slices are reported separately; this series uses All.", "zh": "分数是 agent 至少达到 Kaggle bronze medal 门槛的竞赛占比。low、medium、high 和 all-complexity slice 分开报告；本序列使用 All。"}}, "evaluation_target": "environment_outcome", "protocol": "Original MLE-bench AIDE baseline series across 75 fixed competitions. Pass@1/Pass@10 and complexity slices are not mixed into the All any-medal metric."},
    {"id": "paperbench", "name": "PaperBench", "domain": "Science / research", "file": "paperbench_external.csv", "score": "Score (%)", "release": "2025-04-02", "floor": 0.0, "ceiling": 1.0, "source": "https://openai.com/index/paperbench/", "summary": {"en": "PaperBench evaluates agents on reproducing machine-learning research papers from scratch.", "zh": "PaperBench 评估 agent 能不能从头复现机器学习 research paper。"}, "task_format": {"en": "The agent reads a paper, builds a codebase, executes experiments in a fresh environment, and is graded against a paper-specific rubric.", "zh": "agent 需要阅读论文、构建 codebase、在全新环境中运行实验，再按照每篇论文专属 rubric 评分。"}, "scoring": {"metric_name": "Mean replication score", "explanation": {"en": "The score is the average fraction of rubric outcomes satisfied across 20 ICML 2024 papers. BasicAgent results are used here; IterativeAgent and Code-Dev are separate series.", "zh": "分数是 20 篇 ICML 2024 论文中满足 rubric outcome 的平均比例。本序列使用 BasicAgent；IterativeAgent 和 Code-Dev 是独立序列。"}}, "evaluation_target": "environment_outcome", "protocol": "PaperBench BasicAgent full-replication series from the official leaderboard. The benchmark's LLM judge and paper-specific rubrics are part of the measurement object."},
    {"id": "mmmu", "name": "MMMU", "domain": "Multimodal", "file": "mmmu_external.csv", "score": "Score", "release": "2023-12-04", "floor": 0.25, "ceiling": 1.0, "source": "https://github.com/MMMU-Benchmark/MMMU", "summary": {"en": "MMMU tests multimodal college-level knowledge and reasoning across six disciplines and diverse visual formats.", "zh": "MMMU 测试模型在六个学科和多种视觉材料上的大学水平多模态知识与推理能力。"}, "task_format": {"en": "The model receives a question with text and an image such as a chart, diagram, map, or chemical structure, then selects or produces the answer.", "zh": "模型会收到带文字和图片的问题，图片可能是图表、示意图、地图或化学结构，然后选择或生成答案。"}, "scoring": {"metric_name": "Validation accuracy", "explanation": {"en": "The score is the fraction of validation questions answered correctly. The four-choice format makes 25% a random-choice reference floor.", "zh": "分数是 validation question 中答对的比例。由于题目通常有四个选项，25% 是随机选择的参考 floor。"}}, "evaluation_target": "final_output", "protocol": "MMMU original fixed validation series from the official benchmark leaderboard and paper. MMMU-Pro is a separate measurement object and is not merged."},
    {"id": "mmmu-pro", "name": "MMMU-Pro", "domain": "Multimodal", "file": "mmmu_pro_external.csv", "score": "Score", "release": "2024-09-05", "floor": 0.0, "ceiling": 1.0, "source": "https://huggingface.co/datasets/MMMU/MMMU_Pro", "summary": {"en": "MMMU-Pro strengthens multimodal academic reasoning by filtering text-solvable items, expanding answer choices, and adding a vision-only setting.", "zh": "MMMU-Pro 通过过滤仅靠文字可解的题目、增加选项并加入 vision-only setting，强化多模态 academic reasoning 测试。"}, "task_format": {"en": "The model solves the same broad academic task style under Standard-10 and Vision formats; the Vision format embeds the question and options in the image.", "zh": "模型在 Standard-10 和 Vision 两种格式下完成 academic task；Vision 格式会把问题和选项直接放进图片。"}, "scoring": {"metric_name": "Overall accuracy", "explanation": {"en": "The headline score is the average of accuracy in the Standard-10 and Vision settings. These settings are not mixed with original MMMU accuracy.", "zh": "headline score 是 Standard-10 和 Vision 两种 setting accuracy 的平均值。这两个 setting 不和原始 MMMU accuracy 混合。"}}, "evaluation_target": "final_output", "protocol": "MMMU-Pro fixed release; overall score is the official average of Standard-10 and Vision settings. Original MMMU and later dynamic leaderboard configurations remain separate."},
    {"id": "bfcl-v4", "name": "BFCL V4", "domain": "Tool use", "file": "bfcl_v4_external.csv", "score": "Overall Accuracy", "release": "2025-07-17", "floor": 0.0, "ceiling": 1.0, "source": "https://gorilla.cs.berkeley.edu/leaderboard.html", "summary": {"en": "BFCL V4 evaluates accurate function and tool calling, including multi-turn and agentic scenarios with real-world functions.", "zh": "BFCL V4 评估模型准确调用 function 和 tool 的能力，包含 multi-turn 及更 agentic 的真实场景。"}, "task_format": {"en": "The model receives a user request and function definitions, then must emit valid calls and arguments; V4 adds multi-turn state, error recovery, and agentic formats.", "zh": "模型会收到用户请求和 function 定义，需要输出有效的调用及参数；V4 增加了 multi-turn state、错误恢复和 agentic format。"}, "scoring": {"metric_name": "Overall accuracy", "explanation": {"en": "Overall accuracy is the unweighted average of the BFCL V4 sub-category scores. Native function-calling and prompt-only modes are retained as distinct observations.", "zh": "Overall accuracy 是 BFCL V4 各子类别分数的非加权平均。原生 function-calling 和 prompt-only 模式作为不同 observation 保留。"}}, "evaluation_target": "process_and_output", "protocol": "BFCL V4 fixed evaluator checkpoint (commit f7cf735 / bfcl-eval 2025.12.17). Scores are not mixed with BFCL V1–V3 or across FC and Prompt modes without preserving the mode in provenance."},
    {"id": "humaneval", "name": "HumanEval", "domain": "Coding", "file": "humaneval_external.csv", "score": "Pass@1", "release": "2021-07-07", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2107.03374", "summary": {"en": "HumanEval is a classic function-level code-generation benchmark with executable unit tests.", "zh": "HumanEval 是经典的 function-level code-generation benchmark，通过可执行 unit tests 检查代码。"}, "task_format": {"en": "The model receives a Python function signature and docstring, then generates an implementation that is run against hidden tests.", "zh": "模型会收到 Python function signature 和 docstring，然后生成实现并通过隐藏测试运行。"}, "scoring": {"metric_name": "Pass@1", "explanation": {"en": "Pass@1 is the probability that one sampled/generated completion passes the hidden tests. This series uses reported single-sample or greedy Pass@1 values and does not mix HumanEval+.", "zh": "Pass@1 是一次生成的 completion 通过隐藏测试的概率。本序列使用公开的 single-sample 或 greedy Pass@1，不混入 HumanEval+。"}}, "evaluation_target": "final_output", "protocol": "HumanEval original 164-problem fixed task set; executable Python unit-test scoring. Sampling temperature and sample-count differences are retained in row notes."},
    {"id": "bigcodebench", "name": "BigCodeBench", "domain": "Coding", "file": "bigcodebench_external.csv", "score": "Complete Pass@1", "release": "2024-06-18", "floor": 0.0, "ceiling": 1.0, "source": "https://huggingface.co/blog/leaderboard-bigcodebench", "summary": {"en": "BigCodeBench evaluates practical code generation with complex instructions, multiple function calls, and diverse libraries.", "zh": "BigCodeBench 通过复杂指令、多次 function call 和多种 library，评估更贴近实际的 code generation。"}, "task_format": {"en": "In the Complete setting, the model fills in a function implementation from a detailed docstring and is evaluated on curated executable tests across 139 libraries.", "zh": "在 Complete setting 中，模型根据详细 docstring 补全 function implementation，再通过覆盖 139 个 library 的可执行测试评估。"}, "scoring": {"metric_name": "Calibrated Pass@1", "explanation": {"en": "Calibrated Pass@1 measures the share of tasks passed after the benchmark's prescribed completion calibration. Complete and Instruct are separate measurement variants; this series uses Complete.", "zh": "Calibrated Pass@1 是按照 benchmark 规定的 completion calibration 后通过的 task 占比。Complete 和 Instruct 是不同 measurement variant；本序列使用 Complete。"}}, "evaluation_target": "final_output", "protocol": "BigCodeBench Complete fixed release with calibrated greedy Pass@1. BigCodeBench Instruct and BigCodeBench-Hard are not merged."},
])

# AssistantBench uses a fixed 214-task set and a published Browser-Use result
# export. Its leaderboard reports full-run cost, so no benchmark-level cost is
# inferred here from totals or from an unrelated serving configuration.
BENCHMARKS.extend([
    {"id": "assistantbench", "name": "AssistantBench", "domain": "General agent tasks", "file": "assistantbench_external.csv", "score": "Accuracy", "release": "2024-07-23", "floor": 0.0, "ceiling": 1.0, "source": "https://assistantbench.github.io/", "summary": {"en": "AssistantBench evaluates web-capable assistants on realistic, time-consuming tasks that require multi-step research across the internet.", "zh": "AssistantBench 评估具备网页能力的 assistant 完成真实、耗时且需要多步互联网 research 的 task 的能力。"}, "task_format": {"en": "The agent receives a real-world question and must browse across websites, gather evidence, reason over it, and submit a final answer.", "zh": "agent 会收到一个真实世界问题，需要跨网站浏览、收集证据、进行推理，并提交最终答案。"}, "scoring": {"metric_name": "Task accuracy", "explanation": {"en": "Accuracy is the fraction of the fixed 214 tasks answered correctly under the published Browser-Use evaluation export. Full-run costs shown by the source are not treated as per-task cost.", "zh": "Accuracy 是在公开 Browser-Use evaluation export 中答对固定 214 个 task 的比例。来源展示的 full-run cost 不会被当作 per-task cost。"}}, "evaluation_target": "environment_outcome", "protocol": "AssistantBench fixed 214-task release; this series uses one result per underlying model from the HAL Browser-Use verified export. Scaffold, model configuration, and full-run cost remain in observation notes; no configurations are silently merged."},
])

BENCHMARKS.extend([
    {"id": "balrog", "name": "BALROG", "domain": "General agent tasks", "file": "balrog_external.csv", "score": "Average progress", "release": "2024-11-20", "floor": 0.0, "ceiling": 1.0, "source": "https://balrogai.com/", "summary": {"en": "BALROG evaluates language and vision-language agents on long-horizon interactive tasks across challenging game environments.", "zh": "BALROG 在多个高难度游戏环境中评估 language agent 和 vision-language agent 完成长链交互任务的能力。"}, "task_format": {"en": "The agent observes a game environment, chooses actions over many steps, and must make progress toward the environment's goal while adapting to feedback.", "zh": "agent 会观察游戏环境，在很多 step 中持续选择动作，并根据反馈适应，逐步完成环境目标。"}, "scoring": {"metric_name": "Average progress", "explanation": {"en": "Average progress aggregates normalized progress across six game environments. It is a progress measure rather than a simple exact-answer accuracy, and the environment-level scores remain available in the observation source.", "zh": "Average progress 汇总六个游戏环境中的 normalized progress。它是 progress metric，不是简单的 exact-answer accuracy；各环境分数仍保留在 observation source 中。"}}, "evaluation_target": "environment_outcome", "protocol": "BALROG fixed six-environment evaluation; the curated series uses official leaderboard Average progress rows and keeps language/vision setup and environment-level scores in row provenance."},
    {"id": "gso", "name": "GSO", "domain": "Software engineering", "file": "gso_external.csv", "score": "Score OPT@1", "release": "2025-05-29", "floor": 0.0, "ceiling": 1.0, "source": "https://gso-bench.github.io/index.html", "summary": {"en": "GSO evaluates software-engineering agents on difficult repository-level performance-optimization tasks.", "zh": "GSO 评估 software-engineering agent 完成高难度 repository-level performance optimization task 的能力。"}, "task_format": {"en": "The agent receives a codebase and performance tests, then must produce a patch that improves runtime efficiency while preserving functional correctness.", "zh": "agent 会收到一个 codebase 和 performance tests，需要提交提升运行效率、同时保持功能正确的 patch。"}, "scoring": {"metric_name": "Opt@1", "explanation": {"en": "Opt@1 is the share of tasks where one submitted patch matches or exceeds the expert optimization target while passing correctness checks. The task set contains 102 optimization problems across 10 codebases.", "zh": "Opt@1 是一次提交的 patch 在通过正确性检查的同时，达到或超过专家优化目标的 task 占比。task set 包含 10 个 codebase 上的 102 个 optimization problem。"}}, "evaluation_target": "environment_outcome", "protocol": "GSO fixed optimization task set; this series uses Score OPT@1 from the official OpenHands leaderboard export. OPT@10 and hack-adjusted variants remain separate metrics."},
    {"id": "metr-time-horizon-1-1", "name": "METR Time Horizon 1.1", "domain": "Science / research", "file": "metr_time_horizons_external.csv", "score": "Time horizon", "release": "2026-01-29", "floor": None, "ceiling": None, "score_format": "number", "source": "https://metr.org/blog/2026-1-29-time-horizon-1-1/", "summary": {"en": "METR Time Horizon 1.1 estimates how long an AI agent can complete software and research tasks with a target probability of success.", "zh": "METR Time Horizon 1.1 估计 AI agent 能以目标成功概率完成多长的人类工作量级 software 和 research task。"}, "task_format": {"en": "The agent attempts a suite of software and research tasks whose human-equivalent completion times vary substantially, using a standardized evaluation scaffold.", "zh": "agent 会在标准化 evaluation scaffold 下完成一组 software 和 research task，这些 task 对人类而言所需的等效完成时间差异很大。"}, "scoring": {"metric_name": "50% task-completion time horizon", "explanation": {"en": "The time horizon is the estimated human-equivalent task duration at which the agent has a 50% probability of success. It is measured in minutes and is not a bounded 0–100% score, so percentage lifecycle thresholds are not applicable.", "zh": "time horizon 是 agent 以 50% 概率成功时对应的人类等效 task 时长，单位为分钟。它不是 0–100% bounded score，因此不适用百分比 lifecycle threshold。"}}, "evaluation_target": "environment_outcome", "protocol": "METR Time Horizon 1.1 methodology and task suite; the headline metric is the estimated 50% time horizon in human-equivalent minutes. TH1.0 and TH1.1 are separate measurement versions and are not merged."},
    {"id": "exploitbench", "name": "ExploitBench", "domain": "Cybersecurity", "file": "exploitbench_base_external.csv", "score": "Mean capability", "release": "2026-05-18", "floor": 0.0, "ceiling": 1.0, "source": "https://exploitbench.ai/", "summary": {"en": "ExploitBench measures how far cybersecurity agents progress from reaching vulnerable code to producing working exploit capabilities.", "zh": "ExploitBench 衡量 cybersecurity agent 从定位 vulnerable code 到产生可用 exploit capability 的进展程度。"}, "task_format": {"en": "The agent works in controlled vulnerability environments and attempts increasingly difficult exploit-development stages, from triggering a bug to achieving arbitrary code execution.", "zh": "agent 会在受控 vulnerability environment 中完成逐级变难的 exploit-development stage，从触发 bug 到实现 arbitrary code execution。"}, "scoring": {"metric_name": "Mean capability", "explanation": {"en": "Mean capability aggregates the normalized capability level reached across the benchmark environments. The base-harness series is kept separate from AutoNudge-assisted runs.", "zh": "Mean capability 汇总 agent 在各 benchmark environment 中达到的 normalized capability level。本卡将 base-harness series 与 AutoNudge assisted runs 分开。"}}, "evaluation_target": "environment_outcome", "protocol": "ExploitBench public May 2026 snapshot; this series uses base-harness Mean capability rows only. AutoNudge-assisted rows are intentionally excluded as a separate intervention."},
    {"id": "proofbench-v1-1", "name": "ProofBench v1.1", "domain": "Mathematics", "file": "proofbench_v1_1_external.csv", "score": "Accuracy", "release": "2026-08-14", "floor": 0.0, "ceiling": 1.0, "source": "https://www.vals.ai/benchmarks/proof_bench", "summary": {"en": "ProofBench v1.1 evaluates whether models can produce formally checked Lean 4 proofs for mathematical statements.", "zh": "ProofBench v1.1 评估模型能不能为数学命题生成经过 Lean 4 formal checker 验证的 proof。"}, "task_format": {"en": "The model receives a natural-language theorem paired with a Lean 4 formalization and must generate a proof accepted by the Lean kernel.", "zh": "模型会收到自然语言 theorem 及其 Lean 4 formalization，需要生成一个被 Lean kernel 接受的 proof。"}, "scoring": {"metric_name": "Formal proof accuracy", "explanation": {"en": "Accuracy is the share of theorem instances for which the generated proof is accepted by the Lean checker. This card uses the v1.1 re-graded series; v1.0-era scores are not mixed.", "zh": "Accuracy 是生成的 proof 被 Lean checker 接受的 theorem instance 占比。本卡使用 v1.1 re-grade series，不混入 v1.0 时代的分数。"}}, "evaluation_target": "environment_outcome", "protocol": "ProofBench v1.1 re-grade published by Vals AI; corrected Lean formalizations and hardened grading are treated as a new fixed measurement object."},
    {"id": "dtbench", "name": "DTBench", "domain": "General knowledge & reasoning", "file": "dtbench_external.csv", "score": "Accuracy", "release": "2026-08-12", "floor": 0.0, "ceiling": 1.0, "source": "https://alignment.anthropic.com/2026/conceptual-reasoning-index/", "summary": {"en": "DTBench measures decision-theoretic reasoning about a model's own behavior and interactions with copies or near-copies.", "zh": "DTBench 衡量模型在 decision theory 场景下推理自身行为，以及和自身或近似副本互动的能力。"}, "task_format": {"en": "The model answers 407 handcrafted multiple-choice questions about decision-theoretic situations, including prediction and interaction with near-copies.", "zh": "模型需要回答 407 道人工设计的 multiple-choice decision theory 问题，内容包括行为预测以及和近似副本互动。"}, "scoring": {"metric_name": "Question accuracy", "explanation": {"en": "The score is the fraction of the 407 DTBench capabilities questions answered correctly. The additional attitude questions and the aggregate CRI are separate measurement objects.", "zh": "分数是 407 道 DTBench capabilities question 中答对的比例。额外的 attitude questions 和 aggregate CRI 属于独立 measurement object。"}}, "evaluation_target": "final_output", "protocol": "DTBench capabilities fixed 407-question series reported with the Conceptual Reasoning Index. Full DTBench attitude questions and CRI aggregate scores are not merged."},
    {"id": "apex-agents", "name": "APEX-Agents", "domain": "General agent tasks", "file": "apex_agents_external.csv", "score": "Pass@1 score", "release": "2026-01-20", "floor": 0.0, "ceiling": 1.0, "source": "https://www.mercor.com/apex/apex-agents-leaderboard/", "summary": {"en": "APEX-Agents evaluates agents on long-horizon, cross-application professional work for investment banking, consulting, and legal roles.", "zh": "APEX-Agents 评估 agent 在投资银行、咨询和法律等职业场景中完成跨应用长链专业工作的能力。"}, "task_format": {"en": "The agent works through realistic files and software applications over a multi-step professional task, then is graded against task-specific rubrics and gold outputs.", "zh": "agent 需要在真实的文件和软件应用中完成多步专业 task，再按照 task 专属 rubric 和 gold output 评分。"}, "scoring": {"metric_name": "Pass@1", "explanation": {"en": "Pass@1 is the share of tasks solved by one agent trajectory. This series uses the benchmark's overall 480-task evaluation and keeps reasoning effort and harness variants in observation provenance.", "zh": "Pass@1 是一次 agent trajectory 成功解决的 task 占比。本序列使用 benchmark overall 480-task evaluation，并在 observation provenance 中保留 reasoning effort 和 harness variant。"}}, "evaluation_target": "environment_outcome", "protocol": "APEX-Agents fixed 480-task release; the curated series uses Pass@1 rows from the public leaderboard. Mean Score, Loop, ReAct, and job-specific slices are not mixed into the headline metric."},
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
    "video-mme": ("Model", "Multimodal", ["video", "temporal reasoning", "no subtitles"]),
    "mathvista": ("Model", "Multimodal", ["visual math", "charts", "diagrams"]),
    "browsecomp": ("Agent", "General agent tasks", ["browsing", "research", "multi-hop"]),
    "longbench-v2": ("Model", "Long context", ["long documents", "multiple-choice", "reasoning"]),
    "healthbench": ("Model", "Health", ["medical", "physician rubric", "safety"]),
    "ifeval": ("Model", "Instruction following", ["verifiable", "constraints", "format"]),
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
    "benchcad-vision2code": ("Model", "Multimodal", ["programmatic CAD", "vision-to-code", "execution-grounded"]),
    "gaia": ("Agent", "General agent tasks", ["browsing", "multimodal", "tool use", "long-horizon"]),
    "mcp-atlas": ("Agent", "Tool use", ["MCP", "multi-step", "real tools", "claim grading"]),
    "toolathlon-verified": ("Agent", "Tool use", ["MCP", "multi-step", "Pass@1", "tool calls"]),
    "the-agent-company": ("Agent", "General agent tasks", ["workplace", "multi-step", "browser", "coding"]),
    "deepswe-v1-1": ("Agent", "Software engineering", ["repository", "long-horizon", "cost"]),
    "frontierswe-v2": ("Agent", "Software engineering", ["repository", "quality", "multi-run"]),
    "scienceagentbench": ("Agent", "Science / research", ["scientific discovery", "Python", "verified"]),
    "mle-bench": ("Agent", "Science / research", ["ML engineering", "Kaggle", "long-horizon"]),
    "paperbench": ("Agent", "Science / research", ["research replication", "experiments", "rubric"]),
    "mmmu": ("Model", "Multimodal", ["vision", "academic", "multi-discipline"]),
    "mmmu-pro": ("Model", "Multimodal", ["vision-only", "ten-choice", "academic"]),
    "bfcl-v4": ("Agent", "Tool use", ["function calling", "multi-turn", "agentic"]),
    "humaneval": ("Model", "Coding", ["Python", "function-level", "unit tests"]),
    "bigcodebench": ("Model", "Coding", ["libraries", "function calls", "calibrated Pass@1"]),
    "assistantbench": ("Agent", "General agent tasks", ["browsing", "multi-step", "web", "research"]),
    "balrog": ("Agent", "General agent tasks", ["games", "interactive", "long-horizon", "vision"]),
    "gso": ("Agent", "Software engineering", ["optimization", "repository", "performance", "test-based"]),
    "metr-time-horizon-1-1": ("Agent", "Science / research", ["long-horizon", "software", "research", "time horizon"]),
    "exploitbench": ("Agent", "Cybersecurity", ["security", "exploit development", "environment", "capability ladder"]),
    "proofbench-v1-1": ("Model", "Mathematics", ["formal proof", "Lean 4", "theorem proving", "verified"]),
    "dtbench": ("Model", "General knowledge & reasoning", ["decision theory", "multiple-choice", "conceptual reasoning"]),
    "apex-agents": ("Agent", "General agent tasks", ["professional work", "cross-application", "long-horizon", "Pass@1"]),
    "big-bench-hard": ("Model", "General knowledge & reasoning", ["reasoning", "multi-task", "few-shot"]),
    "scienceqa": ("Model", "Science", ["multimodal", "multiple-choice", "explanation"]),
    "hellaswag": ("Model", "General knowledge & reasoning", ["commonsense", "multiple-choice"]),
    "piqa": ("Model", "General knowledge & reasoning", ["physical commonsense", "multiple-choice"]),
    "triviaqa": ("Model", "General knowledge & reasoning", ["open-domain QA", "evidence"]),
    "superglue": ("Model", "General knowledge & reasoning", ["language understanding", "multi-task"]),
    "cybench": ("Agent", "Cybersecurity", ["cybersecurity", "terminal", "environment"]),
    "deepresearch-bench": ("Agent", "General agent tasks", ["research", "browsing", "citation"]),
    "scicode": ("Agent", "Science / research", ["scientific coding", "execution", "research"]),
    "spatialviz-bench": ("Model", "Multimodal", ["spatial reasoning", "visual", "geometry"]),
    "vending-bench-2": ("Agent", "General agent tasks", ["simulation", "long-horizon", "business"]),
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
    cleaned_model = re.sub(r"\s*\([^)]*\)", "", model)
    return slug(f"{organization}-{cleaned_model}")


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
        for row_number, row in enumerate(csv.DictReader(handle), start=1):
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
                # Some exports repeat a model name or omit a stable row ID.
                # The row suffix keeps every canonical observation addressable.
                "observation_id": f"obs-{spec['id']}-{row.get('id') or slug(model)}-{row_number}",
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
