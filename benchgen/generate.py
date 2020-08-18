import os
import re
from importlib import import_module

from .parser import Parser

def generate(input, output, generator_type, filter):
  if os.path.isdir(input):
    files = list_files(input, filter)
    failures = []
    for file in files:
      input_file = os.path.join(input, file)
      print(f'\nProcessing input file: {input_file}')
      output_dir = re.sub(r'\.xml$', '', file)
      output_path = os.path.join(output, output_dir)
      try:
        run(input_file, output_path, generator_type)
      except Exception as e:
        print(e)
        failures.append(input_file)
    if len(failures) > 0:
      print('Failed to process the following input files:')
      print('  ' + '\n  '.join(failures))
  else:
    run(input, output, generator_type)
  print('\nFinished!')

def run(input_path, output_path, generator_type):
  xml = read_file(input_path)
  parser = Parser()
  data = parser.parse(xml)
  generator = import_module(f'.generators.{generator_type}', package=__package__)
  generator.generate(data, parser, output_path)

def list_files(dir, regex):
  files = []
  directory = os.fsencode(dir)
  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if re.search(regex, filename): 
      files.append(filename)
  return files

def read_file(path):
  file = open(path, 'r', encoding='utf-8')
  content = file.read()
  file.close()
  return content
