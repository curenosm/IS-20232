(ns mi-proyecto.env
  (:require [clojure.tools.logging :as log]))

(def defaults
  {:init
   (fn []
     (log/info "\n-=[mi-proyecto started successfully]=-"))
   :stop
   (fn []
     (log/info "\n-=[mi-proyecto has shut down successfully]=-"))
   :middleware identity})
