from unrar import rarfile

class RarUtils:
  @staticmethod
  def unrar(fullpath_filename: str, output_path:str):
    with rarfile.RarFile(fullpath_filename) as rf:
      rf.extractall(output_path)