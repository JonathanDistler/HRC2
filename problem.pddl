;;rename to problem.pddl

;; Domain definition for robot pick operations
(define (domain robot-pick)
(:requirements :strips :typing)

;; Define types
(:types
place physobj - object
package vehicle - physobj
robot - vehicle
arm - robot ;; subset of robot, representing arms of different heights
location height - place
)

;; Predicates
(:predicates
(in ?pkg - package ?veh - vehicle)
(at ?obj - physobj ?loc - place)
(connected ?from - place ?to - place)
)

;; Load package onto robot
(:action load-robot
:parameters (?pkg - package ?robarm - arm ?robot - robot ?loc - place ?height - height)
:precondition (and
(at ?robot ?loc)
(at ?pkg ?loc)
(at ?robarm ?height)
(at ?pkg ?height)
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
(at ?robarm ?height)
(in ?pkg ?robot)
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

;; Move robotic arm (with package)
(:action move-robarm-package
:parameters (?robarm - arm ?height-from - height ?height-to - height ?pkg - package)
:precondition (and
(at ?pkg ?height-from)
(at ?robarm ?height-from)
)
:effect (and
(not (at ?pkg ?height-from))
(at ?pkg ?height-to)
(not (at ?robarm ?height-from))
(at ?robarm ?height-to)
)
)

;; Move robotic arm (without package)
(:action move-robarm
:parameters (?robarm - arm ?height-from - height ?height-to - height)
:precondition (at ?robarm ?height-from)
:effect (and
(not (at ?robarm ?height-from))
(at ?robarm ?height-to)
)
)
)
