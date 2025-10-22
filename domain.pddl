(define (domain robot-pick)
  (:requirements :strips :typing)

  ;; Types
  (:types
    place physobj - object
    package vehicle - physobj
    robot - vehicle
    arm - robot
    height - object
  )

  ;; Predicates
  (:predicates
    (in ?pkg - package ?veh - vehicle)
    (at ?obj - physobj ?loc - place)
    (connected ?from - place ?to - place)
    (arm-at ?arm - arm ?height - height)
  )

  ;; Load package onto robot
  (:action load-robot
    :parameters (?pkg - package ?robarm - arm ?robot - robot ?loc - place ?height - height)
    :precondition (and
      (at ?robot ?loc)
      (at ?pkg ?loc)
      (arm-at ?robarm ?height)
    )
    :effect (and
      (not (at ?pkg ?loc))
      (in ?pkg ?robot)
    )
  )

  ;; Unload package from robot
  (:action unload-robot
    :parameters (?pkg - package ?robarm - arm ?robot - robot ?loc - place ?height - height)
    :precondition (and
      (at ?robot ?loc)
      (in ?pkg ?robot)
      (arm-at ?robarm ?height)
    )
    :effect (and
      (not (in ?pkg ?robot))
      (at ?pkg ?loc)
    )
  )

  ;; Drive robot (with package)
  (:action drive-robot-package
    :parameters (?robot - robot ?loc-from - place ?loc-to - place ?pkg - package)
    :precondition (and
      (in ?pkg ?robot)
      (at ?robot ?loc-from)
      (connected ?loc-from ?loc-to)
    )
    :effect (and
      (not (at ?robot ?loc-from))
      (at ?robot ?loc-to)
      (not (at ?pkg ?loc-from))
      (at ?pkg ?loc-to)
    )
  )

  ;; Drive robot (without package)
  (:action drive-robot
    :parameters (?robot - robot ?loc-from - place ?loc-to - place)
    :precondition (and
      (at ?robot ?loc-from)
      (connected ?loc-from ?loc-to)
    )
    :effect (and
      (not (at ?robot ?loc-from))
      (at ?robot ?loc-to)
    )
  )

  ;; Move robotic arm
  (:action move-robarm
    :parameters (?robarm - arm ?height-from - height ?height-to - height)
    :precondition (arm-at ?robarm ?height-from)
    :effect (and
      (not (arm-at ?robarm ?height-from))
      (arm-at ?robarm ?height-to)
    )
  )
)
