from __future__ import print_function

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.service_account import ServiceAccountCredentials

from Person import Person

SCOPES = ['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive']

# The ID and range of a sample spreadsheet.
TEACHERS_NAMES_SHEET_ID = '12ql_eWmskf4VUjpOTByC3MPPxnbtZKVoMcblY9yPOo4'
TEACHERS_NAMES_PAGE_RANGE_NAME = 'Список сотрудников!A2:I'
TEACHERS_NAMES_CREDENTIAL_FILE = 'creds/credentials.json'

SCOPUS_TEACHER_INFO_SHEET_ID = '1p5Vw4SN1KQo1Oj6hLWfIl5NP2KKFJ9Fp9NeYlLJTAB0'
SCOPUS_TEACHER_INFO_PAGE_RANGE_NAME = 'Page1!A2:E'
SCOPUS_TEACHER_CREDENTIAL_FILE = 'creds/scopusinfo-f146e32d6814.json'


def getOurTeacher():
    flow = InstalledAppFlow.from_client_secrets_file(
        TEACHERS_NAMES_CREDENTIAL_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=TEACHERS_NAMES_SHEET_ID,
                                range=TEACHERS_NAMES_PAGE_RANGE_NAME).execute()
    values = result.get('values', [])
    ourTeacher = []

    for row in values:
        if len(row) == 9:
            ourTeacher.append(Person(str(row[1]).strip(), row[3]))

    print("We have info about " + str(len(ourTeacher)) + " teachers")
    return ourTeacher


def putInfoInDB(info_persons):
    creds = ServiceAccountCredentials.from_json_keyfile_name(SCOPUS_TEACHER_CREDENTIAL_FILE, SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    for infoPerson in info_persons:
        values = [
            [
                infoPerson.name,
                infoPerson.scopusId,
                infoPerson.document_count,
                infoPerson.cited_by_count,
                infoPerson.citation_count,
            ],
        ]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=SCOPUS_TEACHER_INFO_SHEET_ID, range=SCOPUS_TEACHER_INFO_PAGE_RANGE_NAME,
            valueInputOption='RAW', body=body).execute()

        print('Add info abbout' + infoPerson.name + ' : {0} cells appended.'.format(
            result.get('updates').get('updatedCells')))
