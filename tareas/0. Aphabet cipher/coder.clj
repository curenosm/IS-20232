;; AUTHOR: Misael Cureño
;; GITHUB: @curenosm
;; DATE: 09-02-2023

(ns alphabet-cipher.coder 
  (:require [clojure.string :refer [index-of] ] ))

;; Data structure used to model the cells
(def matrix (vector 
  "abcdefghijklmnopqrstuvwxyz"
  "bcdefghijklmnopqrstuvwxyza"
  "cdefghijklmnopqrstuvwxyzab"
  "defghijklmnopqrstuvwxyzabc"
  "efghijklmnopqrstuvwxyzabcd"
  "fghijklmnopqrstuvwxyzabcde"
  "ghijklmnopqrstuvwxyzabcdef"
  "hijklmnopqrstuvwxyzabcdefg"
  "ijklmnopqrstuvwxyzabcdefgh"
  "jklmnopqrstuvwxyzabcdefghi"
  "klmnopqrstuvwxyzabcdefghij"
  "lmnopqrstuvwxyzabcdefghijk"
  "mnopqrstuvwxyzabcdefghijkl"
  "nopqrstuvwxyzabcdefghijklm"
  "opqrstuvwxyzabcdefghijklmn"
  "pqrstuvwxyzabcdefghijklmno"
  "qrstuvwxyzabcdefghijklmnop"
  "rstuvwxyzabcdefghijklmnopq"
  "stuvwxyzabcdefghijklmnopqr"
  "tuvwxyzabcdefghijklmnopqrs"
  "uvwxyzabcdefghijklmnopqrst"
  "vwxyzabcdefghijklmnopqrstu"
  "wxyzabcdefghijklmnopqrstuv"
  "xyzabcdefghijklmnopqrstuvw"
  "yzabcdefghijklmnopqrstuvwx"
  "zabcdefghijklmnopqrstuvwxy"))

  
;; ------------------------ HELPER FUNCTIONS -----------------------------------

;; Trim a word to a given length
(defn cut [word n] (subs word 0 n))

;; Get a letter in the matrix from its coordinates
(defn get-char [col row] (get (get matrix row) col))

;; Function that returns the index of a character in the border of the matrix, be a row or a column
(defn get-index [c] (index-of (first matrix) c))

;; Find the first occurrence of the e-letter in the column of the
;; k-letter,  if it's the first step then cur-index it's meant to be zero.
(defn find-col [k-letter e-letter cur-index]
  (def row-index (get-index k-letter))
  (if (= (- (count matrix) 1) cur-index)
    cur-index
    (if (= (str (get-char row-index cur-index)) (str e-letter)) 
      cur-index
      (find-col k-letter e-letter (+ cur-index 1))
    )))

;; Encode the first letter, and then the rest of the message
(defn encode-msg [keyword msg]
  (if (= msg "")
    ""
    (str ; Concatenate
        (get-char (get-index (first msg)) (get-index (first keyword)) ) ; The first encoded letter
        (encode-msg ; And the rest of the encoded message
          (subs msg 1)
          (subs keyword 1)
        )
    )))

;; Decode the first letter, and then the rest of the message
(defn decode-msg [keyword msg]
  (if (= msg "")
    ""
    (str ; Concatenate
      (get-char 0 (find-col (first keyword) (first msg) 0)) ; The first decoded letter
      (decode-msg ; And the rest of the decoded message
        (subs keyword 1)
        (subs msg 1)
      )
    )))

;; Repeat the keyword as many times as necessary to have the same length of the message 
(defn repeat-keyword [keyword msg]
  (cut (.repeat keyword (count msg)) (count msg))
)

;; ------------------------ MAIN FUNCTIONS -----------------------------------

;; Function which takes a keyword and a message and returns it encoded using that password
(defn encode [keyword msg]
  (encode-msg
    (repeat-keyword keyword msg) ; Repeat the keyword as necessary
    msg
  ))

;; Function which receives the password and the encoded message to
;; get finally the decoded message
(defn decode [keyword msg] 
  (decode-msg 
    (repeat-keyword keyword msg) ; Repeat the keyword as necessary
    msg
  ))

;; Function which receives the ciphered text and the original text
;; to get the password which ciphered the text
(defn decipher [cipher msg]
  (if (= msg "")
    "" 
    (str ; Concatenate
      (get-char 0 (find-col (first msg) (first cipher) 0)) ; The first letter of the decipher keyword
      (decipher ;  And the rest of the deciphered password
        (subs cipher 1)
        (subs msg 1)
      )
    )))

;; ---------------------  TESTS  ---------------------------------

(println (encode "scones" "meetmebythetree"))
(println (decode "scones" "egsgqwtahuiljgs"))
(println (decipher "egsgqwtahuiljgs" "meetmebythetree"))