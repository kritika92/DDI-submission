#!/usr/bin/env python

import os
import sys
import argparse
import traceback
from projman.projman import Projman
from projman.exception import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', dest='type', help='The type of the project created from a specific template')
    parser.add_argument('-p', '--path', dest='path', help='The base path in which to create the project. If not supplied, it uses a default project path', type=int)
    subparsers = parser.add_subparsers(help='SUBCMD')
    
    # A list command
    list_parser = subparsers.add_parser('list', help='List the projects which have been created, optionally restricting the list to a specific type or types')
    list_parser.add_argument('-t', '--type', dest='type', help='The type of the project created from a specific template')
    list_parser.set_defaults(which='list')
    
    create_parser = subparsers.add_parser('create', help='Create a new project in PROJECT_PATH')
    create_parser.add_argument('-t', '--type', required=True, dest='type', help='The type of the project created from a specific template')
    create_parser.add_argument('-p', '--path', dest='path', help='The base path in which to create the project. If not supplied, it uses a default project path', type=int)
    create_parser.add_argument('name', help='New project to create')
    create_parser.set_defaults(which='create')

    delete_parser = subparsers.add_parser('delete', help='Delete an existing project. Optionally, restrict the deletion to a particular type within the project tree')
    delete_parser.add_argument('name', help='Project to delete')
    delete_parser.add_argument('-t', '--type', dest='type', help='The type of the project created from a specific template')
    delete_parser.set_defaults(which='delete')

    types_parser = subparsers.add_parser('types', help='List the types of projects which may be created')
    types_parser.set_defaults(which='types')

    describe_parser = subparsers.add_parser('describe', help='Pretty print the structure of a project template')
    describe_parser.add_argument('-t', '--type', required=True, dest='type', help='The type of the project created from a specific template')
    describe_parser.set_defaults(which='describe')

    args = parser.parse_args()

    if args.which == 'types':
        projman = Projman()
        print projman.types()
    elif args.which == 'list':
        projman = Projman()
        projman.list(args.type)
    elif args.which == "create":
        projman = Projman()
        projman.create(args.name, args.type, args.path)
    elif args.which == "delete":
        projman = Projman()
        projman.delete(args.name, args.type)
    elif args.which == "describe":
        projman = Projman()
        projman.describe(args.type)

if __name__ == '__main__':
    try:
        sys.exit(main())
    except TemplateError as e:
        sys.stderr.write("Error: %s\n" % str(e))
        traceback.print_exc(file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        sys.stderr.write("Error: %s\n" % str(e))
        traceback.print_exc(file=sys.stderr)
        sys.exit(4)
