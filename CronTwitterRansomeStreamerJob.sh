if [[ ! `ps -eaf | grep twitterstreamerRansome.py | grep python3 | grep -v grep` ]];then
     python3 twitterstreamerRansome.py
fi
