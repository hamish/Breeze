
TIMESTAMP=`date -u +"%Y%m%d-%H%M%S"`
BUCKET="my-breeze-bucket"
DIRECTORY="output"

echo "$TIMESTAMP" "$BUCKET" "$DIRECTORY"
./runGenerator "$TIMESTAMP" "$BUCKET" "$DIRECTORY"
