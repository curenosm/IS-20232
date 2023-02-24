(ns mi-proyecto.app
  (:require [mi-proyecto.core :as core]))

;;ignore println statements in prod
(set! *print-fn* (fn [& _]))

(core/init!)
