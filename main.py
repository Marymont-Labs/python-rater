# main.py

import json
import os
from dataclasses import asdict
from rating.input.sample_quote import build_quote
from rating.engine.rating_engine import RatingEngine


def main():
    print("******************** BUILDING THE QUOTE **************************************************")
    quote = build_quote()
    # quote_json = json.dumps(asdict(quote), indent=2)
    # print(quote_json)
    print("******************** PRODUCING GOOD, BETTER, BEST VERSIONS AND RATES **********************")
    engine = RatingEngine()
    result = engine.rate(quote)
    result_json = json.dumps(result, indent=2)

    print("******************** WRITING OUT JSON QUOTE AND RATING RESULT *****************************")
    print(result_json)
    output_folder = "./rating/sample_output"
    file_path = os.path.join(output_folder, "data.json")
    os.makedirs(output_folder, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)

    print(f"File successfully saved to {file_path}")    

    
if __name__ == "__main__":
    main()