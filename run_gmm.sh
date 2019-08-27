#!/bin/bash
if [ $# -eq 0 ]; then
    ISR=0.19
else
ISR=$1
fi

cd ntpu-tts
rm -f output.wav
(cd ./programs/ta/ && sh run.sh &&
 cd ../pg/bp && ./bp $ISR ../../ta/all/8.txt ../../ta/all/9.txt &&
 cd ../psp && ./psp $ISR ../../ta/all/9.txt ../../ta/all/10.txt &&
 cd ../paf && ./paf $ISR ../../ta/all/10.txt ../../ta/all/11.xlab 0.025
 cd ../../ss/hts_engine_pc && sh ./synthesis.sh ../../../output.wav ../../ta/all/11.xlab)
 echo "[Success]"
