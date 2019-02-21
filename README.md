# karma
API pwndb - [Demo](https://www.youtube.com/watch?v=tL-kYkmudz4)

Karma is a tool written in [python3](https://www.python.org) for the search of emails and passwords on the site: `pwndb2am4tzkvold (dot) onion`

---

### Install
```
sudo apt install tor python3 python3-pip
git clone https://github.com/decoxviii/karma.git ; cd karma
pip3 install -r requirements.txt
python3 bin/karma.py --help
```

---

### Tests
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

---

### Thanks
This program is inspired by the projects:

+ [M3l0nPan](https://github.com/M3l0nPan) - [pwndb-api](https://github.com/M3l0nPan/pwndb_api)
+ [davidtavarez](https://github.com/davidtavarez) - [pwndb](https://github.com/davidtavarez/pwndb)

### Disclaimer

Usage this program for attacking targets without prior consent is illegal. It's the end user's responsibility to obey allapplicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.

---

#### decoxviii

**[MIT](https://github.com/decoxviii/karma/blob/master/LICENSE)**
