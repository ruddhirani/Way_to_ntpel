# Friendly-Fortnight
# TASK 1(A)
The Python script provided  that can be used to download MP3 lecture files from a given URL. It utilizes the yt_dlp library to download videos from YouTube, extracts the audio from the downloaded videos, and saves them as MP3 files. The script uses Selenium WebDriver to navigate to the course website, find the video links for each week and lesson, and then downloads the videos.

<br />
To run the script, you need to provide the following command-line arguments:

--course_url: The URL of the course website.<br />
--driver_directory: The path to the driver directory (for Selenium WebDriver).<br />
--output_path: The path to the output folder where the MP3 files will be saved.<br /><br />
Once the arguments are provided, the script initializes the driver, navigates to the course website, retrieves the video links, downloads the videos as MP3 files, and finally closes the driver.

Please note that you need to have the necessary dependencies installed (yt_dlp, tqdm, and selenium) for the script to run successfully.

### Usage
To use the script, open a command prompt and navigate to the directory where the script is saved. Then run the following command:

```python 
python ntpel_download_lecture.py --course_url <url> --driver_directory <path> --output_path <path>
```
for example
```python 
python ntpel_download_lecture.py --course_url https://nptel.ac.in/courses/106106184 --driver_directory chromedriver --output_path input_audio
```

# TASK 1(B)

The code provided is a Python script that can be used to download PDF transcript files from a given URL. It utilizes Selenium WebDriver to navigate to the course website, click on the "Downloads" button, and then click on the "View Transcripts" button. It then retrieves the chapter names and PDF download links for each chapter, and downloads the PDF transcripts to a specified output folder.

To run the script, you need to provide the following command-line arguments:
<br />
--course_url: The URL of the course website.<br />
--driver_directory: The path to the driver directory (for Selenium WebDriver).<br />
--output_path: The path to the output folder where the PDF files will be saved.<br />
<br />
Once the arguments are provided, the script initializes the driver, navigates to the course website, clicks on the necessary buttons, retrieves the chapter names and PDF download links, and downloads the PDF transcripts for each chapter.

Please note that you need to have the necessary dependencies installed (selenium, tqdm, and requests) for the script to run successfully.

### Usage
```python 
python ntpel_download_transcript.py --course_url <url> --driver_directory <path> --output_path <path>
```
for example
```python 
python ntpel_download_transcript.py --course_url https://nptel.ac.in/courses/106106184 --driver_directory chromedriver --output_path output_pdf
```
# TASK 2
The provided code is a shell script that takes inputs from the user and converts MP3 audio files to WAV format with a 16KHz sampling rate and mono channel using the ffmpeg command. It also limits the number of parallel processes to a specified value (N) to control resource usage.
<br /><br />
The script expects three command-line arguments:
<br />
<br />
INP: The input directory path where the MP3 files are located.<br />
OUT: The output directory path where the converted WAV files will be saved.<br />
N: The maximum number of parallel processes to run at a time.<br /><br />
If the output directory doesn't exist, it creates the directory. Then, it loops through all the files in the input directory with the .mp3 extension. For each file, it checks if the file exists, and if so, it uses ffmpeg to convert the audio to WAV format with the specified sampling rate and channel settings. It runs the conversion process in the background and limits the number of parallel processes to the specified value (N).

After processing all the files, it waits for all the background jobs to complete using the wait command.

Please note that you need to have ffmpeg installed on your system for the script to work properly.


### Usage
```python 
sudo bash audio_processor.sh input-directory output-directory no-parrell-process
```
for example
```python 
sudo bash audio_processor.sh input_audio output_audio 5
```

# TASK 3
The provided code is a Python script that extracts text from PDF files and saves them as preprocessed text files. It uses the PyPDF2 library to read and extract text from PDF files.

The script expects two command-line arguments:

pdf_file_path: The path to the directory containing the PDF files.<br />
output_file_path: The path to the directory where the output text files will be saved.<br />
The script defines several functions:<br />

convert_pdf_to_text(pdf_path): Converts a PDF file to text using PyPDF2 and returns the extracted text.<br />
preprocess_text(text): Preprocesses the text by converting it to lowercase, removing punctuation, and converting digits to spoken form using regular expressions and the num2words library.<br />
extract_transcripts(pdf_paths, pdf_file_path, output_file_path): Extracts transcripts from PDF files by calling convert_pdf_to_text() and preprocess_text() for each PDF file, and saves the preprocessed text as separate text files.<br />
main(): The main function that parses the command line arguments, retrieves the list of PDF files in the specified directory, and calls extract_transcripts() to extract and save the transcripts.<br />
The code also includes a docstring that provides a brief description of the purpose of the script and the arguments it takes.

Please note that the code relies on the PyPDF2 and num2words libraries, so make sure to install them before running the script.


### Usage
```python 
python pdfExplorer.py  --pdf_file_path <input directory> --output_file_path <output directory>
```
for example
```python 
python pdfExplorer.py  --pdf_file_path output_pdf --output_file_path output
```


# TASK 4

The provided code is a Python script that splits audio files and generates a training manifest for speech recognition tasks. It takes as input the paths to directories containing audio files and PDF files, and outputs the split audio files along with corresponding durations and preprocessed text in a training manifest file.
<br /><br /><br />The script defines several functions:
get_split(pdf_file_path): Extracts timestamped text from a PDF file using the extract_text() function from the pdfminer library. It returns a list of tuples containing timestamps and corresponding text.<br />
<br />chunk_audio(audio_file_path, timestamp_list, output_path): Splits the audio file into chunks based on the provided timestamps. It uses the pydub library to load the audio file, splits it into chunks based on the timestamps, and exports each chunk as a separate audio file. It returns a tuple containing a list of file paths for the audio chunks and a list of corresponding durations.<br />
<br />preprocess_text(text): Preprocesses the text by converting it to lowercase, removing punctuation, and converting digits to spoken form using the num2words library. It returns the preprocessed text.<br />
<br />main(): The main function that parses the command line arguments, retrieves the list of audio files and PDF files in the specified directories, processes the PDF files, splits the audio files, preprocesses the text, and generates a training manifest file.<br />
<br />The script uses the argparse library to handle command line arguments. The required command line arguments are:
<br />
<br />audio_file_path: The path to the directory containing audio files.<br />
<br />pdf_file_path: The path to the directory containing PDF files.<br />
<br />output_file_path: The path to the directory where the split audio chunks will be saved.<br />
<br />manifest_path: The path to the output training manifest file.<br />
<br />The code also includes a docstring that provides a brief description of the purpose of the script and the arguments it takes.
<br />


Please note that the code relies on several external libraries such as PyPDF2, num2words, pydub, pdfminer, and json. Make sure to install these libraries before running the script.


### Usage
for example
```python 
python speed_train.py --audio_file_path output_audio --pdf_file_path output_pdf --output_file_path output12 --manifest_path train_manifest.jsonl
```


# TASK 5
First clone the NeMO repository with the following command
```python
git clone  https://github.com/NVIDIA/NeMo.git
```
```python
pip install -r tools/speech_data_explorer/requirements.txt
```

### Usage
for example
```python 
python Nemo/tools/speech_data_explorer/data_explorer.py train_manifest.jsonl
```

# OBSERVATION

1.Task 1(A) involves a Python script that downloads MP3 lecture files from a given URL using the yt_dlp library and Selenium WebDriver. It requires command-line arguments for the course URL, driver directory, and output path.
<br /><br />
2.Task 1(B) is a Python script that downloads PDF transcript files from a provided URL using Selenium WebDriver. It retrieves chapter names and PDF download links, saving the transcripts to a specified output folder. Command-line arguments are required for the course URL, driver directory, and output path.
<br /><br />
3.Task 2 is a shell script that converts MP3 audio files to WAV format using ffmpeg. It limits the number of parallel processes to control resource usage. The script expects command-line arguments for the input directory, output directory, and maximum number of parallel processes.
<br /><br />
4.Task 3 is a Python script that extracts text from PDF files using PyPDF2. It preprocesses the text and saves it as preprocessed text files. Command-line arguments include the PDF file path and output file path.
<br /><br />
5.Task 4 is a Python script that splits audio files and generates a training manifest for speech recognition tasks. It utilizes PDF files to extract timestamped text and splits audio based on the timestamps. The script requires command-line arguments for the audio file path, PDF file path, output file path, and manifest path.
<br /><br />
6.Task 5 involves using the NeMo repository to explore speech data. The repository needs to be cloned and the required dependencies installed using the provided command.
<br /><br />
7.Task 1(A) requires dependencies such as yt_dlp, tqdm, and Selenium, while Task 1(B) requires selenium, tqdm, and requests. Task 2 requires ffmpeg to be installed. Task 3 relies on PyPDF2 and num2words libraries, and Task 4 requires several external libraries such as PyPDF2, num2words, pydub, pdfminer, and json. It is necessary to install these libraries for the respective tasks to run successfully.
<br /><br />
8.The provided usage examples demonstrate how to execute the scripts with the required command-line arguments.
<br /><br />
9.The tasks involving Selenium WebDriver require specifying the driver directory, which should correspond to the appropriate driver for the chosen browser (e.g., chromedriver for Chrome).
<br /><br />
10.It is important to note the dependencies, command-line arguments, and execution instructions for each task to ensure smooth and successful execution.
<br /><br />
11.In some PDF files, timestamps are not extracted accurately, resulting in inefficient generation of audio and text chunks.
<br /><br />
12.Unwanted Unicode characters may be generated during text extraction from PDF files. Trying alternative text extraction modules could help avoid this issue.
