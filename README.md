# karma
API pwndb

Karma is a tool written in [python3](https://www.python.org) for the search of emails and passwords on the site: `pwndb2am4tzkvold (dot) onion`

---

## Getting Started
### Prerequisites
To run this program it's necessary to have installed:

+ tor
+ python3
+ pyhton-pip3

To install the necessary packages (Debian/Ubuntu), run:
```
sudo apt install tor python3 python3-pip
```

+ python libraries:
    - requests
    - docopt


To install the necessary libraries, run:
```
pip3 install -r requirements.txt
```

### Installing
Once the prerequisites are installed, it is only necessary to clone this repository.

```
git clone https://github.com/decoxviii/karma.git ; cd karma
python3 bin/karma.py --help
```

---

## Running the tests
All the tests were done in `Debian/Ubuntu`.

1. Search emails with the password: `123456789`
```
python3 bin/karma.py search '123456789' --password -o test1
```

2. Search emails with the local-part: `johndoe`
```
python3 bin/karma.py search 'johndoe' --local-part -o test2
```

3. Search emails with the domain: `hotmail.com`
```
python3 bin/karma.py search 'hotmail.com' --domain -o test3
```

4. Search email password: `johndoe@unknown.com`
```
python3 bin/karma.py target 'johndoe@unknown.com' -o test4
```

If you have found an error or have any suggestions, do not hesitate to contribute to this project.

---

## Disclaimer

Usage this program for attacking targets without prior consent is illegal. It's the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program. Only use for educational purposes.

## License

This project is licensed under the [MIT](https://github.com/decoxviii/karma/blob/master/LICENSE) License

## Thanks

This program is inspired by the projects:

+ [M3l0nPan](https://github.com/M3l0nPan) - [pwndb-api](https://github.com/M3l0nPan/pwndb_api)
+ [davidtavarez](https://github.com/davidtavarez) - [pwndb](https://github.com/davidtavarez/pwndb)

## Author:

+ decoxviii

