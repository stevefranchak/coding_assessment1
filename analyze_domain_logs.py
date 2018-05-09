import argparse
import pathlib
import re
import sys

# Accept one positional argument that points to the domain log file
parser = argparse.ArgumentParser(description='Report unique domain \
                                names, top five most frequent domains, and \
                                lines with invalid IPv4 addresses in a domain \
                                log file')
parser.add_argument('domain_log_file', type=str,
                    help='filepath to the domain log')
args = parser.parse_args()

# Verify that the file actually exists
if not pathlib.Path(args.domain_log_file).is_file():
    print('Error: {} is not a file'.format(args.domain_log_file), file=sys.stderr)
    exit(1)

# Store tallies keyed by domain name
domain_counts = {}

# Compile the IPv4 regex once to help with performance
ipv4_address_regex = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\b')

with open(args.domain_log_file, 'r') as file:
    # Use enumerate to keep track of the line number
    for line_number, line in enumerate(file):
        timestamp, domain, ipv4_address = map(lambda item: item.strip(), line.split(' '))

        if domain in domain_counts:
            domain_counts[domain] += 1
        else:
            domain_counts[domain] = 1

        # Check if this line contains an invalid IPv4 address - print to stdout if so
        if not ipv4_address_regex.match(ipv4_address):
            # Increment line number by 1 for accuracy - line numbers start counting at 1, enumerate starts counting at 0
            print('{} {} {}'.format(line_number + 1, domain, ipv4_address))
        

print('\nTotal unique domain names: {}\n'.format(len(domain_counts.keys())))

print('Top 5 domain names with most occurrences:\n{}'.format(
    '\n'.join(
        [domain for sort_index, domain in enumerate(sorted(
            domain_counts.keys(), reverse=True, key=lambda domain: int(domain_counts[domain])
        )) if sort_index < 5]
    )
))
