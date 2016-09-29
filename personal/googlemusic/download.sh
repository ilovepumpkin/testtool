#!/bin/sh

keyword=$2
songsFile=$1

downMusic(){
    local songUrl="$1"
    local outputDir="$4"
    local mp3Path="$4/$2.mp3"
    local lyricsPath="$4/$2.lrc"

    [ ! -d "$outputDir" ] && mkdir -p "$outputDir"

    [ ! -f "$mp3Path" ] && wget --retry-connrefused -O "$mp3Path" "$1"
    [ -n "$3" ] && [ ! -f "$lyricsPath" ] && wget --retry-connrefused -O "$lyricsPath" "$3"
}

readXmlAttr(){
    echo "$1"|sed 's/<\//</g'|awk -F "<$2>" '{print $2}'
}

while read line        
    do        
        songXml=$(curl -s "$line")
        songId=$(readXmlAttr "$songXml" "id") 
        songUrl=$(readXmlAttr "$songXml" "songUrl") 
        lyricsUrl=$(readXmlAttr "$songXml" "lyricsUrl") 
        songInfoUrl="http://www.google.cn/music/song?id=$songId&output=xml"

        songInfoXml=$(curl -s "$songInfoUrl")
        songName=$(readXmlAttr "$songInfoXml" "name")
        artistName=$(readXmlAttr "$songInfoXml" "artist")
        mp3name="$songName($artistName)"

        downMusic "$songUrl" "$mp3name" "$lyricsUrl" "$keyword"

done < $songsFile

