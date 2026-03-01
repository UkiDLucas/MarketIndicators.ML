using Dates

function format_rata_die_to_us_date(d)
    return Dates.format( rata2datetime(d) , "u. d, yyyy")
end