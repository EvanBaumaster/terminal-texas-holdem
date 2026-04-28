import random
import argparse
import time
import sys
from enum import IntEnum, auto
from colorama import Fore, Style, init

init(autoreset=True)

class Rank(IntEnum):
    TWO = 2; THREE = 3; FOUR = 4; FIVE = 5; SIX = 6; SEVEN = 7; EIGHT = 8; NINE = 9; TEN = 10
    JACK = 11; QUEEN = 12; KING = 13; ACE = 14

class Suit(IntEnum):
    CLUBS = auto(); DIAMONDS = auto(); HEARTS = auto(); SPADES = auto()

class Card:
    SUIT_SYMBOLS = {Suit.CLUBS: "♣", Suit.DIAMONDS: "♦", Suit.HEARTS: "♥", Suit.SPADES: "♠"}
    RANK_SYMBOLS = {Rank.TWO: "2", Rank.THREE: "3", Rank.FOUR: "4", Rank.FIVE: "5", Rank.SIX: "6",
                    Rank.SEVEN: "7", Rank.EIGHT: "8", Rank.NINE: "9", Rank.TEN: "10",
                    Rank.JACK: "J", Rank.QUEEN: "Q", Rank.KING: "K", Rank.ACE: "A"}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        color = Fore.RED if self.suit in [Suit.HEARTS, Suit.DIAMONDS] else Fore.WHITE
        return f"{color}{self.RANK_SYMBOLS[self.rank]}{self.SUIT_SYMBOLS[self.suit]}{Style.RESET_ALL}"

class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for r in Rank for s in Suit]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None

class HandRank(IntEnum):
    HIGH_CARD = 1; PAIR = 2; TWO_PAIR = 3; THREE_OF_A_KIND = 4; STRAIGHT = 5
    FLUSH = 6; FULL_HOUSE = 7; FOUR_OF_A_KIND = 8; STRAIGHT_FLUSH = 9

class HandEvaluator:
    @staticmethod
    def evaluate_hand(cards):
        """Returns (HandRank, sort_key) for the best 5-card hand."""
        ranks = sorted([c.rank for c in cards], reverse=True)
        suits = [c.suit for c in cards]
        
        # Flush check
        flush_suit = next((s for s in Suit if suits.count(s) >= 5), None)
        flush_cards = sorted([c.rank for c in cards if c.suit == flush_suit], reverse=True) if flush_suit else None

        # Straight check
        unique_ranks = sorted(list(set(ranks)), reverse=True)
        straight_high = None
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i+4] == 4:
                straight_high = unique_ranks[i]
                break
        if not straight_high and {Rank.ACE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE}.issubset(set(unique_ranks)):
            straight_high = Rank.FIVE

        # Straight Flush
        if flush_cards:
            sf_high = None
            for i in range(len(flush_cards) - 4):
                if flush_cards[i] - flush_cards[i+4] == 4:
                    sf_high = flush_cards[i]
                    break
            if not sf_high and {Rank.ACE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE}.issubset(set(flush_cards)):
                sf_high = Rank.FIVE
            if sf_high: return (HandRank.STRAIGHT_FLUSH, sf_high)

        counts = {r: ranks.count(r) for r in set(ranks)}
        sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)

        if sorted_counts[0][1] == 4:
            return (HandRank.FOUR_OF_A_KIND, (sorted_counts[0][0], sorted_counts[1][0]))
        if sorted_counts[0][1] == 3 and sorted_counts[1][1] >= 2:
            return (HandRank.FULL_HOUSE, (sorted_counts[0][0], sorted_counts[1][0]))
        if flush_cards:
            return (HandRank.FLUSH, tuple(flush_cards[:5]))
        if straight_high:
            return (HandRank.STRAIGHT, straight_high)
        if sorted_counts[0][1] == 3:
            kickers = [r for r, c in sorted_counts[1:3]]
            return (HandRank.THREE_OF_A_KIND, (sorted_counts[0][0], *kickers))
        if sorted_counts[0][1] == 2 and sorted_counts[1][1] == 2:
            return (HandRank.TWO_PAIR, (sorted_counts[0][0], sorted_counts[1][0], sorted_counts[2][0]))
        if sorted_counts[0][1] == 2:
            kickers = [r for r, c in sorted_counts[1:4]]
            return (HandRank.PAIR, (sorted_counts[0][0], *kickers))
        
        return (HandRank.HIGH_CARD, tuple(ranks[:5]))

class Player:
    def __init__(self, name, chips, is_ai=True):
        self.name = name
        self.chips = chips
        self.hole_cards = []
        self.is_ai = is_ai
        self.is_folded = False
        self.current_bet = 0
        self.all_in = False

    def reset_round(self):
        self.hole_cards = []
        self.is_folded = False
        self.current_bet = 0
        self.all_in = False

    def take_action(self, current_call_amount, min_raise, community_cards, fast_mode):
        if self.is_folded or self.all_in: return None
        
        if self.is_ai:
            if not fast_mode: time.sleep(1)
            # Basic AI logic: probability threshold
            hand_val = 0
            if len(self.hole_cards) == 2:
                hand_val = (self.hole_cards[0].rank + self.hole_cards[1].rank) / 28.0
            
            call_needed = current_call_amount - self.current_bet
            if call_needed <= 0:
                action = "check"
            elif hand_val > 0.6 or random.random() > 0.3:
                action = "call"
            else:
                action = "fold"
            
            if action == "call" and hand_val > 0.8 and random.random() > 0.7:
                action = "raise"

            return self.process_action(action, current_call_amount, min_raise)
        else:
            print(f"\n{Fore.CYAN}{self.name}'s turn. Chips: {self.chips}")
            print(f"Your cards: {self.hole_cards}")
            call_needed = current_call_amount - self.current_bet
            print(f"Call needed: {call_needed}")
            
            while True:
                choice = input("Action (Fold, Call/Check, Raise): ").lower().strip()
                if choice in ['f', 'fold']: return self.process_action("fold", current_call_amount, min_raise)
                if choice in ['c', 'call', 'check']: return self.process_action("call", current_call_amount, min_raise)
                if choice in ['r', 'raise']:
                    try:
                        amt = int(input(f"Raise to (min {current_call_amount + min_raise}): "))
                        return self.process_action("raise", amt, min_raise)
                    except ValueError: continue
                print("Invalid input.")

    def process_action(self, action, amount, min_raise):
        if action == "fold":
            self.is_folded = True
            return ("fold", 0)
        
        if action == "call" or action == "check":
            call_amount = amount - self.current_bet
            if call_amount >= self.chips:
                actual_bet = self.chips
                self.all_in = True
            else:
                actual_bet = call_amount
            self.chips -= actual_bet
            self.current_bet += actual_bet
            return ("call", actual_bet)
        
        if action == "raise":
            raise_amount = amount - self.current_bet
            if raise_amount >= self.chips:
                actual_bet = self.chips
                self.all_in = True
            else:
                actual_bet = raise_amount
            self.chips -= actual_bet
            self.current_bet += actual_bet
            return ("raise", actual_bet)

class Game:
    def __init__(self, num_opponents, starting_chips, fast_mode):
        self.players = [Player("You", starting_chips, False)] + \
                       [Player(f"AI {i+1}", starting_chips) for i in range(num_opponents)]
        self.fast_mode = fast_mode
        self.deck = None
        self.community_cards = []
        self.pot = 0

    def play_round(self):
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        active_players = [p for p in self.players if p.chips > 0]
        if len(active_players) < 2: return False

        for p in active_players: p.reset_round()
        
        # Deal hole cards
        for _ in range(2):
            for p in active_players: p.hole_cards.append(self.deck.deal())

        # Rounds: Pre-flop, Flop, Turn, River
        stages = [0, 3, 1, 1]
        for s in stages:
            for _ in range(s): self.community_cards.append(self.deck.deal())
            if not self.betting_round(active_players): break
            if len([p for p in active_players if not p.is_folded]) <= 1: break

        self.resolve_winner(active_players)
        return True

    def betting_round(self, active_players):
        current_call = 0
        min_raise = 20
        last_raiser = None
        
        print(f"\n--- Community: {self.community_cards} | Pot: {self.pot} ---")
        
        acting_players = [p for p in active_players if not p.is_folded and not p.all_in]
        if len(acting_players) <= 1 and len([p for p in active_players if not p.is_folded]) > 1:
            return True # All-ins or one player left acting

        while True:
            round_completed = True
            for p in active_players:
                if p.is_folded or p.all_in: continue
                if last_raiser == p: break
                
                res = p.take_action(current_call, min_raise, self.community_cards, self.fast_mode)
                if res:
                    action, amount = res
                    self.pot += amount
                    if action == "raise":
                        current_call = p.current_bet
                        last_raiser = p
                        round_completed = False
                    print(f"{p.name} {action}s {amount if amount > 0 else ''}")
                
                if last_raiser == p: break
            
            if round_completed: break
            if last_raiser is None: break # Everyone checked
        
        # Reset current bets for next stage
        for p in active_players: p.current_bet = 0
        return True

    def resolve_winner(self, active_players):
        not_folded = [p for p in active_players if not p.is_folded]
        print(f"\n--- Showdown! Community: {self.community_cards} ---")
        
        if len(not_folded) == 1:
            winner = not_folded[0]
            print(f"{winner.name} wins {self.pot} chips (others folded)")
        else:
            results = []
            for p in not_folded:
                rank, key = HandEvaluator.evaluate_hand(p.hole_cards + self.community_cards)
                results.append((p, rank, key))
                print(f"{p.name} has {rank.name} with {p.hole_cards}")

            winner = max(results, key=lambda x: (x[1], x[2]))[0]
            print(f"\n{Fore.GREEN}{winner.name} wins the pot of {self.pot} chips!")
        
        winner.chips += self.pot
        self.pot = 0
        # Remove broke players
        self.players = [p for p in self.players if p.chips > 0]

def main():
    parser = argparse.ArgumentParser(description="Terminal Texas Hold 'em")
    parser.add_argument("--opponents", type=int, default=3, help="Number of AI opponents (1-8)")
    parser.add_argument("--chips", type=int, default=1000, help="Starting chips")
    parser.add_argument("--fast", action="store_true", help="Skip delays")
    args = parser.parse_args()

    game = Game(min(args.opponents, 8), args.chips, args.fast)
    print(f"{Fore.YELLOW}Welcome to Terminal Texas Hold 'em!")
    
    while len(game.players) > 1:
        if not game.play_round(): break
        if any(p.name == "You" for p in game.players):
            cont = input("\nNext hand? (Y/n): ").lower()
            if cont == 'n': break
        else:
            print(f"{Fore.RED}You are out of chips! Game Over.")
            break

    print("Thanks for playing!")

if __name__ == "__main__":
    main()
