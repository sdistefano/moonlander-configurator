import os
import sys

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def get_url_with_graphql(keyboard):
    """ run graphql query against an url """
    hashId = {
        "moonlander": "nj4xD",
        "voyager": "qBEqz"
    }[keyboard]
    url = "https://oryx.zsa.io/graphql"
    params = {}
    # run graphql query against url
    transport = RequestsHTTPTransport(url=url)
    client = Client(transport=transport)
    query = gql('''
        query getLayout($hashId: String!, $revisionId: String!, $geometry: String) {
  layout(hashId: $hashId, geometry: $geometry, revisionId: $revisionId) {
    revision {
        zipUrl
    }
    __typename
  }
}
    ''')
    variables = {
        "hashId": hashId,
        "geometry": keyboard,
        "revisionId": "latest"
    }

    result = client.execute(query, variable_values=variables)

    return result['layout']['revision']['zipUrl']


def download_unzip_file(url):
    """ download and unzip a file """
    import requests
    import zipfile
    import io
    import os
    dir_name = {
        "voyager": "voyager_silvio-voyager_source",
        "moonlander": "moonlander_silvio_source"
        }[keyboard]

    dest = f"C:\\Users\\sdist\\qmk_firmware\\keyboards\\{keyboard}\\keymaps\\oryx"

    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    for file in ['config.h', 'keymap.c', 'rules.mk']:
    #for file in ['keymap.c', 'rules.mk']:
        with open(dest + '/' + file, 'wb') as f:
            f.write(z.read(f'{dir_name}/' + file))
    z.close()


def append_after_line(content, line, append):
    """ append a line after a line in a string """
    index = content.find(line)
    if index == -1:
        return content
    return "\n".join([content[:index], line, append, content[index + len(line):]])


def append_code():
    with(open(b'C:\Users\sdist\qmk_firmware\keyboards\moonlander\keymaps\oryx\keymap.c', 'r+')) as f:
        cont = f.read()
        back_to_0 = 'layer_move(0); return false;'
        back_to_3 = 'layer_move(3); return false;'
        # insert mode I/O/A
        cont = append_after_line(cont, "SEND_STRING(SS_TAP(X_RIGHT));", back_to_0)
        cont = append_after_line(cont, "SEND_STRING(SS_TAP(X_END) SS_DELAY(100) SS_TAP(X_ENTER));", back_to_0)
        # del functions D/E/B
        cont = append_after_line(cont,
                                 "SEND_STRING(SS_TAP(X_HOME) SS_DELAY(100) SS_LSFT(SS_TAP(X_END)) SS_DELAY(100) SS_TAP(X_DELETE) SS_DELAY(100) SS_TAP(X_DELETE));",
                                 back_to_3)
        cont = append_after_line(cont, "SEND_STRING(SS_LCTL(SS_TAP(X_DELETE)));", back_to_3)
        cont = append_after_line(cont, "SEND_STRING(SS_LCTL(SS_TAP(X_BSPACE)));", back_to_3)
        # change functions
        cont = append_after_line(cont, "SEND_STRING(SS_RCTL(SS_TAP(X_DELETE)));", back_to_0)
        cont = append_after_line(cont, "SEND_STRING(SS_RCTL(SS_TAP(X_BSPACE)));", back_to_0)

        f.seek(0)
        f.write(cont)


def flash():
    command = f'''C:\QMK_MSYS\conemu\ConEmu64.exe -NoSingle -NoUpdate -run "C:\\QMK_MSYS\\usr/bin/bash" --login -c "(cd /c/Users/sdist/qmk_firmware/ ; qmk flash -kb {keyboard} -km oryx)"'''
    os.system(command)

def fix_steno():
    with(open(f'C:\\Users\\sdist\\qmk_firmware\\keyboards\\{keyboard}\\keymaps\\oryx\\config.h', 'r+')) as f:
        cont = f.read()
        cont = "\n".join([cont, '\n#define STENO_COMBINEDMAP 1'])
        f.seek(0)
        f.write(cont)
    with(open(f'C:\\Users\\sdist\\qmk_firmware\\keyboards\\{keyboard}\\keymaps\\oryx\\keymap.c', 'r+')) as f:
        cont = f.read()
        cont = cont.replace('STN_NC', 'STN_EU')
        f.seek(0)
        f.write(cont)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Which keyboard?")
    keyboard = sys.argv[1]

    url = get_url_with_graphql(keyboard)
    download_unzip_file(url)
    if keyboard == "moonlander":
        append_code()
    if keyboard == "voyager":
        fix_steno()
    flash()
