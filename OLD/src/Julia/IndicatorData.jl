module IndicatorData

  include("../Julia/fetch_local_CSV_as_DataFrame.jl")
  using DataFrames

  import Base.show
  export Indicator, addIndicator!

  mutable struct Indicator
    name::String
    file::String
    df::DataFrame
    min_rata_die::Int64 # minimum(df[:,1])
    max_rata_die::Int64 # maximum(df[:,1])
  end

  function addIndicator!(dict::Dict, symbol::String, dir = "../DATA/processed/" )
      local file = symbol * ".csv"
      #println("file ", file)
      local df = fetch_local_CSV_as_DataFrame( file, "yyyy-mm-dd", dir )
      local min_rata_die = minimum(df[:,1]) 
      local max_rata_die = maximum(df[:,1]) 
      #println( "min_rata_die ", typeof(min_rata_die), " ", min_rata_die ) # min_rata_die Int64 735493

      dict[symbol] = Indicator(symbol, file, df , min_rata_die, max_rata_die )
      return dict
  end

  show(io::IO, a::Indicator) = print(io, "Indicator $(a.name)")

end # module
