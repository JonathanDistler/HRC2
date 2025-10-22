;; rename to domain.pddl
(define (problem p01)
(:domain robot-pick)

;; Object definitions
(:objects
stretch - robot
stretcharm - arm
tableloc A B - location
table - place
bottle - package
heightlo heightmid heighthi - height
)

;; Initial state
(:init
(at table tableloc)
(at bottle B)
(at stretch A)
(at stretcharm heightmid)
(at table heighthi)
(at bottle heightlo)
(connected A B)
(connected B tableloc)
(connected B A)
(connected tableloc B)
)

;; Goal: bottle should be at the table
(:goal
( (at bottle tableloc))
)
)
