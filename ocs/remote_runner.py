#!/usr/bin/env python3
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--workload', required=True)
    parser.add_argument('--instance', required=True)

    args = parser.parse_args()

    print(args.workload)
    print(args.instance)
