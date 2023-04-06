import unittest
from SkipList.sl import SkipList


class SkipListTests(unittest.TestCase):
    def test_can_create(self):
        # Arrange

        # Act
        sl = SkipList(4)

        # Assert
        self.assertIsNotNone(sl)

    def test_can_insert(self):
        # Arrange
        items = [10, 4, 55, 1, 15]
        sl = SkipList(3)
        sl.beta = 0.5

        # Act
        for i in items:
            sl.insert(i, i + 100)

        # Assert
        self.assertEqual((True, 110), sl.find(10))
        self.assertEqual((True, 104), sl.find(4))
        self.assertEqual((True, 155), sl.find(55))
        self.assertEqual((True, 101), sl.find(1))
        self.assertEqual((True, 115), sl.find(15))

        self.assertEqual((False, None), sl.find(0))
        self.assertEqual((False, None), sl.find(54))
        self.assertEqual((False, None), sl.find(56))
