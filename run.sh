#!/bin/sh

usage()
{
    echo "usage: ./run.sh [[--help | -h]"
}

while [ "$1" != "" ]; do
    case $1 in
        -h | --help )           usage
                                exit
                                ;;
    esac
    shift
done

docker run -e TGTG_ACCESS_TOKEN="$TGTG_ACCESS_TOKEN" \
-e TGTG_REFRESH_TOKEN="$TGTG_REFRESH_TOKEN" -e TGTG_USER_ID="$TGTG_USER_ID" \
-e TGTG_COOKIE="$TGTG_COOKIE" -e TGTG_TELEGRAMBOT_TOKEN="$TGTG_TELEGRAMBOT_TOKEN" \
-e TGTG_TELEGRAMBOT_CHAT_ID="$TGTG_TELEGRAMBOT_CHAT_ID" --rm tgtgbot
