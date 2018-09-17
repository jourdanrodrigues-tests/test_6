class Card:
    def __init__(self, card_number, expiration_month, expiration_year, cvv):
        self.cvv = cvv
        self.card_number = card_number
        self.expiration_year = expiration_year
        self.expiration_month = expiration_month


class SuperChocolateAPI:
    def get_recommendation(self, white_ratio, dark_ratio, milk_ratio):
        # Picture it doing some heavy machine learning thing here
        return []
