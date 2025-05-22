# This is a sample Python script.
import json
import os

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

KVP_FILE = "D:\Games\The Riftbreaker\mods\large_main_gui\gui\styles.kvp"
OUTOUT_KVP_FILE = "new_styles.kvp"
# ie color red instead of color=red
KEY_VALUE_SEP = " "
QUOTE = '"'
BRACKET_START = "{"
BRACKET_END = "}"
PARSER_REMOVE_QUOTE = True # color "red" change to color=red instead of color="red" in json
CHAR_KEY_NAME = "char_height"
COLOR_KEY_NAME = "color"
COMMENT_KEY_NAME = "comment"
COMMENT_CONFIRMED = "confirmed"
KVP_COMMENT = "--"
MIN_CHAR_SIZE=0
MAX_CHAR_SIZE=22

CHAR_LARGER = 20
RED = "255, 0, 0"
BLUE = "0, 0, 255"
PURPLE = "255, 0, 255"
ORANGE = "255, 155, 0"
TEAL = "0, 255, 255"
BLACK = "0, 0, 0"
_new_colors_list = [RED, BLUE, ORANGE, PURPLE, TEAL, BLACK]
_color_index = 0



def parse_kvp_lines(lines):

   STATE_FIND_KVP_NAME = 0
   STATE_FIND_KVP_BRACKET_START = 1
   STATE_FIND_KVP_ITEM = 2
   STATE_FIND_KVP_BRACKET_END = 3
   BRACKET_START = "{"
   BRACKET_END = "}"

   state = STATE_FIND_KVP_NAME
   kvp_name = "unknown kvp name"
   line_num = 0

   all_kvp_dict_list = []
   one_kvp_dict = None
   for line in lines:
      line_num += 1
      line = line.strip()
      #print(f"line is {line}")

      if not line:
         # empty line, ignore
         continue
      # process comment including inline comment  abcd -- comment
      if KVP_COMMENT in line:
         if line.startswith(KVP_COMMENT):
            comment = line
            line=""
         else:
            line, comment = line.split(KVP_COMMENT)
            line = line.strip()
            #print(f"~~{line=}~~ {comment=}")
      else:
         comment =""
      if state == STATE_FIND_KVP_NAME:
         items_for_one_kvp = dict()
         kvp_name = line
         #if kvp_name=="hp_orange":
         print(f"{kvp_name}")
         one_kvp_dict = dict()
         kv_items=dict()
         comment_index=0
         one_kvp_dict[kvp_name]=kv_items

         all_kvp_dict_list.append(one_kvp_dict)

         state = STATE_FIND_KVP_BRACKET_START

      elif state == STATE_FIND_KVP_BRACKET_START:
         if line.startswith(BRACKET_START):

            state = STATE_FIND_KVP_ITEM

      elif state == STATE_FIND_KVP_ITEM:
         if line==BRACKET_END:
            # ended!
            state = STATE_FIND_KVP_NAME

         elif line:
            try:
               key,val = line.split(KEY_VALUE_SEP)
               val= val.strip(QUOTE)
            except Exception as e:
               print(f"wrong key value format in file line #{line_num} : {line} error:{e}")

            kv_items[key]=val

      else:
         raise Exception(f"error, line is not properly handled. {line}")

      if comment:
         comment_key_name = f"{COMMENT_KEY_NAME}{comment_index}"
         kv_items[comment_key_name] = f"{KVP_COMMENT}{comment}"  #--abcd
         comment_index += 1
         if COMMENT_CONFIRMED in comment:
            kv_items[COMMENT_CONFIRMED]=True
         continue
      #elif  state == STATE_FIND_KVP_BRACKET_END:
      #   state = STATE_FIND_KVP_NAME
      #   continue
   return all_kvp_dict_list


def parse_kvp_file(kvp_file=KVP_FILE):
   if not os.path.isfile(kvp_file):
      raise Exception(f"file not found! need to be full path {kvp_file}")
   with open(kvp_file) as filekvp:
      lines = filekvp.readlines()
      kvp_dict_list = parse_kvp_lines(lines)
   return kvp_dict_list


def parse_kvp_file_to_json_file(kvp_file=KVP_FILE):
   kvp_dict_list = parse_kvp_file(kvp_file)
   basename = os.path.basename(kvp_file)
   json_filename = basename + ".json"
   with open(json_filename, 'w') as file:
      json.dump(kvp_dict_list, file, indent=4)
      print(f"json file created {json_filename}")
   return kvp_dict_list


def change_char_and_color(data_dict, min, max, larger, color):

   char_size = int(data_dict[CHAR_KEY_NAME])
   # print(f"found char size! {char_size}")
   if char_size>=min and char_size <=max :
      print(f"found small char for {CHAR_KEY_NAME}: {char_size}")
      # if COLOR_KEY_NAME in data_items:
      #   data_items[data_items]
      if not color :
         global  _color_index
         _color_index = _color_index % len(_new_colors_list)
         color = _new_colors_list[_color_index]
         _color_index+=1
      data_dict[COLOR_KEY_NAME] = color
      orig_size = int(data_dict[CHAR_KEY_NAME])
      new_size = orig_size + larger
      data_dict[CHAR_KEY_NAME] = new_size
      data_dict[f"{COMMENT_KEY_NAME}_origsize"] = f'{KVP_COMMENT} orig {CHAR_KEY_NAME} "{orig_size}"'
      return True
   return False

def check_and_change_char_height(kvp, min, max):
   changed = False
   kvp_name = list(kvp.keys())[0]
   # print(f"kvp_name={kvp_name}")
   data_items = kvp[kvp_name]
   #print(f"{data_items=}")
   # print(f"    {k}={v}")
   if COMMENT_CONFIRMED in data_items:
      # skip since it's confirmed already
      print(f"skip enlarge char since it's already confirmed: {kvp_name}")
   else:
      if CHAR_KEY_NAME in data_items:
         changed = change_char_and_color(data_items, min=min, max=max, larger=CHAR_LARGER, color=None)
         if changed:
            print(f"changed, new {data_items=}")
   return changed
def analyze_kvp_json(kvp_list):
   total_changed = 0
   for kvp in kvp_list:
      # print(f"kvp={kvp}")
      changed = check_and_change_char_height(kvp, MIN_CHAR_SIZE, MAX_CHAR_SIZE)
      if changed:
         total_changed+=1
   return total_changed
def data_to_kvp_file(data, output_file, indent="\t"):
   # not good, bad format , json_string = json.dumps(data, indent=4)
   #space=" "*indent
   with open(output_file, "w") as outfile:
      for kvp in data:
         kvp_name = list(kvp.keys())[0]
         outfile.write(kvp_name + "\n")
         outfile.write(BRACKET_START + "\n")
         # print(f"kvp_name={kvp_name}")
         data_items = kvp[kvp_name]
         for k,v in data_items.items():
            if k.startswith(COMMENT_KEY_NAME):
               line=v
            elif k==COMMENT_CONFIRMED:
               # ignore confirm=True field, write nothing
               continue
               pass
            else:
               line = f"{k}{KEY_VALUE_SEP}{QUOTE}{v}{QUOTE}"
            line=f"{indent}{line}\n"
            outfile.write(line)
         outfile.write(BRACKET_END + "\n\n")



def main():
   kvp_list = parse_kvp_file_to_json_file(KVP_FILE)
   changed_count = analyze_kvp_json(kvp_list)
   print(f"changed {changed_count} items!")
   data_to_kvp_file(kvp_list, OUTOUT_KVP_FILE)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
