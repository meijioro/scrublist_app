import streamlit as st

# IMPORT FUNCTIONS FROM UTILITIES FILE
from utlities import loadCachedData, cleanseEmails, stripWhiteSpace, removeSuffixes, cleanseSpecialChar, removeColumns 

st.set_page_config(
    page_title="Scrubbing Lists App",
    layout="wide",
    initial_sidebar_state="expanded"
)

def app():
  st.title('Scrubbing List')
  # SET COLUMNS
  col1, col2 = st.columns([1,2], gap="large")

  # MAIN COLUMN OUTPUT
  with col2:
      # DEFNINE EMPTY CONTAINER
      placeholder = st.empty()

  # INIT BUTTON STATE
  if "step_one_btn" not in st.session_state:
      st.session_state.step_one_btn = False

  if "step_two_btn" not in st.session_state:
      st.session_state.step_two_btn = False

  if "step_three_btn" not in st.session_state:
      st.session_state.step_three_btn = False

  if "step_four_btn" not in st.session_state:
      st.session_state.step_four_btn = False

  if "step_five_btn" not in st.session_state:
      st.session_state.step_five_btn = False


  # BUTTON CALLBACK TO KEEP STEPS IN SHOWN STATE
  # youtube.com/watch?v=XWKAtQIRyl
  def callback(one,two,three,four,five):
      if (one):
          # step one btn was clicked!
          st.session_state.step_one_btn = True
      
      if (two):
          # step two btn was clicked!
          st.session_state.step_two_btn = True
      
      if (three):
          # step three btn was clicked!
          st.session_state.step_three_btn = True

      if (four):
          # step four btn was clicked!
          st.session_state.step_four_btn = True

      if (five):
          # step five btn was clicked!
          st.session_state.step_four_btn = True

    
  # UPLOAD FILE
  def uploadFile():
      # STEP #1
      col1.subheader('Step #1')
      # upload file
      uploaded_file = col1.file_uploader("Choose .xlsx file (required)", type=['xlsx'])
      sheetname = col1.text_input('Tab name to use (required):')
      upload_submit = col1.button('Upload',on_click=callback,args=(True,False,False,False,False))

      if (upload_submit or st.session_state.step_one_btn):
          if sheetname and uploaded_file is not None:
              readFile(uploaded_file,sheetname)
      

  # READ FILE     
  def readFile(file,sheetname):

      # READ FILE
      dataframe = loadCachedData(file,sheetname)

      # STEP #2
      col1.divider()
      col1.header('Step #2')

      # MULTISELCT FIELD
      keepColumnsList = col1.multiselect('Choose columns to keep.', dataframe.columns.ravel())
      delete_columns_submit = col1.button(label='Step #3 ›',on_click=callback,args=(True,True,False,False,False))

      if (delete_columns_submit or st.session_state.step_two_btn) and keepColumnsList:
          # Drop columns
          dataframe = removeColumns(dataframe,keepColumnsList)
          dataframe = stripWhiteSpace(dataframe)
          dataframe = dataframe.replace("nan", '')
          placeholder.dataframe(dataframe)

          # STEP #3
          col1.divider()
          col1.subheader('Step #3')
          
          # Cache column names 
          columns_list = dataframe.columns.ravel()
          
          # FIELDS
          emailcol = col1.multiselect('Choose primary key email column to cleanse. (required)', columns_list)
          dedupe_emails = col1.checkbox('Delete duplicate emails.')
          remove_personals_emails = col1.checkbox('Remove personal Gmail, Outlook, AOL, Yahoo, Hotmail emails. For CAN & UK opt-in law purposes.')
          cleanse_email_submit = col1.button(label='Step #4 ›',on_click=callback,args=(True,True,True,False,False))

          if cleanse_email_submit or st.session_state.step_three_btn and emailcol:
              dataframe = cleanseEmails(dataframe, emailcol[0], dedupe_emails, remove_personals_emails)
              placeholder.dataframe(dataframe)

              # STEP #4
              col1.divider()
              col1.subheader('Step #4')

              sp_char_columns = col1.multiselect('Choose columns to replace special characters and suffixes. (optional)', columns_list)
              sp_char_submit = col1.button('Step #5 ›',on_click=callback,args=(True,True,True,True,False))
      
              if sp_char_submit or st.session_state.step_four_btn:
                  if sp_char_columns:
                    dataframe = cleanseSpecialChar(dataframe,sp_char_columns)
                    dataframe = removeSuffixes(dataframe, sp_char_columns)
                    placeholder.dataframe(dataframe)

                  # STEP #5
                  col1.divider()
                  col1.subheader('Want to download Everest list?')
                  to_everest_col = col1.selectbox('Choose email column.', columns_list, index=None, on_change=callback, args=(True,True,True,True,True))

                  if to_everest_col:
                      col2.download_button('Download Everest List ↯', dataframe[to_everest_col].to_csv(index=False, header=False),mime='text/csv')
                    


  # INIT
  uploadFile()

