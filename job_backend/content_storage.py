from minio import Minio, error


class ContentStorageManager():
    def __init__(self):
        self.keyvault = StorageKeyVault()
        self.minio = Minio(self.keyvault.get_storage_address(),
                           access_key=self.keyvault.get_access_key(),
                           secret_key=self.keyvault.get_secret_key(),
                           secure=False)

    def save_content(self, bucket, content):
        _bucket = self._find_or_create_bucket(bucket)
        return self._save_content(_bucket, content)

    def _save_content(self, bucket, content):
        filename = f"{content.content_type}-{content.source_url.replace('/', '_')}"
        self.minio.put_object(bucket, filename,
                              content.bvalue, content.bvalue.getbuffer().nbytes)
        return bucket

    def _find_or_create_bucket(self, name):
        try:
            self.minio.make_bucket(name)
        except (error.BucketAlreadyExists, error.BucketAlreadyOwnedByYou):
            pass
        return name


class StorageKeyVault():
    def __init__(self):
        pass

    def get_storage_address(self):
        return "minio:9000"

    def get_access_key(self):
        return "login"

    def get_secret_key(self):
        return "password"
