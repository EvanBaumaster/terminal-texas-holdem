import pytest
from poker import Card, Rank, Suit, Deck, HandEvaluator, HandRank, Player, Game

def test_deck_size():
    deck = Deck()
    assert len(deck.cards) == 52

def test_hand_ranking_pair():
    cards = [
        Card(Rank.ACE, Suit.SPADES), Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.TWO, Suit.CLUBS), Card(Rank.THREE, Suit.DIAMONDS),
        Card(Rank.FOUR, Suit.SPADES), Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.SIX, Suit.CLUBS)
    ]
    rank, _ = HandEvaluator.evaluate_hand(cards)
    assert rank == HandRank.PAIR

def test_hand_ranking_flush():
    cards = [
        Card(Rank.ACE, Suit.SPADES), Card(Rank.TEN, Suit.SPADES),
        Card(Rank.TWO, Suit.SPADES), Card(Rank.FOUR, Suit.SPADES),
        Card(Rank.SEVEN, Suit.SPADES), Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.CLUBS)
    ]
    rank, _ = HandEvaluator.evaluate_hand(cards)
    assert rank == HandRank.FLUSH

def test_betting_pot():
    player = Player("Test", 1000)
    # Action: Raise to 100
    action, amount = player.process_action("raise", 100, 20)
    assert amount == 100
    assert player.chips == 900
    assert player.current_bet == 100

def test_player_all_in():
    player = Player("Test", 50)
    # Try to call 100
    action, amount = player.process_action("call", 100, 20)
    assert amount == 50
    assert player.chips == 0
    assert player.all_in == True

def test_ai_action_returns_valid():
    player = Player("AI", 1000, is_ai=True)
    player.hole_cards = [Card(Rank.ACE, Suit.SPADES), Card(Rank.KING, Suit.SPADES)]
    res = player.take_action(20, 20, [], fast_mode=True)
    assert res is not None
    action, amount = res
    assert action in ["fold", "call", "raise", "check"]
