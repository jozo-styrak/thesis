# class representing semantic role which translates to verbalex roles
class SemanticRole:


    def __init__(self, first_lvl_role, second_lvl_role):
        self.first_level_role = first_lvl_role
        self.second_level_role = second_lvl_role

    def __str__(self):
        return '{ Semantic roles: ' + self.second_level_role + ' as ' + self.first_level_role + ' }'