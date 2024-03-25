"""
Term Project

Team Member 1: Madeline Boss (mrb5727)
Team Member 2: Tariq Ali (taa2536)
"""
import random

# Code can handle resampling of up to 10,000 with no real issue. Limitations for resampling will be based on binary tree run time
def bootstrap(base_sample, num):
    """
    inputs:
    base_sample: sample to create synethic samples
    num: number of samples to be creted

    output:
    final_list: list of final bootstrapped samples
    """
    final_list  = []
    sample_size = len(base_sample)

    for __ in range(num):
        temp_total = 0
        for __ in range(sample_size):
            random_pos = random.randint(0, sample_size - 1)
            temp_total += base_sample[random_pos]
        bootstrap_sample = temp_total/sample_size
        final_list.append(bootstrap_sample)

    return final_list

class BST():
    def __init__():
        pass

    def create_tree():
        pass

    def medain():
        pass

    def range():
        pass

    def mean():
        pass

def main():
    sample_input = input("What is your orginal sample? ")
    num_samples_input = input("How many bootstrap samples do you want to make (limit is 50)? ")


    
