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

    args = parser.parse_args()
    return vars(args)
