from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from io import BytesIO
from googleapiclient.discovery import build


def download_file(creds, real_file_id: str):
    """Downloads a file
  Args:
      creds: creds from google cloud console
      real_file_id: ID of the file to download
  Returns : IO object with location.

  """
    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)

        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        status = None
        while done is False:
            status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}.")

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None
    return file.getvalue()


def find_folder_by_id(folder_id: str, creds):
    # FIND FOLDER bY ID AND RETURN ALL CONTENTS within folder
    files = []
    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = (
                service.files()
                .list(
                    q=f"'{folder_id}' in parents",
                    fields="nextPageToken, files(id, name)",
                    # pasta informatica IB drive
                    driveId='0APd00tnWtQCJUk9PVA',
                    corpora='drive',
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                    pageToken=page_token,
                )
                .execute()
            )
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break

    except HttpError as error:
        print(f"An error occurred: {error}")
        files = None

    return files[0]
