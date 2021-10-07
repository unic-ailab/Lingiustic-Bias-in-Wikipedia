import pandas as pd
from utils import load_revisions, get_values_for_tables

# Define paths to revisions files
politic_path = "/home/emath/Data Science/AI Lab-Research/Wikipedia Project/Data/politicians.json"
scientist_path = "/home/emath/Data Science/AI Lab-Research/Wikipedia " \
                 "Project/Data/most_influential_scientist_cleaned.json"
female_scientists_path = "/home/emath/Data Science/AI Lab-Research/Wikipedia " \
                 "Project/Data/notable_women_scientists.json"
athletes_path = "/home/emath/Data Science/AI Lab-Research/Wikipedia Project/Data/athletsWithSixOlympicAppearances.json"

# Define notable women lists
female_politic = [
    "Angela Merkel", "Mette Frederiksen", "Katerina Sakellaropoulou",
    "Sanna Marin", "Rose Christiane Raponda", "Katrín Jakobsdóttir",
    "Ingrida Šimonytė", "Jacinda Ardern", "Erna Solberg", "Sahle-Work Zewde"
]

female_scientist = [
    "Jane Goodall", "Lene Hau", 'Emmanuelle Charpentier', 'Jennifer Doudna', 'Frances Arnold',
    'Ada E. Yonath', 'Dorothy Crowfoot Hodgkin', 'Irène Joliot-Curie', 'Marie Sklodowska-Curie',
    'Frances "Fran" Elizabeth Allen', 'Barbara Liskov', 'Shafi Goldwasser', 'Mirella Lapata',
    'Diane Kelly', 'Jaime Teevan', 'Donna Strickland', 'Maria Goeppert-Mayer', 'Gerty Cori',
    'Rosalyn Yalow', 'Barbara McClintock', 'Rita Levi-Montalcini', 'Gertrude B. Elion',
    'Christiane Nüsslein-Volhard', 'Linda B. Buck', 'Françoise Barré-Sinoussi', 'Carol W. Greider',
    'Elizabeth H. Blackburn', 'May-Britt Moser', 'Youyou Tu']

female_athletes = [
    'Janice York Romary', 'Lia Manoliu', 'Christilot Hanson-Boylen', 'Marja-Liisa Kirvesniemi', 'Tessa Sanderson',
    'Christine Stückelberger', 'Nonka Matova', 'Emese Hunyady', 'Birgit Fischer', 'Elisabeta Oleniuc Lipă',
    'Agathi Kassoumi', 'Anne Abernathy', 'Gerda Weissensteiner', 'Kateřina Neumannová', 'Susan Nattrass',
    'Kyra Kyrklund', 'Fabienne Diato-Pasetti', 'Maria Mutola', 'Anna Orlova', 'Evgeniya Radanova', 'Štěpánka Hilgertová',
    'Mönkhbayar Dorjsurengiin', 'Natalia Valeeva'
]

# Load revisions from politicians biographies
politicians_revisions = load_revisions(politic_path)
scientists_revisions = load_revisions(scientist_path)
female_scientists_revisions = load_revisions(female_scientists_path)
scientists_revisions.update(female_scientists_revisions)
athletes_revisions = load_revisions(athletes_path)

# Load dictionaries
with open("../data/action_verbs.txt", "r") as f_reader:
    action_verbs = set([line.strip() for line in f_reader.readlines()])
        
with open("../data/state_verbs.txt", "r") as f_reader:
    state_verbs = set([line.strip() for line in f_reader.readlines()])

with open("../data/strong_verbs.txt", "r") as f_reader:
    strong_verbs = set([line.strip() for line in f_reader.readlines()])

with open("../data/pos_words_politics.txt", "r") as f_reader:
    pos_words_p = set([line.strip() for line in f_reader.readlines()])

with open("../data/pos_words_scientits.txt", "r") as f_reader:
    pos_words_s = set([line.strip() for line in f_reader.readlines()])

with open("../data/neg_words_politics.txt", "r") as f_reader:
    neg_words_p = set([line.strip() for line in f_reader.readlines()])

with open("../data/neg_words_scientits.txt", "r") as f_reader:
    neg_words_s = set([line.strip() for line in f_reader.readlines()])

with open("../data/pos_words_athletes.txt", "r") as f_reader:
    pos_words_a = set([line.strip() for line in f_reader.readlines()])

with open("../data/neg_words_athletes.txt", "r") as f_reader:
    neg_words_a = set([line.strip() for line in f_reader.readlines()])


# set of positive words across politicians and scientists    
pos_words = pos_words_p.union(pos_words_s, pos_words_a)

# set of negative words across politicians and scientists
neg_words = neg_words_p.union(neg_words_s, neg_words_a)

columns = ["name", "revId", "userId", "date", "gender", "role",
           "length", "posWords", "negWords", "descrVerbs",
           "actionVerbs", "stateVerbs", "adjectives", "meanAbstractLevel"]

print("Politicians!!! -------------------------------")
politicians_list = get_values_for_tables(politicians_revisions, "politician", female_politic, pos_words, neg_words,
                                         list(state_verbs), list(strong_verbs), list(action_verbs))
print("Scientists!!!---------------------------------")
scientists_list = get_values_for_tables(scientists_revisions, "scientist", female_scientist, pos_words, neg_words,
                                        list(state_verbs), list(strong_verbs), list(action_verbs))
print("Scientists!!!---------------------------------")
athletes_list = get_values_for_tables(athletes_revisions, "athlete", female_athletes, pos_words, neg_words,
                                      list(state_verbs), list(strong_verbs), list(action_verbs))

values = politicians_list+scientists_list+athletes_list
        
revisions_df = pd.DataFrame(data=values, columns=columns)

revisions_df.to_csv("../data/revisions.txt")
