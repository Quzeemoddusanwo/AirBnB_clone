W3C validator for Holberton School
For HTML and CSS files.

Based on 2 APIs:

https://validator.w3.org/nu/
http://jigsaw.w3.org/css-validator/validator
Installation
Clone this repo
git clone https://github.com/holbertonschool/W3C-Validator.git
Run shell script (see example in usage section below)
Usage:
Simple file:

./w3c_validator.py index.html
Multiple files:

./w3c_validator.py index.html header.html styles/common.css
All errors are printed in STDERR; Exit status = # of errors (0 on success)

References
https://developer.mozilla.org/en-US/
