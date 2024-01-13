import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument(
        "--step",
        "-s",
        choices=[
            "team_building",
            "specification",
            "system_design",
            "development",
            "execution",
        ],
        type=str,
        default=None,
        help="Step",
    )

    args = parser.parse_args()
    return vars(args)
