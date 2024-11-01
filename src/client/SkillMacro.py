class SkillMacro:
    def __init__(self, skill1: int, skill2: int, skill3: int, name: str, shout: int, position: int):
        self._macro_id = None
        self.skill1 = skill1
        self.skill2 = skill2
        self.skill3 = skill3
        self.name = name
        self.shout = shout
        self.position = position

    @property
    def macro_id(self) -> int:
        return self._macro_id

    @macro_id.setter
    def macro_id(self, macro_id: int):
        self._macro_id = macro_id

    @property
    def skill1(self) -> int:
        return self._skill1

    @skill1.setter
    def skill1(self, skill1: int):
        self._skill1 = skill1

    @property
    def skill2(self) -> int:
        return self._skill2

    @skill2.setter
    def skill2(self, skill2: int):
        self._skill2 = skill2

    @property
    def skill3(self) -> int:
        return self._skill3

    @skill3.setter
    def skill3(self, skill3: int):
        self._skill3 = skill3

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def shout(self) -> int:
        return self._shout

    @shout.setter
    def shout(self, shout: int):
        self._shout = shout

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, position: int):
        self._position = position
