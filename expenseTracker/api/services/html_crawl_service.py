import bs4 as bs
import re
from email.header import decode_header


# todo add try except on find next
class HtmlCrawlService:
    @staticmethod
    def crawl_piraeus(email_message):
        for part in email_message.walk():
            if part.get_content_type() == "text/html":
                body = part.get_payload(decode=True)
                soup = bs.BeautifulSoup(body, "html.parser")

                account_number = (
                    soup.find(string="Λογαριασμός:").find_next().text.strip()
                )
                transaction_amount = (
                    soup.find(string=re.compile(r"Ποσό\s+Συναλλαγής:"))
                    .find_next()
                    .text.strip()
                )
                transaction_type = (
                    soup.find(string=re.compile(r"Τύπος\s+Συναλλαγής:"))
                    .find_next()
                    .text.strip()
                )
                execution_date = (
                    soup.find(string=re.compile(r"Ημερομηνία\s+Εκτέλεσης:"))
                    .find_next()
                    .text.strip()
                )
                value_date = (
                    soup.find(string=re.compile(r"Ημερομηνία\s+Αξίας:"))
                    .find_next()
                    .text.strip()
                )
                ledger_balance = (
                    soup.find(string=re.compile(r"Λογιστικό\s+Υπόλοιπο:"))
                    .find_next()
                    .text.strip()
                )
                available_balance = (
                    soup.find(string=re.compile(r"Διαθέσιμο\s+Υπόλοιπο:"))
                    .find_next()
                    .text.strip()
                )
                sender = (
                    soup.find(string=re.compile(r"Αιτιολογία\s+1:"))
                    .find_next()
                    .text.strip()
                )
                payment_type = (
                    soup.find(string=re.compile(r"Αιτιολογία\s+2:"))
                    .find_next()
                    .text.strip()
                )

                return (
                    account_number,
                    transaction_amount,
                    transaction_type,
                    execution_date,
                    value_date,
                    ledger_balance,
                    available_balance,
                    sender,
                    payment_type,
                )
