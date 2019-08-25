#this python file reads CSV data, computes total points and save all entries in the database
import pandas as pd

#read all the csv files
basketballm = pd.read_csv('basketball.csv')

#loop through all the entires