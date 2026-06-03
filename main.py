# main.py

import json
from dataclasses import asdict
from rating.input.sample_quote import build_quote
from rating.engine.rating_engine import RatingEngine


def main():
    print("******************** BUILDING THE QUOTE **********************")
    quote = build_quote()
    # quote_json = json.dumps(asdict(quote), indent=2)
    # print(quote_json)
    print("******************** PRODUCING GOOD, BETTER, BEST VERSIONS AND RATES **********************")
    engine = RatingEngine()
    result = engine.rate(quote)
    result_json = json.dumps(result, indent=2)

    print(result_json)


if __name__ == "__main__":
    main()