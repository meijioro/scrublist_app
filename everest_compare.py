import streamlit as st

# IMPORT FUNCTIONS FROM UTILITIES FILE
from utlities import loadCachedData, cleanseEmails, stripWhiteSpace, removeSuffixes, cleanseSpecialChar, removeColumns


def app():
  st.title('Remove Invalid Records')
  st.subheader('')

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
      main_file = col1.file_uploader("Main scrubbed list (required)", type=['csv'])
      everest_file = col1.file_uploader("Everest valid emails list (required)", type=['csv'])

      upload_submit = col1.button('Upload',on_click=callback,args=(True,False,False,False,False))
      delimitter = col1.selectbox('Delimiter', (',', '|'))

      if (upload_submit or st.session_state.step_one_btn):
          if everest_file is not None and main_file is not None:
              readFile(everest_file,main_file,delimitter)
      
  # READ FILE     
  def readFile(everest_file,main_file,delimitter):
      # READ FILE
      dataframe_everest = loadCachedData(everest_file,delimitter)
      dataframe_main_list = loadCachedData(main_file, delimitter)

      # GRAB EMAILS COLUMN
      dataframe_valid_emails = dataframe_everest[dataframe_everest.columns[0]].tolist()

      # STEP #2
      col1.divider()
      col1.header('Step #2')

      # SELECTBOX FIELD
      emailColumn = col1.selectbox('Choose email column to remove invalid records.', dataframe_main_list.columns.ravel(),index=None)
      delete_invalid_submit = col1.button(label='Keep Dupes',on_click=callback,args=(True,True,False,False,False))

      if (delete_invalid_submit or st.session_state.step_two_btn) and emailColumn:
        scrubbed = dataframe_main_list[dataframe_main_list[emailColumn].isin(dataframe_valid_emails)]
        placeholder.dataframe(scrubbed)
        #placeholder.download_button(scrubbed)
  
  
  #INIT
  uploadFile()