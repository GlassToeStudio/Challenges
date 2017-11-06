function create_board(n)
  board = {}
  for i= 1, n do
    board[i] = {}
    for j = 1, n do
      if(i ~= 1) then
        board[i][j] = '.'
      else
        board[i][j] = j + 1
      end
    end
  end
  --print_board(board, n)
  return board
end

function lattice_paths(n)
  board = create_board(n)
  for i = 2, n do
    for j = i, n do
      if(j ~= i) then
        board[i][j] = board[i][j - 1] + board[i - 1][j]
      else
        board[i][j] = 2 * board[i - 1][j]
      end
    end
  end  
  --print_board(board, n)
  return board[n][n]
end

n = 20
print("\nProject Euler Problem 15 - Lattice Paths - GTS\n")
print("Board size: " .. n .. ' x ' .. n .. '\n')
print('Answer: ' .. string.format("%11.0f", lattice_paths(n)))
