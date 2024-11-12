;hashi_encoding.smt2

(set-logic ALL)
(set-option :produce-models true)

;(declare-const width Int)
;(declare-const height Int)
;(declare-const Grid (Array Int Int)) ;draw grid using an array?
;(declare-fun Cell (Int Int) Int)
;(declare-fun Line (Int Int Int Int) Bool)


(declare-fun Island (Int Int) Int)
(declare-fun Line (Int Int Int Int) Int)

;example
; 5 5
; 2.3.2
; .....
; 3.4.3
; .....
; 2.3.2

;all possible lines between all cells (NOT Islands)
(assert (forall ((x Int) (y Int)) 
                (=> 
                    (and 
                        (>= x 1) (< x 5)
                        (>= y 1) (< y 5) ;Grid here: 5x5
                    )
                    (or
                        (= (Line x y x+1 y) 0)
                        (= (Line x y x+1 y) 1)
                        (= (Line x y x+1 y) 2)

                        (= (Line x y x y+1) 0)
                        (= (Line x y x y+1) 1)
                        (= (Line x y x y+1) 2)
                    )
                )
        )
)


;Lines connecting to an Island
(assert (forall ((x Int) (y Int))
                (=> 
                    (and 
                        (>= x 1) (< x 5)
                        (>= y 1) (< y 5) ;Grid here: 5x5
                    )
                    ;(ite ;for edges and corners?
                        ;(and
                            ;(= x 1) (< y 5) (> y 1))
                        (<=
                            (=
                                (Island x y)
                                (+
                                    (Line (x   y   x   y+1))
                                    (Line (x   y   x+1 y  ))
                                    (Line (x   y-1 x   y  ))
                                    (Line (x-1 y   x   y  )) ;might need to be adjusted for edge Islands
                                )
                            )
                            8 ;no more than 8 bridges can be connected to an island
                        )
                    ;)
                )
        )
)


;Lines can't cross each other
(assert (forall ((x Int) (y Int))
                (=>
                    (and
                        (>= x 1) (< x 5)
                        (>= y 1) (< y 5) ;Grid here: 5x5
                    )
                    (ite
                        (;lines cross each other
                        )

                        (or
                            (= 0 (Line ;soandso
                            ))
                            (= 0 (Line ;andsoand
                            ))   
                        )
                        
                        ;else do nothing? draw both lines?
                    )
                )
        )
)
