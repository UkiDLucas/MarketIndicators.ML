# import Pkg; Pkg.add("Dates")

using Printf, Dates
function update_yahoo_finance(uri::String, interval = "1d")
    str_interval = "&interval=" * interval
    str_events = "&events=history"
    unix_date_now = @sprintf("%.0f", Dates.datetime2unix(Dates.now()))
    cut_position = findfirst("period2=", uri)[end] # take only second element of the tuple
    str_begining = uri[1:cut_position]
    uri = str_begining * unix_date_now * str_interval * str_events
    return uri
end
