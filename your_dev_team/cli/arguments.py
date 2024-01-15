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
            "improvement",
            "deployment",
        ],
        type=str,
        default=None,
        help="Step",
    )
    parser.add_argument(
        "--project_name",
        "-p",
        type=str,
        default=None,
        help="Project name",
    )
    parser.add_argument(
        "--japanese",
        "-j",
        type=bool,
        default=False,
        help="Japanese mode",
    )

    args = parser.parse_args()
    return vars(args)
