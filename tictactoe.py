# Final Revised Tic Tac Toe Code with Leaderboard and Custom Player Names

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.core.window import Window
import random
import json
import os

Window.clearcolor = (0.1, 0.1, 0.1, 1)

LEADERBOARD_FILE = "leaderboard.json"

# Ensure leaderboard exists
def initialize_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        leaderboard = {"easy": 0, "medium": 0, "hard": 0}
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(leaderboard, f)

def update_leaderboard(difficulty):
    with open(LEADERBOARD_FILE, "r") as f:
        leaderboard = json.load(f)
    leaderboard[difficulty] += 1
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f)

def get_leaderboard():
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.difficulty = 'easy'
        self.player_starts = True
        self.vs_bot = True

        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        self.layout.add_widget(Label(text="Tic Tac Toe", font_size=40, color=(1, 1, 1, 1)))

        mode_box = BoxLayout(spacing=10)
        for label, bot in [("Vs Bot", True), ("Vs Player", False)]:
            btn = ToggleButton(text=label, group='mode', state='down' if bot else 'normal')
            btn.bind(on_press=lambda instance, b=bot: self.set_mode(b))
            mode_box.add_widget(btn)
        self.layout.add_widget(Label(text="Select Game Mode", color=(1,1,1,1)))
        self.layout.add_widget(mode_box)

        self.difficulty_box = BoxLayout(spacing=10)
        for level in ['Easy', 'Medium', 'Hard']:
            btn = ToggleButton(text=level, group='difficulty', state='down' if level == 'Easy' else 'normal')
            btn.bind(on_press=lambda instance, lvl=level.lower(): setattr(self, 'difficulty', lvl))
            self.difficulty_box.add_widget(btn)
        self.layout.add_widget(Label(text="Select Difficulty", color=(1,1,1,1)))
        self.layout.add_widget(self.difficulty_box)

        self.first_box = BoxLayout(spacing=10)
        for label, value in [("You", True), ("Bot", False)]:
            btn = ToggleButton(text=label, group='first', state='down' if value else 'normal')
            btn.bind(on_press=lambda instance, val=value: setattr(self, 'player_starts', val))
            self.first_box.add_widget(btn)
        self.layout.add_widget(Label(text="Who Plays First?", color=(1,1,1,1)))
        self.layout.add_widget(self.first_box)

        self.leaderboard_label = Label(text=self.get_leaderboard_text(), color=(1, 1, 0, 1), font_size=20)
        self.layout.add_widget(self.leaderboard_label)

        btn_start = Button(text='Play', font_size=28, background_color=(0.2, 0.8, 0.4, 1))
        btn_start.bind(on_press=self.start_game)
        self.layout.add_widget(btn_start)

        self.add_widget(self.layout)
        self.set_mode(True)

    def set_mode(self, vs_bot):
        self.vs_bot = vs_bot
        self.difficulty_box.disabled = not vs_bot
        self.difficulty_box.opacity = 1 if vs_bot else 0
        self.first_box.disabled = not vs_bot
        self.first_box.opacity = 1 if vs_bot else 0

    def start_game(self, instance):
        game_screen = self.manager.get_screen('game')
        game_screen.set_options(self.vs_bot, self.difficulty, self.player_starts)
        game_screen.reset_game()
        self.manager.current = 'game'

    def get_leaderboard_text(self):
        scores = get_leaderboard()
        return f"Games Clutched by Dhruv Rathee ( vs Narendra Modi) : Easy - {scores['easy']}, Medium - {scores['medium']}, Hard - {scores['hard']}"

class TicTacToeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vs_bot = True
        self.difficulty = 'easy'
        self.player_starts = True

    def set_options(self, vs_bot, difficulty, player_starts):
        self.vs_bot = vs_bot
        self.difficulty = difficulty
        self.player_starts = player_starts

    def reset_game(self):
        self.clear_widgets()
        self.tic_tac_toe = TicTacToe(vs_bot=self.vs_bot, difficulty=self.difficulty, player_starts=self.player_starts)
        self.add_widget(self.tic_tac_toe)

class TicTacToe(GridLayout):
    def __init__(self, vs_bot=True, difficulty="easy", player_starts=True, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.vs_bot = vs_bot
        self.difficulty = difficulty
        self.player_starts = player_starts

        self.status = Label(text="Dhruv Rathee's turn", font_size=28, size_hint=(1, 0.15), color=(1, 1, 1, 1))
        self.board_layout = GridLayout(cols=3, spacing=5, size_hint=(1, 0.75), padding=10)

        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

        for i in range(3):
            for j in range(3):
                btn = Button(font_size=48, background_color=(0.15, 0.15, 0.15, 1))
                btn.bind(on_press=self.on_button_press)
                self.board_layout.add_widget(btn)
                self.buttons[i][j] = btn

        self.add_widget(self.status)
        self.add_widget(self.board_layout)

        btn_back = Button(text='Back to Home', size_hint=(1, 0.1), background_color=(0.8, 0.2, 0.2, 1))
        btn_back.bind(on_press=self.go_home)
        self.add_widget(btn_back)

        if self.vs_bot and not self.player_starts:
            Clock.schedule_once(lambda dt: self.bot_move(), 0.5)

    def on_button_press(self, btn):
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == btn and not self.board[i][j]:
                    self.make_move(i, j)
                    return

    def make_move(self, i, j):
        self.board[i][j] = self.current_player
        btn = self.buttons[i][j]
        btn.markup = True
        btn.text = f"[color={'FFA500' if self.current_player == 'X' else '3399FF'}]{self.current_player}[/color]"
        btn.disabled = True

        if self.check_winner(self.current_player):
            if self.vs_bot and self.current_player == "X":
                update_leaderboard(self.difficulty)
                self.show_victory_screen()
            else:
                self.status.text = f"{self.get_player_name()} wins!"
                self.disable_all_buttons()
            return
        elif self.is_draw():
            self.status.text = "It's a draw!"
            self.disable_all_buttons()
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.status.text = f"{self.get_player_name()}'s turn"

        if self.vs_bot and self.current_player == "O":
            Clock.schedule_once(lambda dt: self.bot_move(), 0.5)

    def get_player_name(self):
        if self.vs_bot:
            return "Dhruv Rathee" if self.current_player == "X" else "Narendra Modi"
        else:
            return "Dhruv Rathee" if self.current_player == "X" else "Elvish Yadav"

    def bot_move(self):
        move = self.random_move() if self.difficulty == 'easy' else self.minimax_move(max_depth=2 if self.difficulty == 'medium' else None)
        if move:
            row, col = move
            self.make_move(row, col)

    def random_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if not self.board[i][j]]
        return random.choice(empty) if empty else None

    def minimax_move(self, max_depth=None):
        best_score = float('-inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if not self.board[i][j]:
                    self.board[i][j] = 'O'
                    score = self.minimax(0, False, max_depth)
                    self.board[i][j] = None
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def minimax(self, depth, is_maximizing, max_depth=None):
        if max_depth is not None and depth >= max_depth:
            return 0
        if self.check_winner('O'):
            return 10 - depth
        if self.check_winner('X'):
            return depth - 10
        if self.is_draw():
            return 0

        best = float('-inf') if is_maximizing else float('inf')
        for i in range(3):
            for j in range(3):
                if not self.board[i][j]:
                    self.board[i][j] = 'O' if is_maximizing else 'X'
                    score = self.minimax(depth + 1, not is_maximizing, max_depth)
                    self.board[i][j] = None
                    best = max(best, score) if is_maximizing else min(best, score)
        return best

    def check_winner(self, player):
        win_states = [
            [self.board[i] for i in range(3)],
            [[self.board[i][j] for i in range(3)] for j in range(3)],
            [[self.board[i][i] for i in range(3)]],
            [[self.board[i][2 - i] for i in range(3)]]
        ]
        return any(all(cell == player for cell in line) for group in win_states for line in group)

    def is_draw(self):
        return all(cell in ['X', 'O'] for row in self.board for cell in row)

    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.disabled = True

    def show_victory_screen(self):
        self.clear_widgets()
        box = BoxLayout(orientation='vertical', spacing=20, padding=40)
        box.add_widget(Label(text="[b][color=00FF00]Wow! Dhruv defeated Narendra![/color][/b]", markup=True, font_size=30))
        box.add_widget(Label(text="[b][color=FF4500]Dhruv is LEGEND...[/color][/b]", markup=True, font_size=26))
        box.add_widget(Label(text="[b][color=FFA500]...wait for it...[/color][/b]", markup=True, font_size=22))
        box.add_widget(Label(text="[b][color=87CEEB]DARY! LEGENDARY!!![/color][/b]", markup=True, font_size=30))
        btn = Button(text="Back to Home", size_hint=(1, 0.2), background_color=(0.9, 0.3, 0.3, 1))
        btn.bind(on_press=self.go_home)
        box.add_widget(btn)
        self.add_widget(box)

    def go_home(self, instance):
        if self.parent:
            self.parent.manager.get_screen('home').leaderboard_label.text = self.parent.manager.get_screen('home').get_leaderboard_text()
            self.parent.manager.current = 'home'

class TicTacToeApp(App):
    def build(self):
        initialize_leaderboard()
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(TicTacToeScreen(name="game"))
        return sm

if __name__ == "__main__":
    TicTacToeApp().run()