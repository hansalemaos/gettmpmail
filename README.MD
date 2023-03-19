# Generates temporary emails

### pip install gettmpmail

```python

from gettmpmail import get_tmp_email
df = get_tmp_email(n=2, timeout=5, imapfile=None)
print(df)
q = df.aa_checkmail.iloc[0]()
print(q)


r"""
                      aa_id  ...                                    aa_fullname_adb
0  64169847610fe899xxxeb803  ...  (sleep 0.001, input text V, sleep 0.001, input...
1  6416984865f9fcd7xxxx2be8  ...  (sleep 0.001, input text J, sleep 0.001, input...
[2 rows x 7 columns]
{'@context': '/contexts/Message', '@id': '/messages', '@type': 'hydra:Collection', 'hydra:member': [], 'hydra:totalItems': 0}


"""

```
