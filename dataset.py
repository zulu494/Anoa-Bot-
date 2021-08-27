from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
import csv

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()
stop_factory = StopWordRemoverFactory().get_stop_words()

class Dataset():
    label = []
    data = []

    def extract(self, dataset_location):
        with open(dataset_location, 'r', encoding='utf-8') as csvfile:
            dataset = csv.reader(csvfile, delimiter=',', quotechar='"')
            for message in dataset:
                self.label.append(message[0])
                self.data.append(self.data_cleaning(message[1]))

        return (self.label, self.data)

    def data_cleaning(self, message, custom_stopword = None):
        after_stem = stemmer.stem(message)
        remover = StopWordRemover(ArrayDictionary(custom_stopword if custom_stopword else stop_factory))
        after_stopword = remover.remove(after_stem)
        return after_stopword.strip()