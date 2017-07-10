#disk_test.sh
# run it inside the src folder
# dd tests
touch dd_stats.txt
touch fio_stats.txt
echo "=========== Test time: $(date) ==============" >> dd_stats.txt
echo $'\n\tWrite' >> dd_stats.txt
(dd if=/dev/zero bs=512k of=tstfile count=1024) 2>> dd_stats.txt
echo $'\n\tRead' >> dd_stats.txt
(dd if=tstfile bs=512k of=/dev/null count=1024) 2>> dd_stats.txt
echo $'\n' >> dd_stats.txt
rm -f tstfile
# fio tests
echo "=========== Test time: $(date) ==============" >> fio_stats.txt
(fio trivial.fio) >> fio_stats.txt
echo $'\n' >> fio_stats.txt