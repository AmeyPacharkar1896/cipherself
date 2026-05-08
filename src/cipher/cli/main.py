import argparse
import sys

from cipher.cli.scan import handle_scan
from cipher.cli.compare import handle_compare
from cipher.cli.demo import handle_demo

def main():
    parser = argparse.ArgumentParser(
        description="cipher - Digital Footprint Intelligence Tool",
        epilog="run 'cipher <command> --help' for command-specific options"
    )
    subparsers = parser.add_subparsers(dest="command", title="commands")
    subparsers.required = True

    scan_parser = subparsers.add_parser("scan", help="Scan a subject's public digital footprint")
    scan_parser.add_argument("--github", help="GitHub username")
    scan_parser.add_argument("--name", help="Full Name of the subject")
    scan_parser.add_argument("--reddit", help="Reddit username")
    scan_parser.add_argument("--email", help="Email address (placeholder for now, not implemented yet)")

    compare_parser = subparsers.add_parser("compare", help="Compare two subjects side by side (coming soon)")

    demo_parser = subparsers.add_parser("demo", help="Generate a demo report with fictional data")

    args = parser.parse_args()

    if args.command == "compare":
        handle_compare(args)
    elif args.command == "demo":
        handle_demo(args)
    elif args.command == "scan":
        handle_scan(args, scan_parser)
