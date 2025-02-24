import re
from kivy.properties import StringProperty
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
    sex = StringProperty("M")

    def set_sex(self, value):
        self.sex = value


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
    option = StringProperty("NEUTRE")

    def set_option(self, option):
        self.option = option

    def value(self):
        return self.option


class AbilityBox(BoxLayout):
    aptitude = StringProperty("APTE")

    def set_aptitude(self, aptitude):
        self.aptitude = aptitude


class CandidateTypeBox(BoxLayout):
    type_candidat = StringProperty("OFFICIEL")

    def set_type(self, type):
        self.type_candidat = type


class AttemptAndAvgBox(BoxLayout):
    attempts = StringProperty()
    moy_6e = StringProperty()
    moy_5e = StringProperty()
    moy_4e = StringProperty()
    moy_3e = StringProperty()

    def validation(self, type_candidat):
        motif_attempts = r"^(10|[0-9])$"
        motif_avg = r"^(20(\.0{1,2})?|1?\d(\.\d{1,2})?)$"
        if re.match(motif_attempts, self.attempts):
            if (type_candidat == "OFFICIEL" and re.match(motif_avg, self.moy_6e) and re.match(motif_avg, self.moy_5e)
                    and re.match(motif_avg, self.moy_4e) and re.match(motif_avg, self.moy_3e)):
                return self.attempts, self.moy_6e, self.moy_5e, self.moy_4e, self.moy_3e
            else:
                return self.attempts, None, None, None, None
        else:
            return False

    def clear_fields(self):
        self.attempts = ""
        self.moy_6e = ""
        self.moy_5e = ""
        self.moy_4e = ""
        self.moy_3e = ""
