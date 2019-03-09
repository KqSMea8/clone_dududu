#!/bin/sh

if [ $# -ge 2 ]; then
    DD="$1"
    win=$2
else
    DD="$1"
    win=1
fi

rm final_user_trade.txt
wget nmg01-ido-sche10.nmg01.baidu.com:/home/work/user_trade_final-Feedas_user_trade-user_env/final_user_trade.txt
cp final_user_trade.txt script/feedas_user_trade 
HADOOP_HOME="/home/sunfuhao/tools/hadoop_afs/output/hadoop-client/hadoop"
SHITU_PATH="/log/11523/fc_mingtou_clk_charge_log/$DD/*/nmg01-khan-hdfs.dmop/tc-toad-log00.tc.baidu.com/*.log"
SHITU_OUT="/app/ecom/cm/cm_pfs/sunfuhao_pfs/feed_shitu/"$DD"_"$win
DD_STR=""
for((i=0;i<$win;i++))
do
    CUR_DAY=`date +"%Y%m%d" -d"$DD $i days ago"`
    cur_src="${SHITU_PATH}"
    if [ $i -eq 0 ]; then
        DD_STR="${cur_src}"
    else
       cur_path="/log/11523/fc_mingtou_clk_charge_log/$CUR_DAY/*/nmg01-khan-hdfs.dmop/tc-toad-log00.tc.baidu.com/*.log" 
        DD_STR="${DD_STR},${cur_path}"
    fi
done
echo $DD_STR


$HADOOP_HOME/bin/hadoop fs -rmr ${SHITU_OUT}

$HADOOP_HOME/bin/hadoop streaming \
	-D mapred.map.tasks=1000 \
	-D mapred.job.map.capacity=3000 \
	-D mapred.reduce.tasks=100 \
	-D mapred.job.reduce.capacity=3000 \
	-D abaci.split.remote=true \
	-D mapred.job.priority=VERY_HIGH \
	-D mapred.job.name="sunfuhao_shitu_${DD}" \
	-input ${DD_STR} \
	-output ${SHITU_OUT} \
	-mapper "sh mapper_3.sh" \
	-reducer "sh reduce_3.sh" \
	-file "./script/mapper_3.sh" \
	-file "./script/reduce_3.sh" \
	-file "./script/dkf" \
	-file "./script/feedas_user_trade" \
	-file "./script/hangye_2" 
if [ $? -ne 0 ]
then
   echo "$0 fail $DD"
   exit 1
fi

rm ./data/feed_shitu.$DD"_"$win
$HADOOP_HOME/bin/hadoop fs -getmerge ${SHITU_OUT} ./data/feed_shitu.$DD"_"$win



#
#
#
