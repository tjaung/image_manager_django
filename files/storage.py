from django.core.files.storage import FileSystemStorage

class PreserveNameFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Instead of generating a new name if the file exists,
        # simply overwrite the existing file.
        return name
