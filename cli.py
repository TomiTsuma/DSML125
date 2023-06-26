import argparse
from workflow import call
ag = argparse.ArgumentParser(description="Model update workflow")
ag.add_argument('-m', '--modeling-instructions', type=str,
                help='Path to the model update/optimization instructions csv file')
ag.add_argument('-p', '--phone-number', type=str,
                help='Path to the csv file containing phone numbers')
ag.add_argument('-e', '--evaluation-instructions', type=str,
                help='Path to the csv file containing the evaluation instructions')
ag.add_argument('-v', '--version', type=str,
                help='latest model version')


args = ag.parse_args()

print(args)
modeling_instructions = args.modeling_instructions
phone_number = args.phone_number
evaluation_instructions = args.evaluation_instructions
version = args.version


def cli():
    call(modeling_instructions, phone_number, evaluation_instructions, version)


if __name__ == "__main__":
    cli()
