# Author: Kyle Greene
# GitHub username: Civenge
# Date: 6/1/2022
# Description:  Portfolio Project - Write a class called RealEstateGame that allows 2 or more people to play a
# simplified version of the game Monopoly.


class Space:
    """
    Represents a space on the board of the RealEstateGame, which has a rent value, space number.
    """

    def __init__(self):
        """
        Constructor method for the Space class.  Takes no parameters.  Initializes
        the private data members: _rent, _space_number and _players_here.
        """
        self._rent = None
        self._space_number = None
        self._players_here = []
        self._owner = None

    def get_rent(self):
        """Get the rent value for the current space."""
        return self._rent

    def set_rent(self, rent_value):
        """Set the rent value for the current space."""
        self._rent = rent_value

    def get_space_number(self):
        """get the space number for the current space"""
        return self._space_number

    def set_space_number(self, space_number):
        """Set the space number for the current space."""
        self._space_number = space_number

    def add_player_here(self, player_name):
        """Add a player to the current space."""
        self._players_here.append(player_name)

    def remove_player_here(self, player_name):
        """Remove a player from the current space."""
        self._players_here.remove(player_name)

    def get_owner(self):
        """get owner of the space object"""
        return self._owner

    def set_owner(self, player):
        """set owner of the space object"""
        self._owner = player


class Player:
    """
    Represents a player who is playing the RealEstateGame.
    """

    def __init__(self, name):
        """
        Constructor method for the Player class.  Takes a name parameter.  Initializes
        the private data members: _name, _location, _properties_owned, and _account_balance.
        """
        self._name = name
        self._location = 0
        self._properties_owned = []
        self._account_balance = None

    def get_name(self):
        """ get method for player name"""
        return self._name

    def add_property(self, space_object):
        """set method to add space number to properties owned list"""
        self._properties_owned.append(space_object)

    def remove_property(self, space_number):
        """set method to remove space number from properties owned list"""
        self._properties_owned.remove(space_number)

    def get_properties_owned(self):
        """get method for properties owned list"""
        return self._properties_owned

    def get_account_balance(self):
        """get method to return the player's account balance"""
        return self._account_balance

    def set_account_balance(self, value):
        """set method for updating the player's account balance"""

        # when creating a Player object, set value to passed in value
        if self._account_balance is None:
            self._account_balance = value

        # for all other times besides creating Player, value will be added to account balance
        else:
            self._account_balance = self._account_balance + value

    def get_location(self):
        """get method for player's current location"""
        return self._location

    def set_location(self, value):
        """set method for player's current location"""
        self._location = value


class RealEstateGame:
    """
    A real estate game class to mimic the game Monopoly.
    """
    def __init__(self):
        self._player_list = []
        self._spaces_list = None

    def create_spaces(self, pass_go_money, spaces_list):
        """
        Takes the amount of money when they land on or pass GO, and
        a LIST of 24 integers (rent amounts) for the remaining spaces.
        """
        # when initializing spaces, create the GO space
        if self._spaces_list is None:

            # create an empty list
            self._spaces_list = []

            # creating the GO space object in the _spaces_list
            self._spaces_list.append(Space())

            # reference the GO space object
            go_space = self._spaces_list[0]

            # set the space number for GO space object
            go_space.set_space_number(0)

            # set rent value for GO space (will be used to increase account balance)
            go_space.set_rent(pass_go_money)

        # sets the remaining spaces 1 through list length
        space_counter = 1
        for space in spaces_list:
            # add a new Space object to _spaces_list
            self._spaces_list.append(Space())

            # reference the current Space object
            space_num = self._spaces_list[space_counter]

            # set the space number for the current space
            space_num.set_space_number(space_counter)

            # set the rent value for the current space
            space_num.set_rent(space)

            # increase counter for next space
            space_counter += 1

    def create_player(self, name, initial_account_balance):
        """
        Creates a player with a name and starting account balance.
        """
        # create a Player object with the name parameter
        new_player = Player(name)

        # set the Player object's starting account balance
        new_player.set_account_balance(initial_account_balance)

        # append the Player object to the _player_list
        self._player_list.append(new_player)

    def get_player_account_balance(self, player_name):
        """
        Takes a player name and returns that player's account balance.
        """
        # iterate through the player list, matching the player name, then return player account balance
        for player in self._player_list:
            if player_name == player.get_name():
                return player.get_account_balance()

    def get_player_current_position(self, player_name):
        """
        Takes a player name and returns the player's current position on the board as
        an integer, with GO being position zero.
        """
        # iterate through the player list, matching the player name, then return the player location as an integer
        for player in self._player_list:
            if player_name == player.get_name():
                return player.get_location()

    def buy_space(self, player_name):
        """
        Takes a player name, and if the account balance is greater than purchase price,
        and if there is not already an owner:
        -deduct the purchase price of the space from the current player's account
        -set the current player as the owner of the space
        -return True
        Otherwise return False
        """
        # use lookup_player_from_name to make sure have the correct player object
        current_player = self.lookup_player_from_name(player_name)
        # print("current player is:", current_player.get_name())

        current_player_account_balance = current_player.get_account_balance()
        # print("current player account balance is:", current_player_account_balance)

        current_player_location = current_player.get_location()
        # print("current player location is:", current_player_location)

        # get the space object where the current player resides
        current_property = self.lookup_space_from_number(current_player_location)

        # 5 times rent cost is purchase price
        current_property_cost = current_property.get_rent() * 5

        # check if the current property is the go space, which can't be bought
        if current_player_location == 0:
            return

        # check if the property already has an owner, return False if so
        if current_property.get_owner() is not None:
            return False

        # check if the player can afford the property, buy it if possible and return True
        if current_player_account_balance > current_property_cost:
            current_player.set_account_balance(-1 * current_property_cost)
            current_player.add_property(current_property)
            current_property.set_owner(current_player)
            return True

        # return False if the player cannot afford the property
        else:
            return False

    def move_player(self, player_name, move_spaces_number):
        """
        Takes a player name and the number of spaces to move.  Checks if a player's account balance is 0,
        if so return without doing anything.  If a player has a positive account balance, move them forward
        1 to 6 spaces.  Pay rent or buy property if possible.  If the player does not have enough money, then
        they lose the game and their properties are available for purchase again.
        """

        # use lookup_player_from_name to make sure we are moving the correct player object
        current_player = self.lookup_player_from_name(player_name)
        # print("current player is:", current_player.get_name())

        # create a variable for current player's account balance
        account_balance = current_player.get_account_balance()
        # if the player has a 0 account balance, they can't move
        if account_balance == 0:
            return

        # raw_move is the current player location plus how far they will move
        raw_move = current_player.get_location() + move_spaces_number

        # set player's new location on board, use modulo 25 to account for landing on or passing go
        current_player.set_location(raw_move % 25)
        # print("current player location is: ", current_player.get_location())
        # print("")

        # when you pass go, increase player account balance by go value
        if raw_move > 24:
            current_player.set_account_balance(self._spaces_list[0].get_rent())

        # check if the space after the move has an owner, if so return doing nothing more
        space_object_at_new_location = self.lookup_space_from_number(current_player.get_location())
        if space_object_at_new_location.get_owner() is None:
            return

        # if the current player is the owner, no rent due, so return doing nothing more
        if space_object_at_new_location.get_owner().get_name() == current_player.get_name():
            return

        # get the current owner of the space
        current_space_owner = space_object_at_new_location.get_owner()

        # figure out the rent for the current space
        current_rent_value = space_object_at_new_location.get_rent()

        # figure out if the rent value exceeds the current_player account balance
        if account_balance <= current_rent_value:
            # set current player account balance to 0
            current_player.set_account_balance(-1 * account_balance)

            # pay current space owner account balance
            current_space_owner.set_account_balance(account_balance)

            # set current player's properties to no owner
            for a_property in current_player.get_properties_owned():
                for space in self._spaces_list:
                    if space.get_owner() == current_player.get_name():
                        space.set_owner(None)
                        a_property.remove_property()

        # when player can afford rent
        if account_balance > current_rent_value:

            # deduct rent to the current player
            current_player.set_account_balance(-1 * current_rent_value)

            # pay rent to the owner
            current_space_owner.set_account_balance(current_rent_value)

    def check_game_over(self):
        """
        Checks if the game is over, meaning all players but one have
        an account balance of 0.  If the game is over, return the winning
        player's name.  Otherwise, return an empty string.
        """
        # create a counter to track players who have a positive account balance
        number_of_players_with_money = 0

        # create an empty list to track the names of players with a positive account balance
        list_of_players_with_money = []

        # iterate through the player list, check if the player has a positive account balance
        for player in self._player_list:
            if player.get_account_balance() > 0:

                # increase the counter for number_of_players_with_money
                number_of_players_with_money += 1

                # add the player's name to list_of_players_with_money
                list_of_players_with_money.append(player.get_name())

        # if only 1 player has a positive account balance, return that player, meaning the game is over
        if number_of_players_with_money <= 1:
            return list_of_players_with_money

        # if more than 1 player has money, return an empty list, meaning the game is not over
        else:
            return []

    def lookup_player_from_name(self, player_name):
        """return the player object corresponding to the name parameter, or None if no such player exists"""
        # iterate through the player list, if the parameter matches a player, return the Player object
        for player in self._player_list:
            if player_name == player.get_name():
                return player

        # return None if no match found
        # return None

    def get_player_list(self):
        """return the list of players"""
        return self._player_list

    def lookup_space_from_number(self, space_number):
        """return the space object from the space number"""
        # iterate through the spaces list, if the parameter matches a space, return the Space object
        for space in self._spaces_list:
            if space_number == space.get_space_number():
                return space


def main():
    game = RealEstateGame()

    rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350,
             350, 350]
    game.create_spaces(50, rents)

    game.create_player("Player 1", 300)
    game.create_player("Player 2", 300)
    game.create_player("Player 3", 300)

    game.move_player("Player 1", 1)
    game.buy_space("Player 1")
    print("Player 1 current position:", game.get_player_current_position("Player 1"))
    print(game.get_player_account_balance("Player 1"))

    game.move_player("Player 2", 2)
    game.buy_space("Player 2")
    print(game.get_player_account_balance("Player 2"))

    game.move_player("Player 3", 3)
    game.buy_space("Player 3")

    game.move_player("Player 1", 1)
    game.buy_space("Player 1")

    game.move_player("Player 2", 1)
    game.buy_space("Player 2")
    game.move_player("Player 1", 1)
    game.move_player("Player 2", 1)
    game.buy_space("Player 2")
    # print(game.get_player_account_balance("Player 1"))
    # print(game.get_player_account_balance("Player 2"))

    # print(game.get_player_list())
    # game.buy_space("Player 1")
    # game.move_player("Player 2", 6)
    #
    # print(game.get_player_account_balance("Player 1"))
    # print(game.get_player_account_balance("Player 2"))
    #
    print(game.check_game_over())


if __name__ == "__main__":
    main()
