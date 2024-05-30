from src.tests.Classes import Bots
import unittest

all_tests = [
    {
        "PodcastToShorts": {
            "all_tests": [
                {"name": "full_run", "test": Bots.PodcastToShorts.FullRun},
                {"name": "clip_shorts", "test": Bots.PodcastToShorts.ClipShorts},
                {"name": "download_video", "test": Bots.PodcastToShorts.DownloadVideo},
                {"name": "get_full_transcript", "test": Bots.PodcastToShorts.GetFullTranscript},
            ],
        },
    }
]

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
