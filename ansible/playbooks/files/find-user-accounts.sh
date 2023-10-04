#!/bin/bash

echo "Server,Username,UID,GID,Groups,Home_Directory,Last_Login,account_lock,account_del"

while IFS=: read -r username _ uid gid _ home shell; do
    if [ "$uid" ] && [ "$uid" -ge 1000 ] && [ "$shell" != "/usr/sbin/nologin" ]; then
        groups=$(id -Gn "$username" | tr '\n' ',' | sed 's/,$//')  # Remove the trailing comma

        # Check last login date
        last_login_raw=$(lastlog -u "$username" | grep -v "Username")
        last_login=$(echo "$last_login_raw" | awk '{print $2}')
        if [ "$last_login" = "**Never" ]; then
            last_login="No Login"
            account_lock="Y"
            account_del="Y"
        else
            last_login=$(echo "$last_login_raw" | awk '{print $9, $5, $6}')
            last_login=$(lastlog -u "$username" | grep -v "Username" | awk '{gsub(/월/, "", $5); print $9"-"$5"-"$6}' | sed 's/Jan/01/;s/Feb/02/;s/Mar/03/;s/Apr/04/;s/May/05/;s/Jun/06/;s/Jul/07/;s/Aug/08/;s/Sep/09/;s/Oct/10/;s/Nov/11/;s/Dec/12/' | xargs -I{} date --date="{}" +"%Y-%m-%d")
            account_lock="N"
            account_del="N"
        fi

        # Set account lock and delete based on last login date
        if [ "$last_login" != "No Login" ]; then
            today=$(date '+%Y-%m-%d')
            last_login_timestamp=$(date -d "$last_login" '+%s')
            today_timestamp=$(date -d "$today" '+%s')

            days_difference=$(( (today_timestamp - last_login_timestamp) / 86400 ))

            if [ "$days_difference" -gt 90 ]; then
                account_lock="Y"
            fi

            if [ "$days_difference" -gt 365 ]; then
                account_del="Y"
            fi
        fi

        echo "$HOSTNAME,$username,$uid,$gid,$groups,$home,$last_login,$account_lock,$account_del"
    fi
done < /etc/passwd

