import path_finder

start = "Cristiano Ronaldo"
end = "Bear"

paths = path_finder.bidirectional_BFS(start, end)
path_finder.print_paths(paths)