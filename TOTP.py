import random
import string
import sys
import hmac
import base64
import struct
import datetime
import urllib.request
import urllib.error
import urllib.parse
from time import sleep, time


def gen_secret():
    # base32 is all Upper case letters and numbers 2-7
    base32_dict = list(string.ascii_uppercase)
    base32_dict = base32_dict + \
        ["{:01d}".format(x) for x in range(2, 8)]

    secret = ""

    for _ in range(32):
        rand_num = random.randrange(31)
        secret += base32_dict[rand_num]

    return secret


def hotp(key, counter, digits, digest):
    # pseduocode found here: https://pypi.org/project/authenticator/
    # key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    key = base64.b32decode(key)
    # Q = unsigned long long
    counter = struct.pack('>Q', counter)
    # use sha1 to hash the secret
    mac = hmac.new(key, counter, digest).digest()
    # reverse the hash and take the last four bits
    offset = mac[-1] & 0x0f
    # L = unsigned long
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].zfill(digits)


def create_totp(key, time_step=30, digits=6, digest='sha1'):
    return hotp(key, int(time() / time_step), digits, digest)


def totp_loop(secret: str):
    totp = create_totp(secret)
    print("OTP code: ", totp[:3] + " " + totp[3:])

    while True:
        # calculate time to sleep at the 30 second and minute mark
        t = datetime.datetime.now()
        sec = (t.second + 60 * t.minute) % 30
        sleep(30 - sec)
        totp = create_totp(secret)
        print("OTP code: ", totp[:3] + " " + totp[3:])


def check_args(sys, command_valid=True):
    if len(sys.argv) <= 1 or len(sys.argv) > 3 or not command_valid:
        print(
            "Accepted commands: \n\t--generate-qr [USERNAME](optional) \n\t--get-otp [USERNAME](optional)")
        exit()


def save_QR_code(qr_url):
    r = urllib.request.urlopen(qr_url)
    QR = r.read()
    date_and_time = datetime.datetime.now().strftime("%Y-%m-%d--%H.%M")
    file_name = 'QRcode-' + date_and_time + ".jpg"
    f = open(file_name, 'wb')
    f.write(QR)
    f.close
    print("File Name:", file_name)


def main():
    check_args(sys)

    # parse line commands
    arg_names = ["application_name", "command", "user_name"]
    args = dict(zip(arg_names, sys.argv))

    if "user_name" not in args:
        args["user_name"] = "User%20Name%20N%2FA"

    if args['command'] == "--get-otp":

        secret = gen_secret()
        print("------ \nGenreateing keys at every 30 second and minute mark")
        print("Cancel program to stop (Crtl+C) \n------")
        print("Secret:", secret)

        totp_loop(secret)

    elif args['command'] == "--generate-qr":
        secret = gen_secret()
        url = "https://www.google.com/chart?chs=200x200&chld=M|0&cht=qr&chl="
        issuer = "Secure%20App"

        print("SECRET:", secret)

        url_2 = "otpauth://totp/" + issuer + "%20" + "%28" +\
            args["user_name"] + "%29?secret=" + secret + "&issuer=" + issuer

        qr_url = url + url_2
        print(qr_url)
        save_QR_code(qr_url)

    else:
        check_args(sys, False)


if __name__ == "__main__":
    main()
