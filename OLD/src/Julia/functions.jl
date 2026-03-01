# import Pkg; Pkg.add("CSV")
using CSV

# import Pkg; Pkg.add("Dates")
using Dates


# import Pkg; Pkg.add("DataFrames")
using DataFrames

using CSV, DataFrames
using Statistics 


include("add_overal_mean.jl")
include("add_rata_die_column.jl")
include("available_datasets.jl")
include("calculate_average.jl")
include("fetch_data.jl")
include("fetch_csv_from_web.jl")
include("find_Rata_Die.jl")
include("format_dates.jl")
include("populate_missing_dates.jl")
include("position_on_date.jl")
include("preview_data.jl")
include("print_colunms.jl")
include("quantize_column.jl")
include("save_dataset.jl")
include("shift_dates_by_days.jl")
include("update_rata_die.jl")
include("update_yahoo_finance.jl")
include("updated.jl")

println() # prevents the last function from printing