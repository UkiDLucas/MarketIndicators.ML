function save_dataset(
    df::DataFrame,
    file_name="undefined.csv", 
    dir="Data/processed/"
)

file_path = dir*file_name
CSV.write( file_path, df, delim=',' ) # , header=true
return file_path
end