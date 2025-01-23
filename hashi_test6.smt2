;hashi.smt2

(set-logic ALL)
(set-option :produce-models true)


(declare-fun Island (Int Int) Int)
(declare-fun Line (Int Int) Int)

;(declare-fun Number (Int Int) Int)
(declare-fun Connected_in (Int Int) Bool)
; Connected_in (is Node n connected to Node 0, in Int Steps?)

(assert
    (and
        (= (Island 1 1) 2)
        (= (Island 1 3) 2)
        (= (Island 3 1) 2)
        (= (Island 3 3) 2)
    )
)

(assert
    (and
        (or
            (= (Line 1 2) 0)
            (= (Line 1 2) 1)
            (= (Line 1 2) 2)
        )
        (or
            (= (Line 1 3) 0)
            (= (Line 1 3) 1)
            (= (Line 1 3) 2)
        )
        (or
            (= (Line 2 4) 0)
            (= (Line 2 4) 1)
            (= (Line 2 4) 2)
        )
        (or
            (= (Line 3 4) 0)
            (= (Line 3 4) 1)
            (= (Line 3 4) 2)
        )
        (= (Island 1 1) (+ 0 (Line 1 2) (Line 1 3)))
        (= (Island 1 3) (+ 0 (Line 1 2) (Line 2 4)))
        (= (Island 3 1) (+ 0 (Line 1 3) (Line 3 4)))
        (= (Island 3 3) (+ 0 (Line 2 4) (Line 3 4)))
    )
)

(assert
    (forall ((i Int) (n Int))
        (=> (and
                (> i 1) (<= i 4)
                (> n 1) (<= n 4)
            )
            (and
                (= (Connected_in 1 i) true)
                (= (Connected_in n 1) (> (Line 1 n) 0))
                (= (Connected_in n i) (or (Connected_in n (- i 1)) (exists ((z Int))
                                                                        (=> (and
                                                                                (> z 1) (< z 4)
                                                                            )
                                                                            (and (Connected_in z (- i 1)) (> (Line z n) 0))
                                                                        ))))
                (= (Connected_in n 3) true)
            )
        )       
    )
)

(check-sat)
(get-model)