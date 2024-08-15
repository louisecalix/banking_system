from gui import LogicController, BankFacade





if __name__ == '__main__':
    logic_controller = LogicController()
    facade = BankFacade()
    facade.start()