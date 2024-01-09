import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument(
        '--step', '-s',
        choices=['clarify', 'specification', 'development', 'execution'],
        type=str,
        default=None,
        help='Step'
    )

    # Parse the arguments.
    args = parser.parse_args()

    return vars(args)
