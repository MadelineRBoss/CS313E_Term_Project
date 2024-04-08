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
    def __init__ (self, data_mean, data_sd, lchild = None, rchild = None):
        self.mean = data_mean   # tree is based on mean value
        self.lchild = lchild
        self.rchild = rchild

class BootstrapBST():
    """
    BST tree that represents Bootstrap samples
    """
    def __init__(self, base):
        self.base = base  #when intalized, keeps memory of base sample
        #rest to be implemented (Tariq needs to implement)

    def add_tree_value(self, val):
        """
        Add to tree
        """
        new_node = Node(val)
        if self.base is None:
            self.base = new_node
        else:
            current = self.base
            parent = self.base

            while current is not None:
                parent = current
                if val < current.mean:
                    current = current.lChild
                else:
                    current = current.rChild

            if val < parent.mean:
                parent.lChild = new_node
            else:
                parent.rChild = new_node

    def median(self):
        """
        returns median of BST
        """
        sorted_list = self.sorted_tree_mean()
        median = sorted_list[len(sorted_list) // 2]
        
        return median

    def minimum(self):
        current = self.base
        parent = current
        while (current != None):
            parent = current
            current = current.lChild
        return parent

    def maximum(self):
        current = self.base
        parent = current
        while (current != None):
            parent = current
            current = current.rChild
        return parent

    def range(self):
        """
        return BST range (i.e min and max of BST)
        """
        min_bst = self.minimum()
        max_bst = self.maximum()
        
        return max_bst - min_bst

    def mean(self):
        """
        return mean of BST
        """
        #(Tariq needs to implement)
        return sum(self.sorted_tree_mean()) / self.length()

    def sorted_tree_mean(self):
        """
        return the BST sorted
        """
        sorted_tree = []
        self.in_order_traversal(self.base, sorted_tree)
        
        return sorted_tree

    def in_order_traversal(self, node, sorted_tree):
        if node:
            self.in_order_traversal(node.lChild, sorted_tree)
            sorted_tree.append(node.key)
            self.in_order_traversal(node.rChild, sorted_tree)

    def length(self):
        """
        return length of BST
        """
        #(Tariq needs to implement)
        return len(self.sorted_tree_mean())

    def se(self):
        """
        gets standard error
        """
        #Need to find a way to loop through sd values (another class method maybe?)
        sum_of_sd = 0
        mean_list = self.sorted_tree_mean()
        BST_mean = self.mean()
        for m in mean_list:
            sum_of_sd += (m - BST_mean)**2
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
        #potentially add binary search algorthim for next best value?
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
    #gets input for base sample and number of synethic samples
    sample_input = input("What is your orginal sample? ")
    num_samples_input = input("How many bootstrap samples do you want to make (limit is 50)? ")
    choice = 0

    #tree is created
    my_tree = BootstrapBST(sample_input)
    #Make code to add bootstraps to tree

    #interactions with BST
    while choice != 7:
        #Choices
        print("Now that we have made a sampling distrubution what would you like to do with it?")
        print("1) Find the mean")
        print("2) Find the median")
        print("3) Find the range")
        print("4) Find the standard error")
        print("5) Find a Confidence Interval for it")
        print("6) Test another mean against your sampling distrubution")
        print("7) End interface")
        choice = int(input("Please type the respetive number "))

        #Invalid Choice
        if 7 >= choice >= 1:
            print("Thats an invalid option")
            break

        # End Interface Option
        if choice == 7:
            break

        # print mean (Tariq needs to implement)
        if choice == 1:
            pass

        # print median (Tariq needs to implement)
        if choice == 2:
            pass

        # print range (Tariq needs to implement)
        if choice == 3:
            pass

        # find Standard Error
        if choice == 4:
            print(f'The standard error is {my_tree.se()}')
        
        # find Confidence interval
        elif choice == 5:
            print("Choose your confidence level")
            print("80\n85\n90\n95\n97.5\n99\n99.5\n99.9")
            approved_ci_list = [80, 85, 90, 95, 97.5, 99, 99.5, 99.5]
            ci_choice = float(input())
            if ci_choice not in approved_ci_list:
                print("Invalid choice. You'll be returned to the main menu")
                break
            ci_min, ci_max = my_tree.ci(ci_choice)
            print(f'Your {ci_choice}% Confidence Interval is {ci_min}-{ci_max}')

        # test different mean
        elif choice == 6:
            test_mean = float(input("First, what mean do you want to test it with? "))
            print("Secondly, choose your confidence level")
            print("80\n85\n90\n95\n97.5\n99\n99.5\n99.9")
            approved_ci_list = [80, 85, 90, 95, 97.5, 99, 99.5, 99.5]
            ci_choice = float(input())
            if ci_choice not in approved_ci_list:
                print("Invalid choice. You'll be returned to the main menu")
                break
            chance = my_tree.test_mean(test_mean)
            if chance >= 100 - ci_choice:
                print(f'With your confidence level of {ci_choice}% and probability of {test_mean}\
                       being {chance}, your mean is not abnormal')
            else:
                print(f'With your confidence level of {ci_choice}% and probability of {test_mean}\
                       being {chance}, your mean is abnormal')
