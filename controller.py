import filecmp
import os
import shutil
import hashlib


class UploaderController:
    def upload_item(self, item, thread_name):
        raise NotImplementedError('function not implemented')

    def validate_upload(self):
        raise NotImplementedError('function not implemented')


class MockedUploaderController(UploaderController):
    def upload_item(self, item, thread_name):
        print(f"uploading {item} with {thread_name}")

        src = item["Source_folder"]
        dest = item["Destination_bucket"]
        marked_files, marked_dirs = self.collect_source(src, dest)
        self.create_dirs_in_target(marked_dirs)
        self.upload_files(marked_files)
        self.valid_dest_files(marked_files)

        print(f"done_uploading with {thread_name}")

    def collect_source(self, src, dest):
        marked_files = []
        marked_dirs = []
        for root, dirs, files in os.walk(src):
            for name in files:
                source_file = os.path.join(root, name)
                dest_file = os.path.join(root.replace(src, dest), name)
                if not os.path.exists(dest_file) or not filecmp.cmp(source_file, dest_file, shallow=True):
                    marked_files.append([source_file, dest_file])
            for name in dirs:
                source_dir = os.path.join(root, name)
                dest_dir = os.path.join(root.replace(src, dest), name)
                if not os.path.exists(dest_dir):
                    marked_dirs.append((source_dir, dest_dir))

        return marked_files, marked_dirs

    @staticmethod
    def digest_file(file):
        hash_md5 = hashlib.md5()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def valid_dest_files(self, marked_files):
        for file in marked_files:
            while True:
                digest_source = self.digest_file(file[0])
                digest_dest = self.digest_file(file[1])
                if digest_source != digest_dest:
                    print(f"{file[0]} was not uploaded correctly. Trying again...")
                    self.upload_files(marked_files)
                else:
                    break

    @staticmethod
    def create_dirs_in_target(marked_dirs):
        for dir in marked_dirs:
            os.makedirs(dir[1])
            print(f"uploading folder: {dir[1]}")

    @staticmethod
    def upload_files(marked_files):
        for file in marked_files:
            shutil.copy2(file[0], file[1])
            print(f"uploading file {file[1]}")
