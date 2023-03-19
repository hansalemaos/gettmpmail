import string
from a_pandas_ex_read_charsep_frames import pd_add_read_charsep_frames
import pandas as pd
from adbescapes import convert_text_each_letter

pd_add_read_charsep_frames()
from a_pandas_ex_imap2df import pd_add_imap2df
import os

pd_add_imap2df()
import time
import json
import random
from charchef import aa_convert_utf8_to_ascii_

aa_convert_utf8_to_ascii_("a")
from kthread_sleep import sleep
import requests
import sys
from functools import partial

maifol = os.path.join(os.path.abspath(os.path.dirname(sys.executable)))
pklnames = os.path.normpath(os.path.join(maifol, "allnamesformatfirst.pkl"))
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions
from deepcopyall import deepcopy

pd_add_apply_ignore_exceptions()
dfnames = pd.read_pickle(pklnames)
codecharssenha = string.printable[:62].replace('"', "")
api_address = "https://api.mail.tm"


def iter_get_random_values_with_max_rep(list_, howmany, maxrep):
    resi = []
    resistr = []
    numbers = list_
    alldi = {f"{repr(x)}{x}": x for x in numbers}
    numbersdi = {}
    for ma in range(maxrep):
        for key, item in alldi.items():
            numbersdi[f"{key}{ma}"] = item
    if (h := len(numbersdi.keys())) < howmany:
        raise ValueError(f"choices: {howmany} / unique: {h}")
    while len(resi) <= howmany - 1:
        [
            (resi.append(numbersdi[g]), resistr.append(g))
            for x in range(len(numbers))
            if len(resi) <= howmany - 1
            and (g := random.choice(tuple(set(numbersdi.keys()) - set(resistr))))
            not in resistr
        ]
    return resi


def get_password_for_adb():
    feax = list(
        iter_get_random_values_with_max_rep(
            list_=codecharssenha, howmany=random.choice(list(range(9, 15))), maxrep=2
        )
    )
    feax2 = iter_get_random_values_with_max_rep(
        list_=[str(x) for x in list(range(9))],
        howmany=random.choice(list(range(1, 3))),
        maxrep=2,
    )
    wholesen = feax + feax2
    random.shuffle(wholesen)
    allsenha = "".join(wholesen)
    return allsenha


def get_random_name():
    firstname = dfnames.sample(1)
    secondname = dfnames.sample(1).sobrenometogether
    wholename = firstname.name.iloc[0] + " " + secondname.iloc[0]

    return aa_convert_utf8_to_ascii_(wholename)


def _get_domains_list():
    while True:
        with requests.get("{}/domains".format(api_address)) as r:
            if r.status_code == 200:
                response = r.json()
                domains = list(map(lambda x: x["domain"], response["hydra:member"]))
                return domains
        sleep(1)


domli = _get_domains_list()


def _generate_password(length):
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def get_account(imapfile):
    """Create and return a new account."""
    myrandomname = "".join(get_random_name())
    myrandomnameescaped = f'"{aa_convert_utf8_to_ascii_(myrandomname)}"'

    try:
        df = pd.Q_read_charsep_frames(
            encoding="utf-8",
            file_or_string=imapfile,
            sep="\t",
        )
        df = df[["0_0", "0_1", "0_2"]]
        df.columns = ["aa_email", "aa_pass", "aa_imap"]
        df = df.dropna()
        aa_email, aa_pass, aa_imap = df.iloc[:1].__array__()[0].tolist()
        df[1:].to_csv(imapfile, sep="\t", index=False, header=False)

        return f"IMAP:{aa_imap}", aa_email, aa_pass, myrandomname, myrandomnameescaped

    except Exception as fe:
        pass

    username = (myrandomname.replace(" ", "")).lower()

    domain = random.choice(domli)
    address = "{}@{}".format(username, domain)

    password = get_password_for_adb()

    response = _make_account_request("accounts", address, password)
    return (
        str(response["id"]),
        response["address"],
        password,
        myrandomname,
        myrandomnameescaped,
    )


def _make_account_request(endpoint, address, password):
    account = {"address": address, "password": password}
    headers = {"accept": "application/ld+json", "Content-Type": "application/json"}
    with requests.post(
        "{}/{}".format(api_address, endpoint), data=json.dumps(account), headers=headers
    ) as r:
        if r.status_code not in [200, 201]:
            raise ValueError
        return r.json()


def emailcontent(address, password):

    jwt = _make_account_request("token", address, password)
    auth_headers = {
        "accept": "application/ld+json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(jwt["token"]),
    }
    page = 1
    with requests.get("{}/messages?page={}".format(api_address, page), headers=auth_headers) as r:

        return json.loads(r.content)


def get_timeout(timeout):
    return time.time() + timeout


def is_timeout(timeo):
    return timeo < time.time()


def get_tmp_email(n=1, timeout=30, imapfile=None):
    df = range(n)
    emailids = []
    emailaddresses = []
    passwords = []
    fullnames = []
    fullnamesescaped = []

    timeobig = get_timeout(timeout)
    timeobig += len(df) * timeout
    for qno in range(len(df)):
        if len(emailids) >= n:
            break
        if is_timeout(timeobig):
            break
        timeo = get_timeout(timeout)
        while True:
            if is_timeout(timeo):
                break

            try:
                (
                    id,
                    emailaddress,
                    password,
                    fullname,
                    myrandomnameescaped,
                ) = get_account(imapfile)
                emailids.append(id)
                emailaddresses.append(emailaddress)
                passwords.append(password)
                fullnames.append(fullname)
                fullnamesescaped.append(myrandomnameescaped)

                break
            except Exception as be:
                sleep(1.1)
                continue

    dfemail = pd.DataFrame(
        [
            emailids,
            emailaddresses,
            passwords,
            fullnames,
            fullnamesescaped,
        ]
    )
    dfemail = dfemail.T.copy()
    dfemail.columns = [
        "aa_id",
        "aa_email",
        "aa_password",
        "aa_fullname",
        "aa_fullname_escaped",
    ]
    dfemail["aa_checkmail"] = dfemail.ds_apply_ignore(
        pd.NA,
        lambda q: deepcopy(partial(emailcontent, q.aa_email, q.aa_password)),
        axis=1,
    )
    dfemail.aa_fullname_escaped = dfemail.aa_fullname_escaped.str.slice(3, -3).apply(
        lambda x: f'"{x}"'
    )
    dfemail["aa_fullname_adb"] = dfemail.aa_fullname.ds_apply_ignore(
        pd.NA,
        lambda q: tuple(
            convert_text_each_letter(
                q.replace("\t", "    ").splitlines(),
                delay=(0.001, 0.002),
                respect_german_letters=True,
                debug=False,
            )
        ),
    )

    return dfemail
