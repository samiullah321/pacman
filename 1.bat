python pacman.py 

python pacman.py --frame_t 0 -p reflex_agent


python pacman.py --frame_t 0 -p alpha_beta_agent -l trappedClassic -a depth=3 -q -n 10


python pacman.py --frame_t 0 -p expecti_max_agent -l trappedClassic -a depth=3 -q -n 10

python pacman.py --frame_t 0 -p reflex_agent -l testClassic


python pacman.py --frame_t 0 -p reflex_agent -k 1


python pacman.py --frame_t 0 -p reflex_agent -k 2

python pacman.py --frame_t 0 -p reflex_agent -l openClassic -n 10 -q



python pacman.py --frame_t 0 -p minimax_agent -l minimaxClassic -a depth=4

python pacman.py --frame_t 0 -p minimax_agent -l trappedClassic -a depth=3


python pacman.py --frame_t 0 -p alpha_beta_agent -a depth=3 -l smallClassic
pause

::python pacman.py --frame_t 0 -l smallClassic -p expecti_max_agent -q -n 30

::pause
