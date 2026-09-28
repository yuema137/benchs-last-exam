"""Protocol variants must not improve any canonical card or lifecycle metric."""
import csv
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from scripts import build_snapshot as build


class AuxiliaryProtocolTests(unittest.TestCase):
    def setUp(self):
        self.spec = dict(next(s for s in build.BENCHMARKS if s['id'] == 'cadworld-v1'))
        self.spec['cost_column'] = 'Cost'
        self.canonical = {'Name': 'Example model', 'Success rate': '.3',
                          'Organization': 'OpenAI', 'Result public date': '2026-09-20',
                          'Source link': 'https://example.org/canonical', 'Cost': '2'}
        self.auxiliary = {
            **self.canonical, 'Name': 'Other model', 'Success rate': '.99',
            'Organization': 'Anthropic', 'Cost': '100',
            'Auxiliary protocol': 'different-task-set',
            'Auxiliary task set': 'subset', 'Auxiliary label': 'Subset evaluation',
            'Auxiliary explanation en': 'Different tasks and grading.',
            'Auxiliary explanation zh': '题集和评分方式不同。',
        }

    def build_rows(self, rows):
        with tempfile.TemporaryDirectory() as folder:
            fields = list(dict.fromkeys(key for row in rows for key in row))
            with (Path(folder) / self.spec['file']).open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fields)
                writer.writeheader()
                writer.writerows(rows)
            with patch.object(build, 'RAW', Path(folder)):
                evidence = []
                benchmark = build.build_benchmark(self.spec, {}, {}, evidence)
                return benchmark, evidence

    def test_high_auxiliary_score_does_not_change_canonical_views(self):
        before, _ = self.build_rows([self.canonical])
        after, evidence = self.build_rows([self.canonical, self.auxiliary])
        for field in ('frontier_events', 'capability_frontier_value', 'reported_frontier_value',
                      'normalized_progress', 'normalized_headroom', 'threshold_days',
                      'reported_threshold_days', 'velocity_180d', 'coverage'):
            self.assertEqual(before[field], after[field], field)
        self.assertEqual(before['cost_per_task']['value'], after['cost_per_task']['value'])
        self.assertEqual(build.lifecycle_eligibility(before, date(2026, 9, 27)),
                         build.lifecycle_eligibility(after, date(2026, 9, 27)))
        self.assertEqual(len(evidence), 2)
        series = after['auxiliary_score_series'][0]
        self.assertFalse(series['lifecycle_eligible'])
        self.assertEqual(series['label'], 'Subset evaluation')
        self.assertEqual(series['frontier_events'][0]['score'], .99)

    def test_incomplete_or_canonical_protocol_metadata_is_rejected(self):
        for change in ({'Auxiliary explanation zh': ''},
                       {'Auxiliary protocol': self.spec['protocol_id']}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.build_rows([{**self.auxiliary, **change}])

    def test_conflicting_metadata_is_rejected_even_for_duplicate_measurements(self):
        with self.assertRaises(ValueError):
            self.build_rows([self.auxiliary, {**self.auxiliary, 'Auxiliary label': 'Conflicting label'}])

class AuxiliaryOnlyCardTests(unittest.TestCase):
    def test_auxiliary_only_card_has_unknown_metrics_and_requires_reason(self):
        import copy
        import json
        from scripts.validate_benchmark_integration import validate_benchmark
        payload = json.loads(Path('site/data/benchmarks.json').read_text())
        card = next(b for b in payload['benchmarks'] if b['id'] == 'showandtell-v1-comprehension')
        resources = {r['id']: r for r in payload['resources']}
        models = {m['id']: m for m in payload['models']}
        self.assertEqual(validate_benchmark(card, resources, models), [])
        self.assertIsNone(card['capability_frontier_value'])
        self.assertTrue(all(not x['eligible'] for x in card['lifecycle_eligibility'].values()))
        broken = copy.deepcopy(card)
        broken['unavailable'] = []
        self.assertTrue(any('unavailable reason' in e for e in validate_benchmark(broken, resources, models)))


if __name__ == '__main__':
    unittest.main()
