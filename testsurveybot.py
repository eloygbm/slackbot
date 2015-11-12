
import slackbot.surveybot
import unittest


class VoteBadInput(unittest.TestCase):
    def testNoArguments(self):
        """vote should fail with no arguments"""
        result = slackbot.surveybot.vote("testuser","")
        self.assertEqual("Parameters ERROR - Example to vote option Green for survey #2: `/survey reply 2 Green`", result)

    def testFewArguments(self):
        """vote should fail with less arguments"""
        result = slackbot.surveybot.vote("testuser","lala")
        self.assertEqual("Parameters ERROR - Example to vote option Green for survey #2: `/survey reply 2 Green`", result)


if __name__ == "__main__":
    unittest.main()

