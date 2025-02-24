import re

from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class FullNameBox(BoxLayout):
    first_name = StringProperty()
    last_name = StringProperty()

    def validation(self):
        motif = r"^[A-Z][a-zA-ZÀ-ÖØ-öø-ÿ\s'-]*$"
        if re.match(motif, self.first_name) and re.match(motif, self.last_name):
            return self.first_name, self.last_name
        else:
            return False

    def clear_fields(self):
        self.first_name = ""
        self.last_name = ""


class BirthBox(BoxLayout):
    birth_date = StringProperty()
    birth_place = StringProperty()

    def validation(self):
        motif_date = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(19|20)\d{2}$"
        motif_place = r"^[\w\s'’\-.,]+$"
        if re.match(motif_date, self.birth_date) and re.match(motif_place, self.birth_place):
            return self.birth_date, self.birth_place
        else:
            return False

    def clear_fields(self):
        self.birth_date = ""
        self.birth_place = ""


class SexBox(BoxLayout):
    sex = StringProperty()

    def set_sex(self, value):
        self.sex = value
        print(self.sex)


class NationalityAndSchoolBox(BoxLayout):
    nationality = StringProperty()
    school = StringProperty()

    def validation(self):
        motif_nat = r"^[A-Z]{3}$"
        motif_school = r"^[\w\s'’-]+$"
        if re.match(motif_nat, self.nationality) and re.match(motif_school, self.school):
            return self.nationality, self.school
        else:
            return False

    def clear_fields(self):
        self.nationality = ""
        self.school = ""


class OptionalTestBox(BoxLayout):
    option = ObjectProperty()

    def option_value(self, option):
        self.option = option
        print(self.option)


class AbilityBox(BoxLayout):
    aptitude = StringProperty()

    def aptitude_value(self, aptitude):
        self.aptitude = aptitude
        print(aptitude)


class CandidateTypeBox(BoxLayout):
    def value(self, officiel_radio):
        return "OFFICIEL" if officiel_radio.active else "INDIVIDUEL"


class AttemptAndAvgBox(BoxLayout):
    def validation(self, attempts, moy_6e, moy_5e, moy_4e, moy_3e, type_candidat):
        motif_attempts = r"^(10|[0-9])$"
        motif_avg = r"^(20(\.0{1,2})?|1?\d(\.\d{1,2})?)$"
        if re.match(motif_attempts, attempts):
            if (type_candidat == "OFFICIEL" and re.match(motif_avg, moy_6e) and re.match(motif_avg, moy_5e)
                    and re.match(motif_avg, moy_4e) and re.match(motif_avg, moy_3e)):
                return attempts, moy_6e, moy_5e, moy_4e, moy_3e
            else:
                return attempts, None, None, None, None
        else:
            return False

    def clear_fields(self, attempts, moy_6e, moy_5e, moy_4e, moy_3e):
        attempts.text = ""
        moy_6e.text = ""
        moy_5e.text = ""
        moy_4e.text = ""
        moy_3e.text = ""
