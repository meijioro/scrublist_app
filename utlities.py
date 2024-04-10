import streamlit as st
import pandas as pd
from lists import suffixes_to_remove, special_characters_to_replace


# CORRECT EMAIL FORMATTING
def correctEmailFormat(email):
    return ''.join(e for e in email if (e.isalnum() or e in ['.', '@']))


# CHECK EMAIl DOMAIN
def checkEmailDomain(email):
    if ('gmail' in email) or ('outlook' in email) or ('yahoo' in email) or ('aol' in email) or ('hotmail' in email):
        return True
    else:
       return False
    

# DROP DUPLICATES AND REMOVE ENTIRE ROW
def dropDuplicates(dataframe, column_name):
    return dataframe.drop_duplicates(column_name, keep='first').reset_index(drop=True)


# CLEANSE EMAILS
def cleanseEmails(dataframe,column_name,dedupe_emails,remove_personals_emails):

  if 'email' in column_name.lower() and column_name is not '0':
    # LOOP TO CLEANSE
    for index, value in enumerate(dataframe[column_name]):
        value = value.replace('_x000D_','').replace('\n','').replace('\n\n','')
        value = correctEmailFormat(value)

        if value[-1] == '.' or value[-1] == "'":
          value = value[0:-1]

        # TRIM LEADING WHITESPACE AND LOWERCASE EMAILS
        dataframe.at[index, column_name] = value.strip().lower()

        # DELETE EMAILS WITH PERSONAL DOMAINS
        if remove_personals_emails:
            if checkEmailDomain(value):
                  dataframe = dataframe.drop(index)
        
    # DROP DUPLICATE EMAILS
    if dedupe_emails:
        dataframe = dropDuplicates(dataframe,column_name)

  else:
     st.sidebar.write('This must be an email column.')
    
  return dataframe


# STRIP WHITESPACE
def stripWhiteSpace(dataframe):

  # loop through each column
  for column_name, col_data in dataframe.items():     
      #loop through each row in column
      for index, value in enumerate(dataframe[column_name]):
          if value:
              dataframe.at[index,column_name] = str(value).strip(); 
  
  return dataframe


# REMOVE SUFFIXES
def removeSuffixes(dataframe, cols):
  # LOOP THROUGH CHOSEN COLS
  for index, column_name in enumerate(cols):
      # LOOP THROUGH VALUES IN COLUMN
      for index2, value in enumerate(dataframe[column_name]):

        # LOOP THROUGH SUFFIX LIST
        for suffix in suffixes_to_remove:
            # REPLACE 
            if suffix in value:
              dataframe.at[index2, column_name] = value.replace(suffix,'')
            
  return dataframe


# REPLACE SPECIAL CHARACTERS 
# https://stackoverflow.com/questions/47088629/how-do-i-iterate-through-a-string-and-replace-specific-chars-in-python-correctly
def cleanseSpecialChar(dataframe,cols):  
  # LOOP THROUGH CHOSEN COLS
  for index, column_name in enumerate(cols):
      # LOOP THROUGH VALUES IN COLUMN
      for index2, value in enumerate(dataframe[column_name]):

        # TURN STRING INTO ARRAY OF CHARS
        string = list(value)

        # LOOP THROUGH ARRAY OF CHARS
        for index3, char in enumerate(string):

          # LOOP THROUGH ARRAY OF SPECIAL CHARS
          for sp_char, htmlentity in special_characters_to_replace.items():
        
            if char == sp_char:
                string[index3] = htmlentity
            
        dataframe.at[index2, column_name] = ''.join(string)

  return dataframe



# KEEP ONLY COLUMNS
def removeColumns(dataframe, keepColumns):
    dataframe = pd.DataFrame(dataframe, columns=keepColumns)
    return dataframe


# CACHE READ FILE
@st.cache_data
def loadCachedData(file,sheetname='',delimitter=','):
    try:
        return pd.read_csv(file, sep=delimitter)
    except:
        return pd.read_excel(file, sheet_name=sheetname, skiprows=0, header=0, dtype=object)
