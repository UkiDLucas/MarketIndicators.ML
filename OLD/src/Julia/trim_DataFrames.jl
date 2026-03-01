#include("../Julia/IndicatorData.jl") # addIndicator!()

using Dates

function trim_DataFrames!(data::Dict{String, IndicatorData.Indicator})
    oldest = get_oldest_common_day(data)
    println("oldest = ", oldest, " ", typeof(oldest), " ", Dates.rata2datetime(oldest) )

    newest = get_newest_common_day(data)
    println("newest = ", newest, " ", typeof(newest), " ", Dates.rata2datetime(newest) )

    
    ## Iterate thru each Indicator
    for key in keys(data) 
        local df = data[key].df
        #println(" - BEFORE ", data[key].name, " size ", size( df) ) 
        
        oldest_row = find_Rata_Die(df, oldest)
        newest_row = find_Rata_Die(df, newest)
        
        data[key].df = df[oldest_row:newest_row, :] # trimming rows, columns stays same
        #println(" - AFTER  ", data[key].name, " size ", size( data[key].df ) ) 
    end
end



function get_newest_common_day(data::Dict{String, IndicatorData.Indicator})
    v = Int64[]

    for key in keys(data) 
        local rata_die = data[key].max_rata_die
        ## The all are the 7 (or whatever was set) days from today
        #println(" - ", Dates.rata2datetime(rata_die), " \t max_rata_die = ", rata_die, " \t", data[key].name  )
        push!(v, rata_die)
    end
    return minimum( v )
end

## Iterate thru all Indicators and find the biggest in minium Rata Die
function get_oldest_common_day(data::Dict{String, IndicatorData.Indicator})
    v = Int64[]

    for key in keys(data) 
        local rata_die = data[key].min_rata_die
        println(" - ", Dates.rata2datetime(rata_die), " \t min_rata_die = ", rata_die, " \t", data[key].name  )
        push!(v, rata_die)
    end
    return maximum( v )
end