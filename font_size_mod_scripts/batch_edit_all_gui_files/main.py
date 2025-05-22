# This is a sample Python script.
import os

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# char_height "21.000" ie
Gui_File_Path = "D:\Games\The Riftbreaker\mods\larger_text_main_screen"
MAX_SIZE = 35  # ignore size >28
ENLARGE = 20
char_size_info_list = []
Keyword_Char_Height = 'char_height "'


def modify_char_size_line(line):
   tmp, orig_size = line.split(Keyword_Char_Height, 1)
   if '"' in orig_size:
      orig_size, tmp = orig_size.split('"')
      orig_size = float(orig_size)
      if orig_size < MAX_SIZE:
         new_size = orig_size + ENLARGE
         print(f"line has orig size {orig_size}, using new size {new_size}")
         new_line = f'char_height "{new_size}"'
         return new_line
   return line


def modify_all_char_height_lines(gui_file_fullpath, max_size=MAX_SIZE, delta=ENLARGE):
   with open(gui_file_fullpath, "r") as gui_file:
      lines = gui_file.readlines()

   with (open(gui_file_fullpath, "w") as gui_file):
      for line in lines:
         if Keyword_Char_Height in line:
            new_line = modify_char_size_line(line)

            print(f"new line is {new_line}")

         else:
            new_line = line
         new_line=f"{new_line}\n"
         gui_file.write(new_line)

   return


def modify_all_gui_file(file_path):
   # os.listdir(file_path)
   for (root, dirs, files) in os.walk(file_path, topdown=True):
      # print(f"root is {root}")
      # print(f"dirs is {dirs}")
      # print(f"files is {files}")

      for file in files:
         if file.endswith(".gui"):
            filefullpath = os.path.join(root, file)
            print(f"file is a .gui file {filefullpath}")
            modify_all_char_height_lines(filefullpath)


def print_hi(name):
   # Use a breakpoint in the code line below to debug your script.
   print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   modify_all_gui_file(Gui_File_Path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
