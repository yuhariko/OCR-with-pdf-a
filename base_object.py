class ResultObject:
    company_name: str = None
    tax_code: str = None
    table: dict = None
    total_amount: float = None

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items()}
