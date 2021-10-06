from argparse import Namespace

from .commands import benchmarks_list, tools_list


def run_app(ns: Namespace):
    if ns.command == "benchmarks":
        benchmarks_list()

    if ns.command == "tools":
        tools_list(ns.benchmark)
