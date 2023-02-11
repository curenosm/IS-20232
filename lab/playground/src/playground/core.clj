(ns playground.core
  (:gen-class)
  (:require [clojure.string :refer [index-of] ] )
  (:require [playground.coder :refer [encode decode decipher] ] )
  )

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println (encode "scones" "meetmebythetree"))
  (println (decode "scones" "egsgqwtahuiljgs"))
  (println (decipher "egsgqwtahuiljgs" "meetmebythetree"))
)
