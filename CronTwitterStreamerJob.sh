if [[ ! `ps -eaf | grep twitterstreamer.py | grep python3 | grep -v grep` ]];then
     python3 twitterstreamer.py
fi
