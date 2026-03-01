
function find_Rata_Die(df::DataFrame, day::Int64)
    #found_items = df[df.Day .== uber_min_day, 1] # Array{Float64,1}
    
    ## identify particular day in DataFrame
    bit_array_01 = ( df.Rata_Die .== day )
    
    record_count = size(df)[1]

    for id in 1:record_count
        if bit_array_01[id] == true
            #println(id, " ", bit_array_01[id])
            return id
        end
    end
end
