class PetCommand:
    def __init__(self, pet_id: int, skill_id: int, prob: int, inc: int):
        self.pet_id = pet_id
        self.skill_id = skill_id
        self.prob = prob
        self.inc = inc

    def get_pet_id(self) -> int:
        return self.pet_id

    def get_skill_id(self) -> int:
        return self.skill_id

    def get_probability(self) -> int:
        return self.prob

    def get_increase(self) -> int:
        return self.inc
