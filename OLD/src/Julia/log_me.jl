## https://cormullion.github.io/assets/images/juliamono/juliamanual/stdlib/Logging.html

function log_me(tag::String, message::String, severity::String)
    println(Dates.now, tag, " ", message)
end # function