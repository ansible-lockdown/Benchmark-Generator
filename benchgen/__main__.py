import argparse

from .generate import generate

def main():
  args = parse_args()
  generate(args.input, args.output, args.type, args.filter)

def parse_args():
  parser = argparse.ArgumentParser(
    prog='benchgen',
    description='Generate output from an XCCDF benchmark.'
  )
  parser.add_argument(
    '-t',
    '--type',
    default='ansible_cis',
    help='Generator type. Can be ansible_cis or ansible_stig.'
  )
  parser.add_argument(
    '-i',
    '--input',
    required=True,
    help='Path to XCCDF benchmark(s). If this is a file, a single output folder will be generated. If it is a directory, one output folder is generated for each benchmark in the folder. Use the --filter option to filter input files.'
  )
  parser.add_argument(
    '-o',
    '--output',
    required=True,
    help='Output directory path.'
  )
  parser.add_argument(
    '-f',
    '--filter',
    default='\\.xml$',
    help='Input file filter (regex).'
  )
  return parser.parse_args()

if __name__ == '__main__':
  main()