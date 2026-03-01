function toFloat64(column)
    new_column = map(x -> 
    (
        if typeof(x) == Int64            # takes only BigFloat, Missing, Integer
            x = isinteger(x) ? (x * 1.0) : x; # convert to Float64
        end;

        x = ismissing(x) ? "" : x;        # no method matching tryparse(::Type{Float64}, ::Missing)
        
        if typeof(x) == String            # tryparse takes only Strings
            x = tryparse(Float64, x)      # returns: Float64 or nothing
        end;   
        
        isnothing(x) ? 0.0 : x;           # options: missing, or "", or 0.0, or nothing
    ), column)                        # input 
    ## I decided to convert ALL missing values to 0.0, otherwise it is a nightmare later
    # returns Array{Float64,1} OR Array{Union{Missing, Float64},1}
    return new_column
end

# https://stackoverflow.com/a/65163457/6312771
#data_array = ["1.2", "-1e3", "", Base.missing, "NA"]
#data = toFloat64(data_array)