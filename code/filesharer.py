from filestack import Client


class FileSharer:
    """
    Generates a link for any given type of file
    """

    def __init__(self, filepath, api_key="A1tkLKtniT9SOGsVbNXbfz"):
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        client = Client(self.api_key)

        # I think this uploads the file to the cloud.
        # Then it prints the url of the uploaded file
        new_filelink = client.upload(filepath=f'{self.filepath}')
        return new_filelink.url