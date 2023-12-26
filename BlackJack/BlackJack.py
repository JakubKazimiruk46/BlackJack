#Prosty program symulujący grę w Blackjacka
#W python
import random, sys

HEARTS = '♥'
SPADES = '♠'
DIAMONDS = '♦'
CLUBS = '♣'
BACKSIDE = 'tyl'

def GetBet(money):

    while True:

        UserBet = input("Ile chcesz postawic? ('K' aby zakonczyc)\n>").upper()

        if UserBet == 'K':
            print("Dzieki za gre!")

            print("Zapraszamy ponownie do naszego salonu!")
            sys.exit()
        if not UserBet.isdecimal():
            continue
        UserBet = int(UserBet)
        if 1<= UserBet <= money:
            return UserBet


def CreateDeck():

    deck = []

    for suit in (HEARTS, SPADES, DIAMONDS, CLUBS):

        for value in range(2, 11):
            deck.append((suit, str(value)))
        for rank in ('J', 'D', 'K', 'A'):
            deck.append((suit, rank))

    random.shuffle(deck)
    return deck


def DisplayCard(cards):

    rows = ['','','','','']

    for i, card in enumerate(cards):
        rows[0] += ' ___  '

        if card == BACKSIDE:
            rows[1] += '|###| '
            rows[2] += '|###| '
            rows[3] += '|###| '
        else:
            suit, rank = card
            rows[1] += '|{}  | '.format(rank)
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|__{}| '.format(rank)
    for row in rows:
        print(row)


def GetHandValue(cards):

    Aces = 0
    TotalValue = 0

    for card in cards:

        rank = card[1]
        if rank == 'A':
            Aces += 1
        elif rank in ('J', 'D', 'K'):
            TotalValue += 10
        else:
            TotalValue += int(rank)
    
    for i in range(Aces):
        if TotalValue + 11 <= 21:
            TotalValue += 11
        else:
            TotalValue += 1

    return TotalValue

def DisplayHands(PlayerOneHand, PlayerTwoHand, IsHidden):

    if IsHidden:
        print(f'Krupier = {GetHandValue(PlayerOneHand)}')
        DisplayCard(PlayerOneHand)

    else:
        print('Krupier = ???')
        DisplayCard([BACKSIDE] + PlayerOneHand[1:])

    print(f'Gracz = {GetHandValue(PlayerTwoHand)}')
    DisplayCard(PlayerTwoHand)


def GetMove(PlayerTwoHand, money):

    while True:

        moves = ['(D)obierz ', '(S)top ']

        if len(PlayerTwoHand) == 2 and money > 0:
            moves.append('(P)odwoj')
        move = input(''.join(moves) + '\n> ').upper()

        if move in ('D', 'S'):
            return move
        if move == 'P' and '(P)odwoj' in moves:
            return move


def main():

    print("""
Sprobuj uzyskac liczbe punktow jak najbardziej zblizona do 21, ale nie wieksza. Walety, damy i krole maja po 10 punktow.
Asy maja 1 lub 11 punktow
Nacisnij D aby dobrac dodatkowa karte
Nacisnij W aby wstrzymac dobieranie kart
Nacisnij P aby podwoic swoj zaklad, jednak mozesz to zrobic tylko w pierwszej rozgrywce, przed zakonczeniem dobierania kart.
Krupier konczy dobieranie kart gdy osiagnie 17 punktow
    """)

    money = 5000
    while True:
        if money <= 0:
            print("Jestes splukany!")
            print("Dzieki za pozostawienie takiej fortuny ;)")
            sys.exit()
        
        print(f'W twojej kieszeni: {money}')
        bet = GetBet(money)

        deck = CreateDeck()
        PlayerOneHand = [deck.pop(), deck.pop()]
        PlayerTwoHand = [deck.pop(), deck.pop()]

        print(f"Zaklad: {bet}")
        while True:
            DisplayHands(PlayerOneHand, PlayerTwoHand, True)
            print()

            if GetHandValue(PlayerTwoHand) > 21:
                break
            move = GetMove(PlayerTwoHand, money - bet)

            if move == 'P':
                bet *= 2
                print(f'Zwiekszyles zaklad do {bet}!')
                print('Zobaczymy czy Ci sie poszczesci')
            elif move == 'D':
                NewCard = deck.pop()
                suit, rank = NewCard
                print(f'Dobrales: {rank}, {suit}')
                PlayerTwoHand.append(NewCard)
            elif move == 'S':
               break

        if GetHandValue(PlayerTwoHand) <= 21:
            while GetHandValue(PlayerOneHand) < 17:
                    
                PlayerOneHand.append(deck.pop())
                DisplayHands(PlayerOneHand, PlayerTwoHand, True)
        PlayerOneValue = GetHandValue(PlayerOneHand)
        PlayerTwoValue = GetHandValue(PlayerTwoHand)

        if PlayerOneValue > 21:
            print('Krupier przekroczyl 21! Tym razem Ci sie poszczescilo.')
            print(f'Wygrales {bet} PLN!')
            money += bet
        
        elif PlayerTwoValue > 21 or PlayerTwoValue < PlayerOneValue:
            print('Tym razem Ci sie nie udalo :(')
            print(f'Przegrales {bet} PLN!')
            money -= bet

        elif PlayerTwoValue > PlayerOneValue:
            print('Tym razem Ci sie udalo.')
            print(f'Wygrales {bet} PLN!')
            money += bet

        elif PlayerOneValue == PlayerTwoValue:
            print("REMIS!")
            print("Nic nie zyskales... Ale tez niczego nie straciles")

        print()
        print()
        
main()
