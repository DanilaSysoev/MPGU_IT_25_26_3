#!/usr/bin/sh

cd $1

echo "Cleaning..."
rm -vrf $2/migrations
rm -vf db.sqlite3
rm -vrf data
echo "OK"
