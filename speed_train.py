import argparse
import re
import os
import json
import string
from num2words import num2words
from pydub import AudioSegment
from datetime import datetime
from pdfminer.high_level import extract_text


def get_split(pdf_file_path):
    """
    Extracts timestamped text from a PDF file.

    Args:
        pdf_file_path (str): Path to the PDF file.

    Returns:
        list: A list of tuples containing timestamp and corresponding text.
    """
    # Extract text from the PDF file
    text = extract_text(pdf_file_path)

    # Remove header
    text = text.split("\n\n")
    text = text[2:]  # Join the text without header
    text = ' '.join(text)  # Adding the initial timestamp
    text = "(Refer Slide Time: 00:00) " + text

    # Make list of tuples of text and time stamp
    pattern = r'\(Refer Slide Time: (\d+:\d+)\)\s*(.*?)\s*(?=\(Refer Slide Time:|$)'

    matches = re.findall(pattern, text)

    result = [(match[0], match[1].strip()) for match in matches]

    return result


def chunk_audio(audio_file_path, timestamp_list, output_path):
    """
    Splits the audio file into chunks based on the provided timestamps.

    Args:
        audio_file_path (str): Path to the audio file.
        timestamp_list (list): List of tuples containing timestamps and corresponding text.
        output_path (str): Path to the directory where audio chunks will be saved.

    Returns:
        tuple: A tuple containing a list of file paths for the audio chunks and a list of corresponding durations.
    """
    audio_file = AudioSegment.from_wav(audio_file_path)
    timestamps = [k[0] for k in timestamp_list]

    # Convert timestamps to milliseconds
    timestamps_ms = [datetime.strptime(x, "%M:%S") for x in timestamps]
    timestamps_ms = [int((x.minute * 60 + x.second) * 1000) for x in timestamps_ms]

    # Split the audio file into chunks based on the timestamps
    chunks = []
    for i in range(len(timestamps_ms)-1):
        start = timestamps_ms[i]
        end = timestamps_ms[i+1]
        if i == 0:  # First chunk
            start = start + 10*1000
        chunks.append(audio_file[start:end])
    end = len(audio_file) - 30.5 * 1000
    chunks.append(audio_file[timestamps_ms[-1]:end])

    # Export each chunk as a separate audio file
    file_paths = []
    audio_durations = []
    for i, chunk in enumerate(chunks):
        file_name = output_path + "_{}.wav".format(i)
        chunk.export(file_name, format="wav")
        file_paths.append(file_name)
        audio_durations.append(chunk.duration_seconds)

    return file_paths, audio_durations


def preprocess_text(text):
    """
    Preprocesses the text by converting it to lowercase, removing punctuation, and converting digits to spoken form.

    Args:
        text (str): Input text.

    Returns:
        str: Preprocessed text.
    """
    # Convert all text to lowercase
    text = text.lower()

    # Remove all punctuations
    punctuations = string.punctuation + '\uf0b4\uf0b6"\',-\''+'\uf061\uf071'
    text = text.translate(str.maketrans('', '', punctuations))

    # Convert all digits to their spoken form
    words = []
    for word in text.split():
        if word.isdigit():
            words.append(num2words(word))
        else:
            words.append(word)
    text = ' '.join(words)

    return text


def main():
    """
    Main function to split audio and generate a training manifest.

    Reads the command line arguments, processes PDF files, splits audio files, preprocesses text, and generates a training manifest file.
    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Split audio and generate a training manifest")

    # Add the required arguments
    parser.add_argument('--audio_file_path', required=True, help='Path to the directory containing audio files')
    parser.add_argument('--pdf_file_path', required=True, help='Path to the directory containing PDF files')
    parser.add_argument('--output_file_path', required=True, help='Path to the directory where audio chunks will be saved')
    parser.add_argument('--manifest_path', required=True, help='Path to the output training manifest file')

    # Parse the command line arguments
    args = parser.parse_args()

    audio_file_path = args.audio_file_path
    pdf_file_path = args.pdf_file_path
    output_file_path = args.output_file_path
    manifest_path = args.manifest_path

    file_names = os.listdir(audio_file_path)
    audio_file_list = sorted(file_names)

    file_names = os.listdir(pdf_file_path)
    pdf_file_list = sorted(file_names)

    results = []
    for audio_file, pdf_file in zip(audio_file_list, pdf_file_list):
        try:
            res = get_split(f'{pdf_file_path}/{pdf_file}')
            chunk_path, durations = chunk_audio(f'{audio_file_path}/{audio_file}', res, f'{output_file_path}/{audio_file[:-4]}')
            for tup, path, dur in zip(res, chunk_path, durations):
                results.append({'audio_filepath': path,
                                'duration': dur,
                                'text': tup[1]})

        except Exception as e:
            print(f"Error preprocessing PDF {pdf_file}: {e}")
            continue

    for item in results:
        item['text'] = preprocess_text(item['text'])

    with open(manifest_path, 'w') as f:
        for item in results:
            if len(item["text"]) <= 1:
                continue
            if item["duration"] == 0:
                continue
            audio_filepath = os.path.abspath(item['audio_filepath'])
            json.dump({"audio_filepath": audio_filepath, "duration": item['duration'], "text": item['text']}, f)
            f.write('\n')


if __name__ == "__main__":
    main()


"""Finds 'n' properties within the circle.

Args:
    properties (list): List of property Object
    n (int) : Number of properties to find

Returns:
    PropertyResult: List of property data
"""
