(define (problem p01)
  (:domain robot-pick)

  ;; Objects
  (:objects
    stretch - robot
    stretcharm - arm
    tableloc A B - place
    table - place
    bottle - package
    heightlo heightmid heighthi - height
  )

  ;; Initial state
  (:init
    ;; Robot starts at A
    (at stretch A)
    ;; Package starts at B
    (at bottle B)
    ;; Arm initial height
    (arm-at stretcharm heightlo)

    ;; connectivity
    (connected A B)
    (connected B tableloc)
    (connected B A)
    (connected tableloc B)
  )

  ;; Goal
  (:goal
    (at bottle tableloc)
  )
)
