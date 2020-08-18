from os import path
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(Path(Path(__file__).parent, '..', '..', 'templates').resolve()))

def generate(data, parser, output_path):
  rule_set = get_tagged_rule_ids(data['profiles'])
  if isinstance(rule_set, list):
    for rs in rule_set:
      render_rule_set(data, rs['rules'], f'{output_path}{rs["suffix"] or ""}')
  else:
    render_rule_set(data, rule_set, output_path)

def render_rule_set(data, rule_set, output_path):
  Path(output_path).mkdir(parents=True, exist_ok=True)
  manifest = []
  for i, section in enumerate(range(1, 7)):
    manifest.append(f'\nsection{i+1}')
    groups = list(filter(lambda g: g['number'].startswith(str(section)), data['groups']))
    tasks = []
    for group in groups:
      for rule in group['rules']:
        tags = []
        for t, r in rule_set.items():
          if rule['id'] in r:
            tags.append(t)
        tags.append(f'rule_{rule["number"]}')
        rule_name = re.sub(r'_', ' ', rule['id'].split(f'{rule["number"]}_')[1].strip())
        tasks.append({
          'name': rule_name,
          'number': rule['number'],
          'tags': tags
        })
    sort_by_number(tasks)
    manifest.extend(map(lambda t: f'{t["number"]} - {t["name"]}', tasks))
    render_tasks(tasks, path.join(output_path, f'section{section}.yml'))
  with open(path.join(output_path, 'manifest.txt'), 'w', encoding='utf-8') as file:
    file.write('\n'.join(manifest))

def get_tagged_rule_ids(profiles):
  # If there is a single Level 1 profile produce one level1 rule set
  if len(profiles) == 1 and 'Level_1' in profiles[0]['id']:
    return {
      'level1': set(map(lambda r: r['idref'], profiles[0]['selections']))
    }
  # If there are 2 profiles, Level 1 and Level 2, produce a rule set for each
  if len(profiles) == 2 and 'Level_1' in profiles[0]['id'] and 'Level_2' in profiles[1]['id']:
    return {
      'level1': set(map(lambda r: r['idref'], profiles[0]['selections'])),
      'level2': set(map(lambda r: r['idref'], profiles[1]['selections']))
    }
  # If there are 4 profiles, two designated as Server, use the server profiles for level1 and level2 and ignore the others
  if len(profiles) == 4:
    level1Server = next((p for p in profiles if p['id'] == 'xccdf_org.cisecurity.benchmarks_profile_Level_1_-_Server'), None)
    level2Server = next((p for p in profiles if p['id'] == 'xccdf_org.cisecurity.benchmarks_profile_Level_2_-_Server'), None)
    if level1Server and level2Server:
      return {
        'level1': set(map(lambda r: r['idref'], level1Server['selections'])),
        'level2': set(map(lambda r: r['idref'], level2Server['selections']))
      }
  # If there are Domain Member/Controller Level 1 and Level 2 profiles, return one rule set for each. This produces multiple outputs.
  if len(profiles) >= 4:
    level1Domain = next((p for p in profiles if p['id'] == 'xccdf_org.cisecurity.benchmarks_profile_Level_1_-_Domain_Controller'), None)
    level2Domain = next((p for p in profiles if p['id'] == 'xccdf_org.cisecurity.benchmarks_profile_Level_2_-_Domain_Controller'), None)
    level1Member = next((p for p in profiles if p['id'] == 'xccdf_org.cisecurity.benchmarks_profile_Level_1_-_Member_Server'), None)
    level2Member = next((p for p in profiles if p['id'] == 'xccdf_org.cisecurity.benchmarks_profile_Level_2_-_Member_Server'), None)
    if level1Domain and level2Domain and level1Member and level2Member:
      return [{
        'suffix': '-Domain_Controller',
        'rules': {
          'level1': set(map(lambda r: r['idref'], level1Domain['selections'])),
          'level2': set(map(lambda r: r['idref'], level2Domain['selections']))
        }
      },{
        'suffix': '-Member_Server',
        'rules': {
          'level1': set(map(lambda r: r['idref'], level1Member['selections'])),
          'level2': set(map(lambda r: r['idref'], level2Member['selections']))
        }
      }]
  raise Exception(f'Generator does not support the following profiles: {list(map(lambda p: p["id"], profiles))}')

def render_tasks(tasks, output_path):
  template = env.get_template('ansible_cis.yml.j2')
  result = template.render(tasks=tasks)
  with open(output_path, 'w', encoding='utf-8') as file:
    file.write(result)

def sort_by_number(items):
  items.sort(key=lambda item: [int(n) for n in item['number'].split('.')])