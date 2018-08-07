#!/bin/sh
# sunfuhao
# 20180314

export LD_LIBRARY_PATH=ffmpeg/ffmpeg_i_2/lib/
HADOOP=hh/hadoop_1.4.8/hadoop/bin/hadoop
#one="yuan01.jpg"
#two="yuan02.jpg"
#three="yuan03.jpg"
one=$1
two=$2
three=$3
rm -rf mohu
rm -rf openimg
mkdir mohu
mkdir openimg
echo $one
#rm mohu*
#rm size*
rm *.mpg
rm *.mp4
#rm ./openimg/*
echo "run python begin"
i_python="~tools/python27-gcc482/bin/python"
#i_python="py/python27-gcc482/bin/python"
$i_python video_mohu.py ./$one ./mohu
$i_python video_mohu.py ./$two ./mohu
$i_python video_mohu.py ./$three ./mohu
#~/tools/python27-gcc482/bin/python video_mohu.py $one ./mohu
#~/tools/python27-gcc482/bin/python video_mohu.py $two ./mohu
#~/tools/python27-gcc482/bin/python video_mohu.py $three ./mohu

$i_python video_py.py ./$one ./openimg
$i_python video_py.py ./$two ./openimg
$i_python video_py.py ./$three ./openimg
##~/tools/python27-gcc482/bin/python video_py.py $one ./openimg
##~/tools/python27-gcc482/bin/python video_py.py $two ./openimg
##~/tools/python27-gcc482/bin/python video_py.py $three ./openimg
#
echo "run python end"
#ffmpeg=ffmpeg/ffmpeg_tool/ffmpeg
ffmpeg=~/tools/all_ffmpeg/ffmpeg_tool/ffmpeg
$ffmpeg -i ./mohu/$one -vf "drawtext=fontfile=arial.ttf: text=West Germanic language:x=293:y=200:fontsize=60:fontcolor=white@1:shadowy=1" ./mohu/tit_$one 
#run base video
$ffmpeg \
 -i ./mohu/tit_$one \
 -i ./mohu/$one \
 -i ./mohu/$two \
 -i ./mohu/$three \
 -filter_complex \
 "[0:v]scale=-2:10*ih,zoompan=z='if(gte(zoom,1.05),zoom+0.13,zoom+0.001)':d=65:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom)',scale=-2:720,fade=t=out:st=2.8:d=1[v0]; \
 [1:v]zoompan=z='if(gte(zoom,2),zoom+0.012,zoom)':d=65,fade=t=in:st=0:d=1,fade=t=out:st=2.2:d=1[v1]; \
 [2:v]zoompan=z='if(gte(zoom,2),zoom+0.012,zoom)':d=100,fade=t=in:st=0:d=0.8,fade=t=out:st=3.1:d=0.5[v2]; \
 [3:v]zoompan=z='if(gte(zoom,2),zoom+0.012,zoom)':d=170,fade=t=in:st=0:d=0.3[v3]; \
 [v0][v1][v2][v3]concat=n=4:v=1:a=0,format=yuv420p[v]" -map "[v]" -s "1280x720" -vb 2M -r 100 -t 15 ./godemo.mp4

$ffmpeg -i ./godemo.mp4 \
 -i ./openimg/$one \
 -i ./openimg/$two \
 -i ./openimg/$three \
 -filter_complex \
"[0:v]overlay=x='if(gte(t\,2.5),\
		if(gte(t,4.2),\
			if(gte(t,6),(-w), (-100*(t-4.2)-400*(t-4.2)*(t-4.2)+270))\
		,270) \
 	,(-w)
 )'\
 :y=115[tl];[tl] \
 [2:v]overlay=x='if(lte(t\,4.2),(w+1080), \
 	if(gte(t,6),\
 	    if(gte(t,8.2),((-100*(t-8.2)-400*(t-8.2)*(t-8.2)+270)),270) \
 	,(w+1080-113.3*(t-4.2)-400*(t-4.2)*(t-4.2))) \
 )'\
 :y=115[tc];[tc] \
 [3:v]overlay=x='if(lte(t\,4.2),(-w), \
 	if(gte(t,6),\ 
 	    if(gte(t,8.2),\ 
 	    	if(gte(t,10),270,(w+1080-113.3*(t-8.2)-400*(t-8.2)*(t-8.2))) 
 	    \,-w) \
 	,(-w)) \
 )':y=115[out]" \
-map "[out]" godemo_2.mp4 
$ffmpeg -i godemo_2.mp4 -itsoffset 00:00:00.4 -i moyin.mp3 -c:v libx264 -shortest $4 


#~/tools/ffmpeg_i_2/bin/ffmpeg -r 0.5 -i size_mohu_$one stepone_tit.mp4 
$HADOOP fs -put $4 hdfs:///app/ecom/cm/cm_pfs/sunfuhao/
#~/tools/ffmpeg_i_2/bin/ffmpeg -i stepone_tit.mp4 -vcodec mpeg4 testtit.mpg 
