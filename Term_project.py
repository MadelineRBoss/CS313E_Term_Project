"""
Term Project

Team Member 1: Madeline Boss (mrb5727)
Team Member 2: Tariq Ali (taa2536)
"""
import random
import math

random.seed(843960)

#dictonary of z values:
z_star_dict = {0.80: 1.2816, 0.85: 1.4408, 0.90: 1.6449, 0.95: 1.9600,
               0.975: 2.2414, 0.99: 2.5760, 0.995: 2.8070, 0.999: 3.2910}

#Code can handle resampling of up to 10,000 with no real issue. Limitations for resampling will be based on binary tree run time
def bootstrap(base_sample):
    """
    inputs:
    base_sample: sample to create synethic samples
    num: number of samples to be creted

    output:
    final_list: list of final bootstrapped samples
    """
    sample_size = len(base_sample)
    boot_sample = []

    temp_total = 0
    #create bootstrap sample
    for __ in range(sample_size):
        random_pos = random.randint(0, sample_size - 1)
        boot_sample.append(base_sample[random_pos])
        temp_total += base_sample[random_pos]
    
    #get mean
    bootstrap_mean = temp_total/sample_size

    #get sd
    square_of_sums = 0
    for num in boot_sample:
        square_of_sums += ((num - bootstrap_mean) ** 2)
    square_of_sums /= sample_size
    bootstrap_sd = math.sqrt(square_of_sums)

    return round(bootstrap_mean,2), round(bootstrap_sd,2)

class Node():
    """
    Nodes for BST
    """
    def __init__ (self, data_mean, data_sd, lchild = None, rchild = None):
        self.mean = data_mean   # tree is based on mean value
        self.sd = data_sd   # another data value that is stored for stats anaylsis 
        self.lchild = lchild
        self.rchild = rchild

class BootstrapBST():
    """
    BST tree that represents Bootstrap samples
    """
    def __init__(self, base):
        self.base = base  #when intalized, keeps memory of base sample
        #rest to be implemented

    def add_tree_value(self):
        """
        Add to tree
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

    def sorted_tree_mean(self):
        """
        return the BST sorted
        """
        #to be implemented
        return []
    
    def sd_list (self):
        """
        return the sds of the sorted BS
        """
        return []

    def length(self):
        """
        return length of BST
        """
        #To be implemented
        return 1

    def se(self):
        """
        gets standard error
        """
        #Need to find a way to loop through sd values (another class method maybe?)
        sum_of_sd = 0
        sd_values = self.sd_list()
        for sd in sd_values:
            sum_of_sd += sd
        se = sum_of_sd/self.length()

        return se

    def ci(self, ci_percentage = 0.95):
        """
        Finds Confidence Interval (CI)

        input ci_percentage: a value between 0 and .5

        output min: the minimum value in the CI
        output max: the maximum value in the CI
        """
        bst_mean = self.mean()
        bst_se = self.se()

        #checks if ci_percentage is in the z star table then grabs it
        #potentially add binary search algorthim for next best value (lower value) instead of raising exceptions? <-- Get's Tariq's opinion
        if ci_percentage not in z_star_dict.keys():
            raise NotImplementedError("z*star value not implemented")
        z_star = z_star_dict[ci_percentage]

        ci_min = bst_mean - z_star*bst_se
        ci_max = bst_mean + z_star*bst_se

        return ci_min, ci_max

    def stat_signficant(self, value, ci_percentage):
        """
        checks if sample value is in CI (or rather, if it's signficant)
        """
        ci_min, ci_max = self.ci(ci_percentage)
        if ci_min < value < ci_max:
            return True
        return False

    def test_mean(self, test_mean):
        """
        finds a chance of a mean being reasonable in a sampling distrubution
        """
        chance = 0
        values = self.sorted_tree_mean()
        for val in values:
            if val >= test_mean:
                chance += 1
        return round(chance/self.length(), 4)


def main():
    """
    mainline logic
    """
    sample_input = input("What is your orginal sample? ")
    num_samples_input = input("How many bootstrap samples do you want to make (limit is 50)? ")

my_data = [4, 3, 5, 6,2 ,2, 5,6 ,7, 8, 4,3, 2,2 ]
print(bootstrap(my_data))
