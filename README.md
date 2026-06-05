# Python ISO Commercial Auto Rating Engine

![Python](https://img.shields.io/badge/Python-3.x-blue)
![AWS S3](https://img.shields.io/badge/AWS-S3-orange)

## Overview

A dynamic commercial auto rating and pricing engine written in Python
and integrated with AWS S3. Solves the complex problem of pricing
insurance quotes across multiple vehicles, drivers, and states using
ISO's standardized rating framework.This tool could be used by actuarial
analysts to validate current rates and model changes to rates. It is a
faster and more nimble tool for creating, testing, analyzing, and changing
insurance rates than relying on expensive and rigid policy administrative
systems. Yet, it could be integrated into policy administration systems like
Majesco or other pricing analytic systems like Hyperexponential.

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

## Design Philosophy: Universal Data Model Approach

The starting point for the rater was harmonizing and flattening the data files provided
by Verisk in their Excel-based rater. There are about 5 states that are notoriously
complicated from a rating perspective. I asked myself a basic question: what if there
were a 52nd (50 states plus Washington DC) state that had all of the most complicated
elements of the other states? If we can solve for the hardest problem, then all the states
will align. From this, I was able to create a universal data design such that the
state-by-state files look identical (but contain different rates/factors) and the structure
supports both business auto and public auto. One key benefit of this approach, and why I
think this rater is better than many, is that much of the logic is pushed to the data layer.
In other words, there is no logic that says "if this state then do X, but if it is that state
then do Y." A system like that would never get off the ground. It would be a nightmare to test.

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

## Sample Output

Look at rating/sample_output/output_data.json. This has both the
quote/quote_version/vehicles/drivers detail as the quote input.
It also has the rating output included in the json file.

## Technical Architecture

- Language: Python
- Key modules:
  - data definition models: quote, quote_version, vehicle, driver, rate_part
  - configurable quote for multiple quote versions, one to many vehicles and drivers.
  - rating engine: vehicle_context, rating_engine, dataset_loader
  - rate_parts:loss cost, age group, primary & secondary classes, fleet size,
    increased limits, naics, original cost new, liability and pd deductibles, policy tier,
    raca adjustment, loss cost multipliers, truckload dumping
  - premium_calculator: premium calculated at the vehicle level to support a UI grid
    of coverage types as columns and rates and factors as rows
  - dataset_loader: prefetches all rate file datasets from S3 before the logic to filter
    for a given rate is executed
- Amazon S3 bucket to store the rates files for OH, VA, and MD. It also stores other
  files/data to define default data elements as well as support or emulate an online
  quoting experience.

## Insurance Domain Context And Related Production Experience

This is a very close replica of a commercial auto rater I built
for Forge Insurance to support a mid-term conversion. The original
version was written in NextJS and JavaScript. It had API calls to
LexisNexis for Commercial Data Prefill, Attract Scoring, and CLUE.
There was also API calls to Verisk for Symbol rating and another
API to VIN Audit to fetch vehicle values. There are attributes in the
quote version, driver, and vehicle models that could collect the data
elements from these API calls. In this Python model, I am not making
those API calls. Rather, I am just showing where those services
would come into play.

## Finally...

The original rater was JavaScript-based, web-enabled, had capabilities to
ingest .csv rate files and convert them to .json. It also supported a
best-in-class commercial auto quote. I was motivated to recreate this in
Python to improve my Python skills. I learned a lot about JavaScript when
I wrote it the first time and I learned a lot by doing this in Python. The
two implementations gave me a much deeper appreciation for how rating logic
translates across languages and platforms.

## Author

Joe Niemer | linkedin.com/in/joe-niemer
