import re
sms = 1
en = 2
alg = 3
f = open(output_of_edit_script,"r")
new_sms = NEW_FILENAME
new_en = NEW_FILENAME
f1 = open(new_sms, "w")
f2 = open(new_en, "w")

for i, line in enumerate(f.readlines()):
  if i%3==0:
    line = re.sub(r'|', r'', line)
    line = line.replace("|","")
    line = line.replace(" ","")
    
    f1.write(line)
  if i%3==1:
    line = re.sub(r'|', r'', line)
    line = line.replace("|","")
    line = line.replace(" ","")
    
    f2.write(line)
    


