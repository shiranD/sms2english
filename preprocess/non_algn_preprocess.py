import sys
import os

if len(sys.argv) < 3:
  sys.strerr.write('Usage: non-alinged preprocess paralell corpus')
  sys.exit(1)

elif not os.path.exists(sys.argv[1]) or not os.path.exists(sys.argv[2]):
  sys.stderr.write('Error: one of the paths is invalid')
  sys.exit(1)

else:
  smsfile = sys.argv[1]
  enfile = sys.argv[2]
  outdir = sys.argv[3]
  smsf = open(smsfile, "r")
  enf = open(enfile, "r")
  smso = open(outdir+"/sms", "w")
  eno = open(outdir+"/en", "w")
  for sms_sen, en_sen in zip(smsf, enf):
    sms_sen = sms_sen.lower()
    en_sen = en_sen.lower()
    sms_sen = sms_sen.replace(" ", "^")
    en_sen = en_sen.replace(" ", "^")
    smso.write(sms_sen)
    eno.write(en_sen)
