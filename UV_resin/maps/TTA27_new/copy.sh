#!/bin/bash

for i in {1..4}
do
  # reactディレクトリにアクセスし、postとpreファイルをoutputディレクトリにコピー
  cp react${i}/automap/cleaned_post-mol calc/post${i}
  cp react${i}/automap/cleaned_pre-mol calc/pre${i}
  cp react${i}/automap/semi.map calc/semi.map${i}
done
