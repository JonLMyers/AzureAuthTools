import os, uuid
from azure.storage.blob import (
    BlobServiceClient,
    BlobClient,
    ContainerClient,
    __version__,
)


class StorageAccount:
    blob_client = None
    containers = []

    def __init__(self, connectionString):
        self.connectionString = connectionString

    def Connect(self):
        self.blob_client = BlobServiceClient.from_connection_string(
            self.connectionString
        )

    def ListContainers(self):
        all_containers = self.blob_client.list_containers(include_metadata=True)
        for container in all_containers:
            print(container["name"], container["metadata"])
        return all_containers

    def ListBlobs(self, container):
        container_client = self.blob_client.get_container_client(container)
        blob_list = container_client.list_blobs()
        return blob_list

    def DownloadBlob(self, blobName, containerName):
        blob_client = self.blob_client.get_blob_client(
            container=containerName, blob=blobName
        )
        # No need to download this. Just encrypt in memory
        with open(
            "/home/jomy/Git/AzureAuthTools/AzInterface/temp/{0}".format(blobName), "wb"
        ) as download_file:
            download_file.write(blob_client.download_blob().readall())


storage_account = StorageAccount("")

storage_account.Connect()
storage_account.ListContainers()
blobs = storage_account.ListBlobs("test")
for blob in blobs:
    print(blob["name"])
storage_account.DownloadBlob("ptrmp.scandata.addresslist", "test")
