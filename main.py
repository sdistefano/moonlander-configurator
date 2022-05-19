from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def get_url_with_graphql():
    """ run graphql query against an url """
    url = "https://oryx.zsa.io/graphql"
    params = {}
    #run graphql query against url
    transport = RequestsHTTPTransport(url=url)
    client = Client(transport=transport)
    query = gql('''
        query getLayout($hashId: String!, $revisionId: String!, $geometry: String) {
  Layout(hashId: $hashId, geometry: $geometry, revisionId: $revisionId) {
    revision {
        zipUrl
    }
    __typename
  }
}
    ''')
    variables = {
    "hashId": "nj4xD",
    "geometry": "moonlander",
    "revisionId": "latest"
    }

    result = client.execute(query, variable_values=variables)

    return result['Layout']['revision']['zipUrl']

url = get_url_with_graphql()
url