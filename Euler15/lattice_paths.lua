--[[ algorithm
-- (2 + 1) = 3
-- 3 * 2 = 6 -(2x2)

-- (3 + 1) = 4
-- (4 + 6) = 10
-- 10 * 2 = 20 -(3x3)

-- (4 + 1) = 5
-- (5 + 10) = 15
-- (20 + 15) = 35
-- 35 * 2 = 70 -(4x4)

-- (5 + 1) = 6
-- (6 + 15) = 21
-- (35 + 21) = 56
-- (56 + 70) = 126
-- 126 * 2 = 252 -(5x5)
]]--

function print_board(board,n)
  for i = 1, n do
    local str = ''
    for j = 1, n do
      str = str .. string.format("%6s", board[i][j])
    end
    print(str .. '\n' )
  end
end

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

--[[ output
Project Euler Problem 15 - Lattice Paths - GTS
	
Board size: 5 x 5
	
     2     3     4     5     6
	
     .     6    10    15    21
	
     .     .    20    35    56
	
     .     .     .    70   126
	
     .     .     .     .   252
	
Answer:         252
]]--


