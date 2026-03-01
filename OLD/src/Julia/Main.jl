## Directory where I store original data (copied form the Web, etc.)
# original_data_directory = "DATA\\original\\" # Windows 10
original_data_directory = "../DATA/original/" # MacOS

#include("MarketIndicators.jl")
include("fetch_csv_from_web.jl")
include("update_yahoo_finance.jl")
include("preprocess_csv.jl")
include("functions.jl") 
include("toFloat64.jl")
include("IndicatorData.jl") 
include("format_rata_die_to_us_date.jl")
include("trim_DataFrames.jl")
include("print_columns_features.jl")
include("fetch_local_CSV_as_DataFrame.jl")



function print_date_time()
    println("============== ", Dates.DateTime(Dates.now() ), " ==============")
end # function

print_date_time(); 

#global symbol_to_predict = "" # Just declaration

while true
    fetch_csv_from_web( "../DATA/Indicators.csv", original_data_directory ); 
    include("Uber_DataFrame.jl"); print_date_time(); 

    global symbol_to_predict = "AAPL"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
    global symbol_to_predict = "BABA"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
    global symbol_to_predict = "BRK_B"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
    global symbol_to_predict = "BYDDF"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
    global symbol_to_predict = "CRSP"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
    global symbol_to_predict = "DJIA"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
    global symbol_to_predict = "F"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
    global symbol_to_predict = "FB"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
    global symbol_to_predict = "GELYF"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
    global symbol_to_predict = "GELYF"; include("predict_Julia_TuriCreate.jl"); print_date_time();  
    global symbol_to_predict = "GOOG"; include("predict_Julia_TuriCreate.jl"); print_date_time();  
    global symbol_to_predict = "GSPC"; include("predict_Julia_TuriCreate.jl"); print_date_time();  
    global symbol_to_predict = "HD"; include("predict_Julia_TuriCreate.jl"); print_date_time();  
    global symbol_to_predict = "MSFT"; include("predict_Julia_TuriCreate.jl"); print_date_time();  
    global symbol_to_predict = "NVDA"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
    global symbol_to_predict = "QCOM"; include("predict_Julia_TuriCreate.jl"); print_date_time();  
    global symbol_to_predict = "RUT"; include("predict_Julia_TuriCreate.jl"); print_date_time();  
    global symbol_to_predict = "TM"; include("predict_Julia_TuriCreate.jl"); print_date_time();  
    global symbol_to_predict = "TPLGX"; include("predict_Julia_TuriCreate.jl"); print_date_time();  
    global symbol_to_predict = "TSLA"; include("predict_Julia_TuriCreate.jl"); print_date_time();
    global symbol_to_predict = "VIX"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
    global symbol_to_predict = "WMT"; include("predict_Julia_TuriCreate.jl"); print_date_time(); 
  
    
    
    



     
    nap_time = 60*60*12 # seconds * minutes * hours
    print_date_time(); println("going to sleep for ", nap_time/(60*60), " hours" )
    sleep(nap_time) 
end # while loop