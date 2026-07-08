from nl_pddlgym.demo import run_all


import unittest


class TestSystem(unittest.TestCase):
    def test_system(self):
        print("WARNING: this test may take around a minute...")
        run_all(render=False, verbose=False)
        print("Test passed.")


if __name__ == "__main__":
    unittest.main()
