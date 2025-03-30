import os


def concat_txt_files_in_same_folder(output_file):
    try:

        current_folder = os.path.dirname(os.path.abspath(__file__))

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for filename in os.listdir(current_folder):
                if filename.endswith('.txt') and filename != output_file:
                    file_path = os.path.join(current_folder, filename)
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content + '\n')

        print(f"Concatenation completed. Files saved in '{output_file}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


output_file = "concatsongs.txt"
concat_txt_files_in_same_folder(output_file)