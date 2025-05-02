import pytest


UserId = int
UserName = str
User = tuple[UserId, UserName]


class Database:
    def __init__(self):
        self.data: dict[UserId, User] = {}

    def add(self, user: User) -> None:
        self.data[user[0]] = user

    def get(self, user: UserId) -> User | None:
        return self.data.get(user)

    def delete(self, user: UserId) -> bool:
        try:
            del self.data[user]
            return True
        except KeyError:
            return False

    def len(self) -> int:
        return len(self.data)


@pytest.fixture(scope="session")
def database() -> Database:
    return Database()


def test_add_get_delete(database: Database) -> None:
    user = (1, "Kirill")
    database.add(user)
    assert database.get(1) == user
    assert database.delete(1) is True
    assert database.delete(1) is False
    assert database.get(1) is None


@pytest.mark.parametrize(
    "user, count",
    [
        ((1, "Kirill"), 1),
        ((2, "Nikita"), 2),
        ((3, "Egor"), 3),
        ((4, "Maks"), 4),
    ]
)
def test_len(user: User, count: int, database: Database) -> None:
    assert database.len() == count - 1
    database.add(user)
    assert database.len() == count
