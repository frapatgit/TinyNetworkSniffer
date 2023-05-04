#!/bin/bash

# From https://github.com/ntop/ntopng/blob/dev/tools/fritzdump.sh
# usage: fritzdump.sh [username] [password]


# This is the address of the router
FRITZIP=http://fritz.box

# Load configuration file
source config.ini

# Use configuration parameters
FRITZUSER=$username
FRITZPWD=$password


# This is the WAN interface
IFACE="2-1"

# If you use password-only authentication use 'dslf-config' as username.
#FRITZUSER=$1
#FRITZPWD=$2

SIDFILE="/tmp/fritz.sid"

if [ -z "$FRITZPWD" ] || [ -z "$FRITZUSER" ]  ; then echo "Username/Password empty. Usage: $0 <username> <password>" ; exit 1; fi

echo "Trying to login into $FRITZIP as user $FRITZUSER"

if [ ! -f $SIDFILE ]; then
  touch $SIDFILE
fi

SID=$(cat $SIDFILE)

# Request challenge token from Fritz!Box
CHALLENGE=$(curl -k -s $FRITZIP/login_sid.lua |  grep -o "<Challenge>[a-z0-9]\{8\}" | cut -d'>' -f 2)

# Very proprieatry way of AVM: Create a authentication token by hashing challenge token with password
HASH=$(perl -MPOSIX -e '
    use Digest::MD5 "md5_hex";
    my $ch_Pw = "$ARGV[0]-$ARGV[1]";
    $ch_Pw =~ s/(.)/$1 . chr(0)/eg;
    my $md5 = lc(md5_hex($ch_Pw));
    print $md5;
  ' -- "$CHALLENGE" "$FRITZPWD")
  curl -k -s "$FRITZIP/login_sid.lua" -d "response=$CHALLENGE-$HASH" -d 'username='${FRITZUSER} | grep -o "<SID>[a-z0-9]\{16\}" | cut -d'>' -f 2 > $SIDFILE

SID=$(cat $SIDFILE)

# Check for successfull authentification
if [[ $SID =~ ^0+$ ]] ; then echo "Login failed. Did you create & use explicit Fritz!Box users?" ; exit 1 ; fi

# check if directory exists
if [ ! -d "captures" ]; then
    mkdir "captures"
fi

echo "Capturing traffic on Fritz!Box interface $IFACE ..." 1>&2

while true; do
  echo "Capturing traffic on Fritz!Box interface $IFACE for 10 s ..."
  wget --no-check-certificate -qO- $FRITZIP/cgi-bin/capture_notimeout?ifaceorminor=$IFACE\&snaplen=\&capture=Start\&sid=$SID >> ./captures/capture_$(date +%Y%m%d_%H%M%S).pcap &
  wget_pid=$!
  trap "kill -- -$$" SIGINT
  counter=0
  timeout=10
  while [[ -n $(ps -e | awk '{print $1}' | grep "$wget_pid") ]] && [[ "$counter" -lt "$timeout" ]]; do
      sleep 1
      counter=$(($counter+1))
  done
  if [[ -n $(ps -e | awk '{print $1}' | grep "$wget_pid") ]]; then
    kill -s SIGKILL "$wget_pid"
    sleep 1
    echo "process capture terminated after 10 seconds ----- 2"
  fi
done