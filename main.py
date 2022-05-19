import os
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

def download_unzip_file(url):
    """ download and unzip a file """
    import requests
    import zipfile
    import io
    import os

    dest = b"C:\Users\sdist\qmk_firmware\keyboards\moonlander\keymaps\default"

    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    # for file in ['config.h', 'keymap.c', 'rules.mk']:
    for file in ['keymap.c', 'rules.mk']:
        with open(dest.decode('utf-8') + '/' + file, 'wb') as f:
            f.write(z.read('moonlander_silvio_source/' + file))
    z.close()

def append_after_line(content, line, append):
    """ append a line after a line in a string """
    index = content.find(line)
    if index == -1:
        return content
    return "\n".join([content[:index], line, append, content[index+len(line):]])

def append_code():
    with(open(b'C:\Users\sdist\qmk_firmware\keyboards\moonlander\keymaps\default\keymap.c', 'r+')) as f:
        cont = f.read()
        back_to_0 = 'layer_move(0); return false;'
        back_to_3 = 'layer_move(3); return false;'
        cont = append_after_line(cont, "SEND_STRING(SS_TAP(X_RIGHT));", back_to_0)
        cont = append_after_line(cont, "SEND_STRING(SS_TAP(X_END) SS_DELAY(100) SS_TAP(X_ENTER));", back_to_0)
        cont = append_after_line(cont,
         "SEND_STRING(SS_TAP(X_HOME) SS_DELAY(100) SS_LSFT(SS_TAP(X_END)) SS_DELAY(100) SS_TAP(X_DELETE) SS_DELAY(100) SS_TAP(X_DELETE));",
          back_to_3)
        f.seek(0)
        f.write(cont)


def flash():
    command = b'''C:\QMK_MSYS\conemu\ConEmu64.exe -NoSingle -NoUpdate -run "C:\QMK_MSYS\usr/bin/bash" --login -c "(cd /c/Users/sdist/qmk_firmware/ ; pwd; ls ; source ~/.env ; QMK_VERBOSE=True qmk flash -kb moonlander -km default)"'''
    os.system(command.decode('utf8'))

url = get_url_with_graphql()
download_unzip_file(url)
append_code()
flash()