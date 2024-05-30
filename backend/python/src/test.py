from src.tests.Classes import Bots
import unittest

all_tests = [
    {
        "type": "Classes",
        "children": [
            {
                "name": "PodcastToShorts",
                "units": [
                    {"name": "full_run", "test": Bots.PodcastToShorts.FullRun},
                    {"name": "clip_shorts", "test": Bots.PodcastToShorts.ClipShorts},
                    {
                        "name": "download_video",
                        "test": Bots.PodcastToShorts.DownloadVideo,
                    },
                    {
                        "name": "get_full_transcript",
                        "test": Bots.PodcastToShorts.GetFullTranscript,
                    },
                ],
            },
        ],
    }
]


def main():
    print("0. Run all tests")
    for index, test in enumerate(all_tests):
        print(f"{index+1}. {test['type']}")
    choice = int(input("Enter the number of the test you want to run: "))
    if choice == "0":

        all_units_list = []
        for test_type in all_tests:
            for child in test_type["children"]:
                for unit in child["units"]:
                    all_units_list.append(unit["test"])

        run_suite(all_units_list)
        return

    test_type_dict = all_tests[choice - 1]
    print("0. Run all tests")
    for idx, child in enumerate(test_type_dict["children"]):
        print(f"{idx+1}. {child['name']}")

    choice = int(input("Enter the number of the test you want to run: "))
    if choice == "0":
        all_units_list = []
        for child in test_type_dict["children"]:
            for unit in child["units"]:
                all_units_list.append(unit["test"])

        run_suite(all_units_list)
        return

    selected_child = test_type_dict["children"][choice - 1]
    for idx, child in enumerate(selected_child["units"]):
        print(f"{idx+1}. {child['name']}")

    choice = int(input("Enter the number of the test you want to run: "))
    if choice == "0":
        all_units_list = []
        for unit in selected_child["units"]:
            all_units_list.append(unit["test"])

        run_suite(all_units_list)
        return

    test = unittest.TestLoader().loadTestsFromTestCase(
        selected_child["units"][choice - 1]["test"]
    )
    unittest.TextTestRunner().run(test)


def run_suite(all_units_list):
    suite = unittest.TestSuite()

    suite.addTests(
        [unittest.TestLoader().loadTestsFromTestCase(unit) for unit in all_units_list]
    )
    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    main()
