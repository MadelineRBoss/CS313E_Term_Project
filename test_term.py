import unittest

from Term_project import BootstrapBST

class TestBST(unittest.TestCase):

    def setUp(self):
        self.samples_not_made = True
        while self.samples_not_made:
            self.sample_input = "7 9 1 2 10 4 8 0 3 5 6 9 7 3 1 2 10 8 6 4 7 9 5 0 3 2 8 10 1 4 6 9 0 7 5 3 8 2 4 1 6 9 10 7 5 0 3 2 8 4"
            self.sample_input_list = self.sample_input.split()
            self.samples_not_made = False
            for ps, sample in enumerate(self.sample_input_list):
                if not sample.replace(".", "").isnumeric():
                    self.samples_not_made = True
                    break
                self.sample_input_list[ps] = float(sample)
            
        self.num_samples_input = 10000
        self.tree = BootstrapBST(self.sample_input_list)
        for __ in range(self.num_samples_input):
            self.tree.add_tree_value()

    def test_mean(self):
        self.assertEqual(round(self.tree.mean(), 2), 5.06)

    def test_median(self):
        self.assertEqual(self.tree.median(), 5.06)

    def test_range(self):
        self.assertEqual(self.tree.range(), 3.18)

    def test_se(self):
        self.assertEqual(round(self.tree.se(), 2), 0.44)

    def test_ci(self):
        ci_min, ci_max = self.tree.ci(95.0)
        self.assertEqual(ci_min, 4.19)
        self.assertEqual(ci_max, 5.92)

    def dif_mean_test(self):
        self.assertEqual(self.tree.test_mean(5.9, 1), .0308)

if __name__ == '__main__':
    unittest.main()