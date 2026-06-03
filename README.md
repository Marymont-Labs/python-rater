# Python ISO Commercial Auto Rating Engine DRAFT OUTLINE

## Overview

This is a dynamic commercial auto rating and pricing engine code in
python and integrated with AWS S3 buckets. It solves the complicated
problem of pricing an insurance quote for multiple vehicles, drivers,
and states. This tool would be used by actuarial analysts to validate
current rates and model changes to rates. It could be integrated
into policy administration systems like Majesco other pricing analytic
systems like Hyperexponential.

## Background: What is ISO Commercial Auto Rating?

ISO Commercial auto rating is the standardized framework used by the
commercial auto insurance industry to evaluate the price of the risks
associated with business-owned vehicle. It is developed by the
Insurance Services Office (ISO). ISO is a division of Verisk.

The value of ISO is to eliminate the need by every insurance carrier
to invent their own pricing models from scratch. Most carriers use ISO's
actuarial data, standard class code, territory codes and rating rules as a
baseline. Carriers then adjust the rates with their own company-specific
multipliers.

## What This Engine Does

- Accepts vehicle and risk input attributes
- Applies 14 ISO rates and factors. These include base rates,
  territory factors, class modifiers, deductible limits,
  vehicle value and factors, and others. The rating/rate_parts
  folder details all factors used.
- Produces a tiered good/better/best quote structure. Agents and
  direct-to-consumer users want choices and an avenue to customize
  quotes.
- Outputs a complete pricing payload per vehicle
  per coverage tier — matching production REST API
  payload structure

## Sample Input

Look at rating/input/sample_quote. This is nested quote object.
A quote is composed of 3 quote versions (good, better, and best).
Each quote version has one to many vehicles and drivers.

## Sample Input

Look at rating/sample_output/data.json. This has both the
quote/quote_version/vehicles/drivers detail as the quote input.
It also has the rating output included in the json file.

## Technical Architecture

- Language: Python
- Key modules:
  - data definition models: quote, quote_version, vehicle, driver, rate_part
  - rating engine: vehicle_context, rating_engine, dataset_loader
  - rate_parts:
  - premium_calculator:

- Amazon S3 bucket to store the rates files for OH, VA, and MD.
  It also stores other files/data to define default data elements
  as well as support or emulate an online quoting experience.
- How the rating logic is organized (factors,
  modifiers, validation)

## Insurance Domain Context TODO

Brief note on how this maps to a real production
environment — how this payload would feed a policy
admin system, connect to third-party data sources
like Verisk or LexisNexis, integrate with a
Majesco-style API layer.
This is what separates your repo from a generic
Python exercise.

## Related Production Experience TODO

2-3 sentences referencing Forge Insurance — that
this engine is a Python reconstruction of a
production rating and quoting system you designed
and built. Link to your LinkedIn.

## Author

Joe Niemer | linkedin.com/in/joe-niemer
