import os
import shutil


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
                if not os.path.exists(dest_file) or not self.identical_objects(source_file, dest_file):
                    marked_files.append([source_file, dest_file])
            for name in dirs:
                source_dir = os.path.join(root, name)
                dest_dir = os.path.join(root.replace(src, dest), name)
                if not os.path.exists(dest_dir):
                    marked_dirs.append((source_dir, dest_dir))

        return marked_files, marked_dirs

    def identical_objects(self, source_file, dest_file):
        return True

    def valid_dest_files(self, marked_files):
        valid_flag = False
        while not valid_flag:
            valid_flag = self.identical_objects(marked_files[0], marked_files[1])
            if not valid_flag:
                self.upload_files(marked_files)

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
