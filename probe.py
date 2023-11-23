# To run this program, in powershell, do:
#   type urls.txt | python probe.py
# type prints contents of urls.txt to the terminal. pipe (|) sends
# what is printed to the probe.py program and is accessed with sys.stdin.read().splitlines().
import sys
import requests


def probe(out_file):
    # Alternate to starting the program with:
    #   type urls.txt | python probe.py
    # file = open('urls.txt')
    # for line in file:
    #     print('This is line:')
    #     print(line)

    in_urls = sys.stdin.read().splitlines()
    good_urls = []
    bad_urls = []

    for in_url in in_urls:
        try:
            response = requests.head(
                in_url
            )  # .head is similar to .get except it doesn't ask for the body.
            if response.status_code == 200:
                good_urls.append(in_url)
        except:
            bad_urls.append(in_url)

    with open(out_file, "w") as file:
        file.write("Good urls:\n")
        file.write("\n".join(good_urls))
        file.write("\n\nBad urls:\n")
        file.write("\n".join(bad_urls))


out_file = "filtered_urls.txt"
probe(out_file)
