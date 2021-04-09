if [ -z "$1" ];
then
	echo "Usage: $0 <target_host> <locust_file> [number_of_slaves]"
	exit 1
fi

locust_kill() {
	echo "Killing all current locust processes..."
	killall -9 locust
	exit 0
}

trap locust_kill SIGINT

killall -9 locust 2>/dev/null

if [ -z "$3" ];
then
	echo "Running in sinle-worker mode"
	locust -f $2 --host $1
else
	locust --master -f $2 --host $1 &
	for i in $(seq 1 $3);
	do
		locust --worker -f $2 &
	done

	while true;
	do
		sleep 1
	done
fi
