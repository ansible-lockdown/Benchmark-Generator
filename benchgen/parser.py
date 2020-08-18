from io import BytesIO
import re
from lxml import etree

group_number_regex = re.compile(r'^xccdf_org\..+\.benchmarks_group_((\d+\.?)+)_')
rule_number_regex = re.compile(r'^xccdf_org\..+\.benchmarks_rule_((\d+\.)+\d+)_')

class Parser():
  def __init__(self):
    self.rule_count = 0

  def parse(self, xml):
    parser = etree.XMLParser(resolve_entities=False)
    self.tree = etree.parse(BytesIO(bytes(xml, encoding='utf-8')), parser)
    self.benchmark_el = self.tree.getroot()
    self.get_root_namespace()
    print(f'Namespaces: {self.namespaces}')
    self.profiles = self.find_profiles()
    print('Profiles:', len(self.profiles))
    self.groups = self.find_groups()
    print('Groups:', len(self.groups))
    print('Rules:', self.rule_count)
    return {
      'profiles': self.profiles,
      'groups': self.groups
    }

  def get_root_namespace(self):
    if self.benchmark_el.tag[0] == '{':
      uri, tag = self.benchmark_el.tag[1:].split('}')
      self.namespaces = {
        'xccdf': uri
      }
    else:
      self.namespaces = None

  def find_profiles(self):
    profile_els = self.tree.xpath(f'./{self.make_el_name("Profile")}', namespaces=self.namespaces)
    return list(map(lambda profile_el: {
      'id': profile_el.get('id'),
      'title': profile_el.xpath(f'./{self.make_el_name("title")}', namespaces=self.namespaces)[0].text,
      'selections': list(map(lambda select_el: {
        'idref': select_el.get('idref'),
        'selected': select_el.get('selected')
      }, profile_el.xpath(f'.//{self.make_el_name("select")}', namespaces=self.namespaces)))
    }, profile_els))

  def find_groups(self):
    group_els = self.tree.xpath(f'//{self.make_el_name("Group")}', namespaces=self.namespaces)
    groups = []
    for group_el in group_els:
      rule_els = group_el.xpath(f'./{self.make_el_name("Rule")}', namespaces=self.namespaces)
      if len(rule_els) == 0:
        continue
      rules = []
      for rule_el in rule_els:
        rule_id = rule_el.get('id')
        rule = {
          'id': rule_id,
          'title': rule_el.xpath(f'./{self.make_el_name("title")}', namespaces=self.namespaces)[0].text
        }
        match = rule_number_regex.search(rule_id)
        if match:
          rule['number'] = match[1]
        severity = rule_el.get('severity')
        if severity:
          rule['severity'] = severity
        self.rule_count += 1
        rules.append(rule)
      group = {
        'id': group_el.get('id'),
        'title': group_el.xpath(f'./{self.make_el_name("title")}', namespaces=self.namespaces)[0].text,
        'rules': rules
      }
      match = group_number_regex.search(group['id'])
      if match:
        group['number'] = match[1]
      groups.append(group)
    return groups

  def make_el_name(self, name):
    if self.namespaces:
      return f'xccdf:{name}'
    else:
      return name