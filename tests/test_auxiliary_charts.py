"""Exercise real chart functions without a browser or third-party JS packages."""
import subprocess
import unittest


class AuxiliaryChartTests(unittest.TestCase):
    def test_numeric_and_auxiliary_only_charts(self):
        result = subprocess.run(['node', '-e', r'''
const fs=require('fs'), vm=require('vm'), assert=require('assert');
const source=fs.readFileSync('site/app.js','utf8');
const chartCode=source.slice(source.indexOf('function chart(b)'),source.indexOf('function showLeaderboard'));
const data=JSON.parse(fs.readFileSync('site/data/benchmarks.json','utf8'));
const context={state:{detailTimeline:'capability',detailY:'raw',detailX:'calendar',data},
  progress:(b,v)=>b.floor==null||b.ceiling==null?null:(v-b.floor)/(b.ceiling-b.floor),
  metricValue:(b,v)=>String(v),score:v=>String(v),t:v=>v,
  calendarTicks:()=>[],compactTicks:x=>x,niceElapsedInterval:()=>30,elapsedLabel:String};
vm.createContext(context);vm.runInContext(chartCode,context);
for(const id of ['gdpval-aa-v2','showandtell-v1-comprehension']) {
  const b=data.benchmarks.find(x=>x.id===id),before=JSON.stringify(b);
  for(const mode of ['raw','normalized']) {
    context.state.detailY=mode;
    const svg=context.chart(b);
    assert(svg.includes('auxiliary-curve'),id+' missing auxiliary curve');
    assert(svg.includes('axis-title'),id+' missing axes');
    assert(!/NaN|Infinity/.test(svg),id+' non-finite chart geometry');
    for(const match of svg.matchAll(/cy="([^"]+)"/g)) {
      assert(Number(match[1])>=21 && Number(match[1])<=249,id+' point outside y scale');
    }
  }
  assert.equal(JSON.stringify(b),before,'chart mutated canonical data');
  context.state.detailTimeline='reported';
  assert(!context.chart(b).includes('auxiliary-curve'),'auxiliary leaked into reported timeline');
  context.state.detailTimeline='capability';
}
'''], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
