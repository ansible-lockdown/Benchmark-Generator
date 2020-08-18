# XCCDF Benchmark Generator

Developed by Refactr in partnership with MindPoint Group. For more, visit https://refactr.it

Generates complex output from an XCCDF file. Used to generate initial project files for automation tools in various formats.

Current generators:

* Ansible Tasks (CIS)
* Ansible Tasks (STIG)

```
usage: benchgen [-h] [-t TYPE] -i INPUT -o OUTPUT [-f FILTER]

Generate output from an XCCDF benchmark.

optional arguments:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  Generator type. Can be ansible_cis or ansible_stig.
  -i INPUT, --input INPUT
                        Path to XCCDF benchmark(s). If this is a file, a
                        single output folder will be generated. If it is a
                        directory, one output folder is generated for each
                        benchmark in the folder. Use the --filter option to
                        filter input files.
  -o OUTPUT, --output OUTPUT
                        Output directory path.
  -f FILTER, --filter FILTER
                        Input file filter (regex).
```

### How to Install

    pipenv install

### How to Run

#### View Help

    pipenv run python -m benchgen --help

#### Generate CIS or STIG for a single XCCDF file:

    pipenv run python -m benchgen -t ansible_cis -i ./example-benchmarks/RHEL7-CIS.xml -o ./example-output/ansible_cis/RHEL7-CIS
    pipenv run python -m benchgen -t ansible_stig -i ./example-benchmarks/RHEL7-STIG.xml -o ./example-output/ansible_stig/RHEL7-STIG

#### Generate CIS or STIG for multiple XCCDF files:

Note: These commands assume existing folders with all CIS or STIG benchmark XCCDF files present. These are not included in this repository.

    pipenv run python -m benchgen -t ansible_cis -i /opt/xccdf/cis-benchmarks -f 'xccdf\.xml$' -o /opt/xccdf/output/ansible_cis
    pipenv run python -m benchgen -t ansible_stig -i /opt/xccdf/stig-benchmarks -f 'xccdf\.xml$' -o /opt/xccdf/output/ansible_stig
