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

    return round(bootstrap_mean,2)

class Node():
    """
    Nodes for BST
    """
    def __init__ (self, data_mean, lchild = None, rchild = None):
        self.mean = data_mean   # tree is based on mean value
        self.lchild = lchild
        self.rchild = rchild

class BootstrapBST():
    """
    BST tree that represents Bootstrap samples
    """
    def __init__(self, base):
        self.base = base  #when intalized, keeps memory of base sample
        self.root = None  #root of the tree
        #rest to be implemented (Tariq needs to implement)

    def add_tree_value(self):
        """
        Add to tree
        """
        #make new_node from function bootstrap
        new_node = Node(bootstrap(self.base))
        val = new_node.mean

        #checks if root is empty
        if self.root is None:
            self.root = new_node

        #finds next null value to replace with new_node
        else:
            current = self.root
            parent = self.root

            while current is not None:
                parent = current
                if val < current.mean:
                    current = current.lchild
                else:
                    current = current.rchild

            if val < parent.mean:
                parent.lchild = new_node
            else:
                parent.rchild = new_node

    def median(self):
        """
        returns median of BST
        """
        sorted_list = self.sorted_tree_mean()
        size = self.length()

        #checks if there's a list to get a median
        if size == 0:
            median = None

        #checks to see if the list has an even amount of values
        if size % 2 == 0:
            median = sorted_list[size // 2] + sorted_list[(size // 2) - 1]
            median /= 2
            median = round(median,2)

        #checks to see if the list has an odd amount of values
        else:
            median = sorted_list[len(sorted_list) // 2]

        return median

    def minimum(self):
        """
        Finds minimum value in BST
        """
        current = self.root
        parent = current

        while current is not None:
            parent = current
            current = current.lchild
        return parent

    def maximum(self):
        """
        Finds maximum value in BST
        """
        current = self.root
        parent = current
        while current is not None:
            parent = current
            current = current.rchild
        return parent

    def range(self):
        """
        return BST range (i.e min and max of BST)
        """
        min_bst = self.minimum().mean
        max_bst = self.maximum().mean

        #checks if the list is empty
        if min_bst is None or max_bst is None:
            return 0

        #return range
        return abs(round(max_bst - min_bst,2))

    def mean(self):
        """
        return mean of BST
        """

        if self.length() == 0:
            return None

        return sum(self.sorted_tree_mean()) / self.length()

    def sorted_tree_mean(self):
        """
        return the BST sorted
        """
        sorted_tree = []
        if self.root is None:
            return sorted_tree
        
        self.in_order_traversal(self.root, sorted_tree)
        return sorted_tree

    def in_order_traversal(self, node, sorted_tree):
        """
        helper for sorted tree
        """
        if node:
            self.in_order_traversal(node.lchild, sorted_tree)
            sorted_tree.append(node.mean)
            self.in_order_traversal(node.rchild, sorted_tree)

    def length(self):
        """
        return length of BST
        """
        return len(self.sorted_tree_mean())

    def se(self):
        """
        gets standard error
        """
        sum_of_sd = 0
        mean_list = self.sorted_tree_mean()
        BST_mean = self.mean()

        #checks if there's a list to get se
        if self.length() == 0:
            return None

        #finds standard error
        for m in mean_list:
            sum_of_sd += (m - BST_mean)**2
        se = math.sqrt(sum_of_sd/self.length())

        return se

    def ci(self, ci_percentage = 95):
        """
        Finds Confidence Interval (CI)

        input ci_percentage: a value between 0 and .5

        output min: the minimum value in the CI
        output max: the maximum value in the CI
        """
        bst_mean = self.mean()
        bst_se = self.se()

        #checks if there is a list to get ci
        if bst_mean is None:
            return None

        #checks if ci_percentage is in the z star table then grabs it
        #potentially add binary search algorthim for next best value?
        if ci_percentage/100 not in z_star_dict.keys():
            raise NotImplementedError("z*star value not implemented")
        z_star = z_star_dict[ci_percentage/100]

        #finds the min and max values in the condience interval
        ci_min = round(bst_mean - z_star*bst_se, 2)
        ci_max = round(bst_mean + z_star*bst_se, 2)

        return ci_min, ci_max

    def test_mean(self, test_mean, side):
        """
        finds a chance of a mean being reasonable in a sampling distrubution
        """
        #checks if BST is empty
        if self.length() == 0:
            return None

        #checks rarity of getting a value thats less than or greater than test_mean
        if side == 2:
            chance = 0
            values = self.sorted_tree_mean()
            #finds how many times in the BST there's a value less than or equal to the test_mean
            for val in values:
                if val <= test_mean:
                    chance += 1
                else:
                    break
            
            #returns the chance out of the length of the BST
            return round(chance/self.length(), 4)
        
        #checks rarity of getting a value thats greater than or greater than test_mean
        elif side == 1:
            chance = 0
            values = self.sorted_tree_mean()
            #finds how many times in the BST there's a value greaterthan or equal to the test_mean
            for val in range(len(values)-1, -1, -1):
                if values[val] >= test_mean:
                    chance += 1
                else:
                    break
                    
            #returns the chance out of the length of the BST
            return round(chance/self.length(), 4)


def main():
    """
    mainline logic
    """
    #gets input for base sample input
    samples_not_made = True
    while samples_not_made:
        sample_input = input("What is your orginal sample? ")
        sample_input_list = sample_input.split()
        samples_not_made = False
        for ps, sample in enumerate(sample_input_list):
            if not sample.replace(".", "").isnumeric():
                samples_not_made = True
                break
            sample_input_list[ps] = float(sample)

    #gets number of samples input
    num_samples_input = math.inf
    while num_samples_input > 10000 or num_samples_input <= 0:
        print("How many bootstrap samples do you want to make? Please make at minimum 1 sample. Please make it a whole number")
        print("Also please note while you can make up to 10,000 samples, if you make more than 1,000 you may run into an error")
        num_samples_input = input()
        if not num_samples_input.isnumeric():
            num_samples_input = math.inf
        else:
            num_samples_input = int(num_samples_input)

    #tree is created
    my_tree = BootstrapBST(sample_input_list)
    for __ in range(num_samples_input):
        my_tree.add_tree_value()
    #Make code to add bootstraps to tree

    choice = 0
    #interactions with BST
    while choice != 7:
        #Choices
        print()
        print("Now that we have made a sampling distrubution what would you like to do with it?")
        print("1) Find the mean")
        print("2) Find the median")
        print("3) Find the range")
        print("4) Find the standard error")
        print("5) Find a Confidence Interval for it")
        print("6) Test another mean against your sampling distrubution")
        print("7) End interface")

        choice = input("Please type the respetive number ")

        while not choice.isdigit() or 8 < int(choice) < 0:
            print()
            print("Now that we have made a sampling distrubution what would you like to do with it?")
            print("1) Find the mean")
            print("2) Find the median")
            print("3) Find the range")
            print("4) Find the standard error")
            print("5) Find a Confidence Interval for it")
            print("6) Test another mean against your sampling distrubution")
            print("7) End interface")

            choice = input("Please type the respetive number ")
        
        choice = int(choice)

        print()

        if 7 < choice < 1:
            print("Thats an invalid option")
            break

        # End Interface Option
        if choice == 7:
            break

        # print mean (Tariq needs to implement)
        if choice == 1:
            print(f'The mean is {round(my_tree.mean(), 2)}')

        # print median (Tariq needs to implement)
        if choice == 2:
            print(f'The median is {my_tree.median()}')

        # print range (Tariq needs to implement)
        if choice == 3:
            print(f'The range is {my_tree.range()}')

        # find Standard Error
        if choice == 4:
            print(f'The standard error is {round(my_tree.se(), 2)}')
        
        # find Confidence interval
        elif choice == 5:
            print("Choose your confidence level")
            print("80, 85, 90, 95, 97.5, 99, 99.5, 99.9")
            print()
            approved_ci_list = ["80", "85", "90", "95", "97.5", "99", "99.5", "99.9"]

            ci_choice = input()
            #check if option was a number
            while ci_choice not in approved_ci_list:
                print("Thats not an option, try again")
                print("Choose your confidence level")
                print("80, 85, 90, 95, 97.5, 99, 99.5, 99.9")
                ci_choice = input()
                print()
            ci_choice = float(ci_choice)

            #returns confidence interval
            ci_min, ci_max = my_tree.ci(ci_choice)
            print(f'Your {ci_choice}% Confidence Interval is {ci_min}-{ci_max}')

        # test different mean
        elif choice == 6:
            #get mean to test
            test_mean = ""
            while not test_mean.replace(".", "").isnumeric():
                test_mean = input("First, what mean do you want to test it with? ")
            test_mean = float(test_mean)

            #Get CI level
            print("Secondly, choose your confidence level")
            print("80, 85, 90, 95, 97.5, 99, 99.5, 99.9")
            approved_ci_list = ["80", "85", "90", "95", "97.5", "99", "99.5", "99.9"]
            ci_choice = input()
            #check if ci_choice was a number
            while ci_choice not in approved_ci_list:
                print("Thats not an option, try again")
                print("Choose your confidence level")
                print("80, 85, 90, 95, 97.5, 99, 99.5, 99.9")
                ci_choice = input()
                print()
            ci_choice = float(ci_choice)

            #contuine with testing mean

            ci_min, ci_max = my_tree.ci(ci_choice)

            #get which side to test
            side = 0
            while side not in ["1", "2"]:
                side = input("Do you expect this mean to be higher or lower than the expect mean? Type the coresponding number"
                            "\n1) Higher\n2) Lower\n")
            side = int(side)
    
            chance = my_tree.test_mean(test_mean, side)
            
            #checks if mean is in the CI (normal mean)
            if ci_max >= test_mean >= ci_min:
                print(f'With your confidence level of {ci_choice}% and probability of getting {test_mean}'
                        f' or rarer being {chance}, your mean is not abnormal')
            else:
                print(f'With your confidence level of {ci_choice}% and probability of getting {test_mean}'
                        f' or rarer being {chance}, your mean is abnormal')

main()
