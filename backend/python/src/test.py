import tests
import unittest

# TODO: refactor this so that it takes in a dictionary for each class. The user can select a class, and choose to run a specific test for that class, or run all tests for that class. Another option is to run all tests for all classes.
all_tests = {
    # "test_create_channel": tests.TestCreateChannel,
}

def main():
    # Option 0: Run all tests
    print("0. Run all tests")
    for index, test in enumerate(all_tests):
        print(f"{index+1}. {test}")
    choice = int(input("Enter the number of the test you want to run: "))
    if choice == "0":
        # run all tests
        suite = unittest.TestSuite()
        # continue
        suite.addTests([unittest.TestLoader().loadTestsFromTestCase(test) for test in tests.values()])
        unittest.TextTestRunner().run(suite)
    test = list(tests.values())[choice-1]
    test = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner().run(test)

if __name__ == "__main__":
    main()
