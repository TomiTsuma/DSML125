import argparse
from workflow import call
ag = argparse.ArgumentParser(description="Model update workflow")
ag.add_argument('-m', '--modeling-instructions', type=str,
                help='Path to the model update/optimization instructions csv file')
ag.add_argument('-p', '--phone-number', type=str,
                help='Path to the csv file containing phone numbers')
ag.add_argument('-e', '--evaluation-instructions', type=str,
                help='Path to the csv file containing the evaluation instructions')

args = ag.parse_args()

print(args)
modeling_instructions = args.modeling_instructions
phone_number = args.phone_number
evaluation_instructions = args.evaluation_instructions


def cli():
    call(modeling_instructions, phone_number, evaluation_instructions)


if __name__ == "__main__":
    cli()
