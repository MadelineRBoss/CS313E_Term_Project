"""
Term Project

Team Member 1: Madeline Boss (mrb5727)
Team Member 2: Tariq Ali (taa2536)
"""
import random
import math

#dictonary of z values:
z_star_dict = {0.001: 3.090, 0.005: 2.576, 0.025: 1.960, 0.05: 1.645, 0.10: 1.282,
                0.15: 1.036, 0.20: 0.842, 0.25: 0.674, 0.30: 0.524, 0.35: 0.385,
                0.40: 0.253, 0.45: 0.125, 0.50: 0.000}

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

class Node():
    """
    Nodes for BST
    """
    def __init__ (self):
        pass

class BootstrapBST():
    """
    BST tree that represents Bootstrap samples
    """
    def __init__(self, base):
        self.base = base  #when intalized, keeps memory of base sample
        #rest to be implemented

    def create_tree(self):
        """
        create BST
        """
        #to be implemented
        return

    def medain(self):
        """
        returns medain of BST
        """
        #to be implemented
        return

    def range(self):
        """
        return BST range (i.e min and max of BST)
        """
        #to be implemented
        return

    def mean(self):
        """
        return mean of BST
        """
        #to be implemented
        return 0

    def sorted_tree(self):
        """
        return the BST sorted
        """
        #to be implemented
        return []
    
    def length(self):
        """
        return length of BST
        """
        #To be implemented
        return 1
    
    def sd(self):
        """
        gets standard deivation
        """
        #get local mean
        local_mean = self.mean()

        #get sum of variance squared
        sum_of_sqaures = 0
        for num in self.sorted_tree():
            #finds variance then square
            sum_of_sqaures += ((num - local_mean) ** 2) / (len(self.base()) - 1)
        #returns local sd
        return sum_of_sqaures

    def se(self):
        """
        gets standard error
        """
        return self.sd()/math.sqrt(self.length())


    def ci(self, alpha = 0.05):
        """
        Finds Confidence Interval (CI)

        input alpha: a value between 0 and .5

        output min: the minimum value in the CI
        output max: the maximum value in the CI
        """
        bst_mean = self.mean()
        bst_se = self.se()

        #checks if alpha is in the z star table then grabs it
        #potentially add binary search algorthim for next best value (lower value) instead of raising exceptions? <-- Get's Tariq's opinion
        if alpha not in z_star_dict.keys():
            raise NotImplementedError("z*star value not implemented")
        z_star = z_star_dict[alpha]

        ci_min = bst_mean - z_star*bst_se
        ci_max = bst_mean + z_star*bst_se

        return ci_min, ci_max

    def stat_signficant(self, value, alpha):
        """
        checks if sample value is in CI (or rather, if it's signficant)
        """
        ci_min, ci_max = self.ci(alpha)
        if ci_min < value < ci_max:
            return True
        return False
    
    def test_mean(self, test_mean):
        """
        finds a chance of a mean being reasonable in a sampling distrubution
        """
        chance = 0
        values = self.sorted_tree()
        for val in values:
            if val >= test_mean:
                chance += 1
        return round(chance/self.length(), 4)


def main():
    sample_input = input("What is your orginal sample? ")
    num_samples_input = input("How many bootstrap samples do you want to make (limit is 50)? ")
