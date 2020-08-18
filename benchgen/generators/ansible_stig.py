from os import path
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(Path(Path(__file__).parent, '..', '..', 'templates').resolve()))

def generate(data, parser, output_path):
  Path(output_path).mkdir(parents=True, exist_ok=True)
  manifest = []
  for i, severity in enumerate(['high', 'medium', 'low']):
    manifest.append(f'\n{severity}')
    rules = find_rules_by_severity(data['groups'], severity)
    tasks = list(map(lambda rule: {
      'id': rule['groupId'],
      'title': rule['title'],
      'severity': severity,
      'tags': [
        f'cat{i+1}',
        severity,
        rule['groupId']
      ]
    }, rules))
    sort_by_id(tasks)
    manifest.extend(map(lambda t: f'{t["id"]} - {t["severity"]} - {t["title"]}', tasks))
    render_tasks(tasks, path.join(output_path, f'cat{i+1}.yml'))
  with open(path.join(output_path, 'manifest.txt'), 'w', encoding='utf-8') as file:
    file.write('\n'.join(manifest))

def find_rules_by_severity(groups, severity):
  rules = []
  for group in groups:
    for rule in group['rules']:
      if rule['severity'] == severity:
        rule['groupId'] = group['id']
        rules.append(rule)
  return rules

def render_tasks(tasks, output_path):
  template = env.get_template('ansible_stig.yml.j2')
  result = template.render(tasks=tasks)
  with open(output_path, 'w', encoding='utf-8') as file:
    file.write(result)

def sort_by_id(items):
  return sorted(items, key=lambda item: item['id'])
