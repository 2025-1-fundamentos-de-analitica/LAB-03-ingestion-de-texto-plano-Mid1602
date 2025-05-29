"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """

    # Path to the file. In the context of the autograder,
    # it's likely 'clusters_report.txt' in the current or a specific input directory.
    # For local execution, ensure this file exists or adjust path.
    file_path = 'files/input/clusters_report.txt'

    # Expected column names after transformation
    final_column_names = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]

    # List to hold dictionaries, each representing a row
    parsed_data_rows = []
    
    current_cluster_info = None
    accumulated_keywords_list = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find the start of the actual data (after the '---' line)
    data_start_index = 0
    for i, line_content in enumerate(lines):
        if line_content.startswith("-------------------------------------------------"):
            data_start_index = i + 1
            break
    
    # Process lines from data_start_index
    for line_number in range(data_start_index, len(lines)):
        # .strip() removes leading/trailing whitespace including newline characters
        line = lines[line_number].strip() 

        if not line:  # Skip any blank lines that might exist between entries
            continue

        # Regex to identify the start of a new cluster record
        # Groups: (1)cluster_no (2)cantidad (3)porcentaje (4)first_keyword_part
        # Example of a line starting a record:
        # "   1     105             15,9 %          maximum power point tracking, ..."
        # The regex accounts for variable spacing.
        match = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)", line)

        if match:
            # If a new cluster is found, and there's pending data for a previous cluster,
            # finalize and store the previous cluster's data.
            if current_cluster_info:
                # 1. Join all accumulated keyword lines for the previous cluster into a single string.
                full_keywords_string = " ".join(accumulated_keywords_list)
                # 2. Consolidate multiple spaces (which can arise from joining lines
                #    or from original formatting) into single spaces.
                full_keywords_string = re.sub(r"\s+", " ", full_keywords_string).strip()
                # 3. Normalize spacing around commas: e.g., "word ,word" or "word,  word" -> "word, word".
                full_keywords_string = re.sub(r"\s*,\s*", ", ", full_keywords_string)
                # 4. Remove a trailing period if it exists (as seen in example outputs), then strip again.
                if full_keywords_string.endswith('.'):
                    full_keywords_string = full_keywords_string[:-1]
                current_cluster_info["principales_palabras_clave"] = full_keywords_string.strip()
                parsed_data_rows.append(current_cluster_info)
            
            # Extract data for the new cluster record
            cluster_id = int(match.group(1))
            cantidad_palabras = int(match.group(2))
            # Convert percentage string like "15,9" to float 15.9
            porcentaje_palabras_str = match.group(3).replace(",", ".")
            porcentaje_palabras = float(porcentaje_palabras_str)
            first_keyword_segment = match.group(4).strip() # First part of keywords from this line

            current_cluster_info = {
                "cluster": cluster_id,
                "cantidad_de_palabras_clave": cantidad_palabras,
                "porcentaje_de_palabras_clave": porcentaje_palabras,
            }
            # Reset keyword accumulator with the first segment from the current line
            accumulated_keywords_list = [first_keyword_segment]
        
        elif current_cluster_info: 
            # This line is a continuation of keywords for the current_cluster_info
            # (It didn't match the new cluster pattern, and we are in the middle of processing a cluster).
            # The line is already stripped of leading/trailing whitespace.
            accumulated_keywords_list.append(line)

    # After the loop, process the very last cluster's data (if any)
    if current_cluster_info:
        full_keywords_string = " ".join(accumulated_keywords_list)
        full_keywords_string = re.sub(r"\s+", " ", full_keywords_string).strip()
        full_keywords_string = re.sub(r"\s*,\s*", ", ", full_keywords_string)
        if full_keywords_string.endswith('.'):
            full_keywords_string = full_keywords_string[:-1]
        current_cluster_info["principales_palabras_clave"] = full_keywords_string.strip()
        parsed_data_rows.append(current_cluster_info)

    # Create DataFrame from the list of dictionaries, ensuring specified column order
    df = pd.DataFrame(parsed_data_rows, columns=final_column_names)
    
    return df