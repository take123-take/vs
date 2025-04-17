from flask import Flask, render_template, request

app = Flask(__name__)

# 数独を解く関数（バックトラッキングアルゴリズムで解く例）
def solve_sudoku(board):
    def is_valid(board, row, col, num):
        # 行に同じ数字が存在しないかチェック
        for i in range(9):
            if board[row][i] == num:
                return False
        # 列に同じ数字が存在しないかチェック
        for i in range(9):
            if board[i][col] == num:
                return False
        # 3x3のボックスに同じ数字が存在しないかチェック
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:  # 空のセルがあれば
                    for num in range(1, 10):  # 1から9までの数字を試す
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if solve(board):  # 再帰的に解く
                                return True
                            board[row][col] = 0  # 解けなかったら戻す
                    return False  # どの数字も入らない場合
        return True  # 全てのセルが埋まった場合

    solve(board)
    return board  # 解いた数独のボードを返す

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # フォームから送信された数独のデータを取得
        board = [[int(request.form.get(f'cell_{r}_{c}', '0') or 0) for c in range(9)] for r in range(9)]
        
        # 数独を解く
        solved_board = solve_sudoku(board)
        
        return render_template('result.html', board=solved_board)
    
    # GETリクエストのとき、空の数独ボードを表示
    return render_template('index.html', board=[[0] * 9 for _ in range(9)])

if __name__ == '__main__':
    app.run(debug=True)
