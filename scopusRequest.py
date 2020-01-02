from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor
import json

SCOPUS_CREDENTIAL_FILE = "creds/ScopusConfig.json"


def getInfoAboutTeacher(person):
    # Load configuration
    con_file = open(SCOPUS_CREDENTIAL_FILE)
    config = json.load(con_file)
    con_file.close()

    # Initialize client
    client = ElsClient(config['apikey'])
    client.inst_token = config['insttoken']

    # Initialize author with uri
    my_auth = ElsAuthor(
        uri='https://api.elsevier.com/content/author/author_id/' + str(person.scopusId))
    # Read author data, then write to disk
    if my_auth.read(client):
        return my_auth.data['coredata']
    else:
        print("Read author failed.")
