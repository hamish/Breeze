
TIMESTAMP=`date -u +"%Y-%m-%dT%H:%M:%SZ"`
BUCKET="my-breeze-bucket"
DIRECTORY="output"

echo "$TIMESTAMP" "$BUCKET" "$DIRECTORY"
./runGenerator "$TIMESTAMP" "$BUCKET" "$DIRECTORY"
