class Card:
    def __init__(self, card_number, expiration_month, expiration_year, cvv):
        self.cvv = cvv
        self.card_number = card_number
        self.expiration_year = expiration_year
        self.expiration_month = expiration_month
