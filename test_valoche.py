from messenger import User

class TestModel:
    def test_user_repr(self):
        assert str(User(2, 'Alice')) == 'User(id=2, name=Alice)'

