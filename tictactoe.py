"""from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import random

# --------------------- Home Screen ---------------------
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=40)
        layout.add_widget(Label(text="Tic Tac Toe", font_size=32))

        btn_human = Button(text="Play vs Human", size_hint=(1, 0.3))
        btn_bot = Button(text="Play vs Bot", size_hint=(1, 0.3))

        btn_human.bind(on_press=lambda x: setattr(self.manager, 'current', 'human'))
        btn_bot.bind(on_press=lambda x: setattr(self.manager, 'current', 'bot'))

        layout.add_widget(btn_human)
        layout.add_widget(btn_bot)
        self.add_widget(layout)

# --------------------- Game Logic ---------------------
class TicTacToe(GridLayout):
    def __init__(self, mode="human", **kwargs):  # Fixed __init__
        super().__init__(**kwargs)
        self.cols = 3
        self.mode = mode
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                btn = Button(font_size=32)
                btn.bind(on_press=self.on_button_press)
                self.add_widget(btn)
                self.buttons[i][j] = btn

    def on_button_press(self, btn):
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == btn and not self.board[i][j]:
                    self.board[i][j] = self.current_player
                    btn.text = self.current_player
                    if self.check_winner(self.current_player):
                        self.end_game(f"Player {self.current_player} wins!")
                        return
                    elif self.is_draw():
                        self.end_game("It's a draw!")
                        return
                    self.current_player = "O" if self.current_player == "X" else "X"
                    if self.mode == "bot" and self.current_player == "O":
                        self.bot_move()

    def bot_move(self):
        move = self.minimax_move()
        if move:
            row, col = move
            self.board[row][col] = "O"
            self.buttons[row][col].text = "O"
            if self.check_winner("O"):
                self.end_game("Bot wins!")
            elif self.is_draw():
                self.end_game("It's a draw!")
            else:
                self.current_player = "X"

    def minimax_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if not self.board[i][j]]
        return random.choice(empty) if empty else None

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(cell in ["X", "O"] for row in self.board for cell in row)

    def end_game(self, message):
        self.clear_widgets()
        self.cols = 1
        self.add_widget(Label(text=message, font_size=32))

# --------------------- Game Screen ---------------------
class TicTacToeScreen(Screen):
    def __init__(self, mode="human", **kwargs):  # Fixed __init__
        super().__init__(**kwargs)
        self.add_widget(TicTacToe(mode=mode))

# --------------------- App Entry ---------------------
class TicTacToeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(TicTacToeScreen(name="human", mode="human"))
        sm.add_widget(TicTacToeScreen(name="bot", mode="bot"))
        return sm

# --------------------- Main ---------------------
if __name__ == "__main__":  # Fixed __name__ check
    TicTacToeApp().run()
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
import random

Window.clearcolor = (0.1, 0.1, 0.1, 1)


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=50)
        title = Label(text='🎮 Tic Tac Toe', font_size=40, color=(1, 1, 1, 1), size_hint=(1, 0.4))
        layout.add_widget(title)

        btn1 = Button(text='Play vs Human', font_size=24, background_color=(0.2, 0.6, 1, 1))
        btn1.bind(on_press=self.play_human)
        layout.add_widget(btn1)

        btn2 = Button(text='Play vs Bot', font_size=24, background_color=(1, 0.4, 0.4, 1))
        btn2.bind(on_press=self.play_bot)
        layout.add_widget(btn2)

        self.add_widget(layout)

    def play_human(self, instance):
        self.manager.get_screen('human').reset_game()
        self.manager.current = 'human'

    def play_bot(self, instance):
        self.manager.get_screen('bot').reset_game()
        self.manager.current = 'bot'


class TicTacToe(GridLayout):
    def __init__(self, mode="human", **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.mode = mode
        self.status = Label(text="Player ❌'s turn", font_size=28, size_hint=(1, 0.15), color=(1, 1, 1, 1))
        self.board_layout = GridLayout(cols=3, spacing=5, size_hint=(1, 0.85), padding=10)

        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

        for i in range(3):
            for j in range(3):
                btn = Button(font_size=48, background_color=(0.15, 0.15, 0.15, 1), color=(1, 1, 1, 1))
                btn.bind(on_press=self.on_button_press)
                self.board_layout.add_widget(btn)
                self.buttons[i][j] = btn

        self.add_widget(self.status)
        self.add_widget(self.board_layout)

    def on_button_press(self, btn):
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == btn and not self.board[i][j]:
                    self.board[i][j] = self.current_player
                    btn.text = "❌" if self.current_player == "X" else "⭕"
                    btn.color = (1, 0.2, 0.2, 1) if self.current_player == "X" else (0.3, 0.6, 1, 1)
                    if self.check_winner(self.current_player):
                        self.end_game(f"Player {btn.text} wins!")
                        return
                    elif self.is_draw():
                        self.end_game("It's a draw!")
                        return
                    self.current_player = "O" if self.current_player == "X" else "X"
                    self.status.text = f"Player {'❌' if self.current_player == 'X' else '⭕'}'s turn"

                    if self.mode == "bot" and self.current_player == "O":
                        self.bot_move()
                    return

    def bot_move(self):
        move = self.minimax_move()
        if move:
            row, col = move
            btn = self.buttons[row][col]
            btn.trigger_action(duration=0.1)

    def minimax_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if not self.board[i][j]]
        return random.choice(empty) if empty else None

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[r][col] == player for r in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(cell in ['X', 'O'] for row in self.board for cell in row)

    def end_game(self, message):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=20, padding=30)
        layout.add_widget(Label(text=message, font_size=36, color=(1, 1, 1, 1)))
        play_again = Button(text='Play Again', font_size=24, background_color=(0.3, 0.7, 0.3, 1))
        play_again.bind(on_press=lambda x: self.reset_board())
        layout.add_widget(play_again)
        self.add_widget(layout)

    def reset_board(self):
        self.clear_widgets()
        self.__init__(mode=self.mode)


class TicTacToeScreen(Screen):
    def __init__(self, mode="human", **kwargs):
        super().__init__(**kwargs)
        self.mode = mode
        self.tic_tac_toe = TicTacToe(mode=self.mode)
        self.add_widget(self.tic_tac_toe)

    def reset_game(self):
        self.clear_widgets()
        self.tic_tac_toe = TicTacToe(mode=self.mode)
        self.add_widget(self.tic_tac_toe)


class TicTacToeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(TicTacToeScreen(name="human", mode="human"))
        sm.add_widget(TicTacToeScreen(name="bot", mode="bot"))
        sm.current = "home"
        return sm


if __name__ == "__main__":
    TicTacToeApp().run()
