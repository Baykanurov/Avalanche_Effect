import argparse

parser = argparse.ArgumentParser(description='Unique Hash algorithm with avalanche effect')

parser.add_argument('-f', '--file', help='Read text from file', type=str)
parser.add_argument('-t', '--text', help='Text', type=str)
parser.add_argument('-o', '--output', help='Output in file', type=str)
