import unittest
from unittest.mock import Mock
from typing import Tuple, Dict, Optional

UserId = int
UserName = str
User = Tuple[UserId, UserName]

class Database:
    def __init__(self):
        self.data: Dict[UserId, User] = {}

    def add(self, user: User) -> None:
        self.data[user[0]] = user

    def get(self, user: UserId) -> Optional[User]:
        return self.data.get(user)

    def delete(self, user: UserId) -> bool:
        try:
            del self.data[user]
            return True
        except KeyError:
            return False

    def len(self) -> int:
        return len(self.data)

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.database = Database()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.database.data.clear()

    def test_add_get_delete(self) -> None:
        user = (1, "Kirill")
        self.database.add(user)
        self.assertEqual(self.database.get(1), user)
        self.assertTrue(self.database.delete(1))
        self.assertFalse(self.database.delete(1))
        self.assertIsNone(self.database.get(1))

    def test_len(self) -> None:
        test_cases = [
            ((2, "Nikita"), 1),
            ((3, "Egor"), 2),
            ((4, "Maks"), 3),
            ((5, "Alex"), 4),
        ]
        initial_len = self.database.len()
        for user, count in test_cases:
            with self.subTest(user=user, count=count):
                self.assertEqual(self.database.len(), initial_len + count - 1)
                self.database.add(user)
                self.assertEqual(self.database.len(), initial_len + count)

    def test_mock_database_get(self) -> None:
        mock_database = Mock(spec=Database)
        mock_database.get.return_value = (1, "Kirill")
        result = mock_database.get(1)
        self.assertEqual(result, (1, "Kirill"))
        mock_database.get.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
