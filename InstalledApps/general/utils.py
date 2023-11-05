class SetMyErrorCustom(Exception):  # be sure to inherits 'Exception'
    def __init__(self, mensaje):
        super().__init__(mensaje)


