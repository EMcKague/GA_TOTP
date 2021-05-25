# TOTP
TOTP creates 30-Second TOTP codes using the [RFC 6238 standard](https://datatracker.ietf.org/doc/html/rfc6238). These codes syncronize with [GA](https://github.com/google/google-authenticator). It can produce a QR code that is saved a jpg in the directory the file is being ran. This QR code can be scanned and utilized by GA. 

## Installation 

requires python 3.9

## Usuage 

```python
python TOTP.py --get-otp [USERNAME](optional)
python TOTP.py --generate-qr [USERNAME](optional)
```

## Example 

```python
$ python TOTP.py --get-otp
------ 
Genreateing keys at every 30 second and minute mark
Cancel program to stop (Crtl+C)
------
Secret:  AMNL5GR4CF33ATLU6RSGJSGCMJ3JG5PS
OTP code:  763 047
OTP code:  969 270
```

```python
$ python TOTP.py --generate-qr
SECRET: ZFYXJL2T5EXWUWDHOY6MOPTP3H643V4G
https://www.google.com/chart?chs=200x200&chld=M|0&cht=qr&chl=otpauth://totp/Secure%20App%20%28User%20Name%20N%2FA%29?secret=ZFYXJL2T5EXWUWDHOY6MOPTP3H643V4G&issuer=Secure%20App
File Name: QRcode-2021-05-25--16.58.jpg
```

