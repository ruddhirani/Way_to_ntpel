set -e  # Exit immediately if any command fails
set -u  # Treat unset variables as errors
# Take inputs from user
INP=$1
OUT=$2
N=$3

# Create output directory if it doesn't exist
if [ ! -d $OUT ]
then
    mkdir $OUT
fi
echo $INP/*.mp3

# Loop through all files in input directory
for file in "$INP"/*.mp3; do
    # Check if the file exists
    if [ -f "$file" ]; then
        # Use ffmpeg to convert audio to WAV format with 16KHz sampling rate and mono channel
        ffmpeg -i "$file" -ac 1 -ar 16000 "$OUT/$(basename "$file" .mp3).wav" &

        # Limit the number of parallel processes to N
        while [ "$(jobs | wc -l)" -ge "$N" ]; do
            sleep 1
        done
    else
        echo "File not found: $file" >&2
    fi
done

# Wait for all background jobs to complete
wait
