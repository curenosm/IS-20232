(ns example.core)

#_(find-doc "xor")

(defn xors
  [max-x max-y]
  (for [x (range max-x) y (range max-y)]
    [x y (rem (bit-xor x y) 256)]))


(def frame (java.awt.Frame.))

#_(for [meth (.getMethods java.awt.Frame)
        :let [method-name (.getName meth)]
        :when (re-find #"Vis" method-name)]
    method-name)

(.setVisible frame true)
(.setSize frame (java.awt.Dimension. 600 600))

(def gfx (.getGraphics frame))

(defn draw-xor
  [xs ys]
  (doseq [[x y xor] (xors xs ys)]
    (.setColor gfx (java.awt.Color. xor xor xor))
    (.fillRect gfx x y 1 1)))


(draw-xor 600 600)
