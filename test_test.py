from collections import namedtuple
from operator import attrgetter


def get_full_number(number):
    """Function to convert short handed numbers to full number."""
    if number.endswith("K"):
        return float(number[:-1]) * 1000
    elif number.endswith("M"):
        return float(number[:-1]) * 1000000
    else:
        return float(number)


def sort_function(data, sort_field):
    """Function to sort the input Data on the basis of sort_field"""
    if sort_field not in table_fields:
        return data

    complexity_values = {"low": 0, "medium": 1, "high": 2}
    get_key = attrgetter(sort_field)

    sort_key = {
        "complexity": lambda x: complexity_values.get(get_key(x).lower(), 100),
        "impact_score": lambda x: float(get_key(x)),
        "num_cases": lambda x: get_full_number(get_key(x).upper()),
        "default": lambda x: get_key(x).lower(),
    }

    sort_key["name"] = sort_key["default"]

    return sorted(data, key=sort_key[sort_field])


def filter_function(data, filter_text):
    """Function to filter the results on the basis of filter_text from the input Data."""
    filter_text = filter_text.lower()
    return list(
        filter(
            lambda x: filter_text in x.name.lower()
            or filter_text in x.complexity.lower(),
            data,
        )
    )


table_fields = ["name", "num_cases", "impact_score", "complexity"]

row = namedtuple("stats", table_fields)

# Original Input Data

input_data1 = list()

input_data1.append(row("Password attack", "32.85M", "5", "low"))
input_data1.append(row("Phishing", "25.12M", "7.18", "low"))
input_data1.append(row("Session hijack", "9024", "5.79", "high"))
input_data1.append(row("SQL Injection", "1.25M", "10.21", "medium"))
input_data1.append(row("XSS", "29850", "2.19", "low"))
input_data1.append(row("Man in the Middle", "95k", "8.12", "high"))


# Test 1 - Sorting on the basis of "name" field

sort_field = "name"
filter_text = ""

expected_output = [
    "Man in the Middle",
    "Password attack",
    "Phishing",
    "Session hijack",
    "SQL Injection",
    "XSS",
]

result = sort_function(filter_function(input_data1, filter_text), sort_field)

result = [row.name for row in result]

assert result == expected_output


# Test 2 - Sorting on the basis of "complexity" field

sort_field = "complexity"
filter_text = ""

expected_output = ["low", "low", "low", "medium", "high", "high"]

result = sort_function(filter_function(input_data1, filter_text), sort_field)

result = [row.complexity for row in result]

assert result == expected_output


# Test 3 - Sorting on the basis of "impact_score" field

sort_field = "impact_score"
filter_text = ""

expected_output = ["2.19", "5", "5.79", "7.18", "8.12", "10.21"]

result = sort_function(filter_function(input_data1, filter_text), sort_field)

result = [row.impact_score for row in result]

assert result == expected_output


# Test 4 - Sorting on the basis of "num_cases" field
sort_field = "num_cases"
filter_text = ""

expected_output = ["9024", "29850", "95k", "1.25M", "25.12M", "32.85M"]

result = sort_function(filter_function(input_data1, filter_text), sort_field)
result = [row.num_cases for row in result]

assert result == expected_output


# Test 5 - Filter the Input test:
sort_field = ""
filter_text = "med"

expected_output = ["medium"]

result = sort_function(filter_function(input_data1, filter_text), sort_field)
result = [row.complexity for row in result]

assert result == expected_output


# Test 6 - Another Filter the Input test:
sort_field = ""
filter_text = "l"

expected_output = [
    ("Password attack", "low"),
    ("Phishing", "low"),
    ("SQL Injection", "medium"),
    ("XSS", "low"),
    ("Man in the Middle", "high"),
]

result = sort_function(filter_function(input_data1, filter_text), sort_field)
result = [(row.name, row.complexity) for row in result]

assert result == expected_output


# Test 7 - Filter the input and sort the results on the basis of "name" field:
sort_field = "name"
filter_text = "l"

expected_output = [
    ("Man in the Middle", "high"),
    ("Password attack", "low"),
    ("Phishing", "low"),
    ("SQL Injection", "medium"),
    ("XSS", "low"),
]

result = sort_function(filter_function(input_data1, filter_text), sort_field)
result = [(row.name, row.complexity) for row in result]

assert result == expected_output


# Test 8 - Filter the input which produces 0 row output:
sort_field = ""
filter_text = "anything random which doesn't match"

expected_output = list()

result = sort_function(filter_function(input_data1, filter_text), sort_field)

assert result == expected_output


# Test 9 - Any other input other then Original input given in problem:
input_data2 = list()

input_data2.append(row("Random Data - 1", "100.99M", "50", "medium"))
input_data2.append(row("fake Data - 2", "999", "70.18", "medium"))
input_data2.append(row("FAKE data - 3", "999K", "3.79", "low"))
input_data2.append(row("Quick Brown Fox", "999M", "99.21", "medium"))
input_data2.append(row("Jumping over the dog", "69", "21.19", "low"))
input_data2.append(row("Last but not the least", "9k", "1000.8", "high"))

sort_field = "name"
filter_text = "data"

expected_output = [
    ("fake Data - 2", "medium"),
    ("FAKE data - 3", "low"),
    ("Random Data - 1", "medium"),
]

result = sort_function(filter_function(input_data2, filter_text), sort_field)
result = [(row.name, row.complexity) for row in result]

assert result == expected_output
