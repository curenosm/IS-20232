(ns mi-proyecto.env
  (:require
    [selmer.parser :as parser]
    [clojure.tools.logging :as log]
    [mi-proyecto.dev-middleware :refer [wrap-dev]]))

(def defaults
  {:init
   (fn []
     (parser/cache-off!)
     (log/info "\n-=[mi-proyecto started successfully using the development profile]=-"))
   :stop
   (fn []
     (log/info "\n-=[mi-proyecto has shut down successfully]=-"))
   :middleware wrap-dev})
