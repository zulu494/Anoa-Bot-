from dataset import stop_factory, Dataset
import typesense

dataset = Dataset()
client = typesense.Client({
    'api_key': '',
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'connection_timeout_seconds': 2
})

def get_berita(message):
    search_parameters = {
        'q': dataset.data_cleaning(message, stop_factory),
        'query_by': 'title',
        'num_typos': 2
    }

    return client.collections['hoax_articles'].documents.search(search_parameters)