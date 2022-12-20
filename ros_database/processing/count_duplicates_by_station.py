"""Counts the number of duplicated records for each station"""

def count_mesonet_duplicates():
    """Counts duplicate records by station, writes results to stdout"""

    fo = open("duplicate_lists_assessment.txt", "w")
    for country in country_list:
        stations = station_paths_in_country(country)
        for station_path in stations:
            df = load_iowa_mesonet_for_station(station_path)

            # Find duplicated indices
            isduplicated_index = df.index.duplicated(keep=False)
            # Split data into dataset with duplicate indices and without
            df_no_duplicate = df.loc[~isduplicated_index]
            df_duplicate = df.loc[isduplicated_index]

            # For duplicated indices
            duplicated_index = df[isduplicated_index].index.unique()
            nduplicated = len(duplicated_index)
            for index in duplicated_index:
                # Select row with least missing values
                # Save indices
                are_the_same = df.loc[index].duplicated(keep=False).all()
                #if not are_the_same:
                    
            # Find best combination of duplicate rows
            # For each duplicated index, check rows are the same.
            
            

            fo.write(str(station_path)+" "+str(nduplicated)+"\n")
            for index in duplicated_index:
                # Select row with least missing values
                # Save indices
                are_the_same = df.loc[index].duplicated(keep=False).all()
                if not are_the_same:
                    fo.write(df.loc[index].to_string()+"\n")
            fo.write("------------------\n")
        #break 
            #print(station_path, nduplicated)
            
            #clean_df = df[~isduplicated_row]
            #print(f"Removed {nduplicated} from {len(df)} rows, now {len(clean_df)}")
            
            #for index in duplicated_index:
            #    print(index)
            #    print(df.loc[index])
            #    print('')
            #break
        #break