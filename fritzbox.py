#!/usr/bin/env python 

# Python port of fritzbox.sh from https://github.com/ntop/ntopng/blob/dev/tools/fritzdump.sh

import requests
import sys


# This is the address of the router
FRITZIP=http://fritz.box

# This is the interface
IFACE="2-1"

# If you use password-only authentication use 'dslf-config' as username.
FRITZUSER=sys.argv[1] # read from input
FRITZPWD=sys.argv[2] # reads from input

SIDFILE="/tmp/fritz.sid"
url = "fritz.box"

if !FRITZUSER or !FRITZPWD:
	print(f'Missing user or password!')
	return 1

s = requests.Session()
with open('file.txt','a') as fp:
    with s.get(url,stream=True) as resp:
        for line in resp.iter_lines(chunk_size=1):
            fp.write(str(line))






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

echo "Capturing traffic on Fritz!Box interface $IFACE ..." 1>&2

# In case you want to use tshark instead of ntopng
wget --no-check-certificate -qO- $FRITZIP/cgi-bin/capture_notimeout?ifaceorminor=$IFACE\&snaplen=\&capture=Start\&sid=$SID | /usr/bin/tshark -r -

#wget --no-check-certificate -qO- $FRITZIP/cgi-bin/capture_notimeout?ifaceorminor=$IFACE\&snaplen=\&capture=Start\&sid=$SID | ntopng -i -